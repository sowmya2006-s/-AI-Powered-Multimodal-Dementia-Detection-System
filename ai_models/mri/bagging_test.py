import torch
import torch.nn.functional as F
import os
import sys
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

def load_model_mri(model_path, device):
    checkpoint = torch.load(model_path, map_location=device)
    num_classes = checkpoint.get('num_classes', 4)
    model = get_model(num_classes=num_classes).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model

def evaluate_bagging():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    model_dir = os.path.dirname(os.path.abspath(__file__))
    model_paths = [
        os.path.join(model_dir, 'swin_bag1.pth'),
        os.path.join(model_dir, 'swin_bag2.pth'),
        os.path.join(model_dir, 'swin_bag3.pth'),
        os.path.join(model_dir, 'swin_boosted.pth')
    ]

    # Load models
    models = []
    checkpoint_classes = None
    for path in model_paths:
        if os.path.exists(path):
            models.append(load_model_mri(path, device))
            if checkpoint_classes is None:
                checkpoint_classes = torch.load(path, map_location=device).get('classes')
        else:
            print(f"Warning: Model {path} not found.")

    if not models:
        print("❌ Error: No models found for evaluation.")
        return

    # Load test data
    test_dir = os.path.join(project_root, 'datasets', 'MRI_CROPPED', 'test')
    if not os.path.exists(test_dir):
        print(f"❌ Error: Test directory {test_dir} not found.")
        return

    test_dataset = ImageFolder(test_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    
    classes = test_dataset.classes
    print(f"Evaluating on classes: {classes}")

    all_labels = []
    all_ensemble_preds = []
    
    # Store individual model accuracies for comparison
    individual_preds = [[] for _ in range(len(models))]

    print(f"Processing {len(test_dataset)} images...")

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            
            # Get predictions for each model
            batch_probs = []
            for i, model in enumerate(models):
                logits = model(images)
                probs = F.softmax(logits, dim=1)
                batch_probs.append(probs)
                
                # For individual accuracy
                _, s_preds = torch.max(probs, 1)
                individual_preds[i].extend(s_preds.cpu().numpy())

            # Average probabilities
            avg_probs = torch.mean(torch.stack(batch_probs), dim=0)
            _, ensemble_preds = torch.max(avg_probs, 1)
            
            all_ensemble_preds.extend(ensemble_preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Calculate Accuracies
    print("\n--- RESULTS ---")
    for i, preds in enumerate(individual_preds):
        acc = accuracy_score(all_labels, preds)
        print(f"Model {i+1} Accuracy: {acc:.4f}")

    ensemble_acc = accuracy_score(all_labels, all_ensemble_preds)
    print(f"\n🚀 Bagged Ensemble Accuracy: {ensemble_acc:.4f}")
    
    # Detailed Report
    print("\nClassification Report (Ensemble):")
    print(classification_report(all_labels, all_ensemble_preds, target_names=classes))
    
    # Confusion Matrix
    print("\nConfusion Matrix (Ensemble):")
    print(confusion_matrix(all_labels, all_ensemble_preds))

if __name__ == "__main__":
    evaluate_bagging()
