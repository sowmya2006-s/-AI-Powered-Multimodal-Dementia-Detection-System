import torch
import torch.nn.functional as F
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from torchvision import datasets
from torch.utils.data import DataLoader

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

def generate_confusion_matrix():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Use the boosted model as it represents the highest complexity
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swin_boosted.pth")
    if not os.path.exists(model_path):
        print(f"⚠️ Warning: {model_path} not found. Trying best_mri_swin.pth")
        model_path = os.path.join(project_root, "best_mri_swin.pth")

    if not os.path.exists(model_path):
        print(f"❌ Error: Model file not found. Please train a model first.")
        return

    checkpoint = torch.load(model_path, map_location=device)
    num_classes = checkpoint.get('num_classes', 4)
    model = get_model(num_classes=num_classes).to(device)
    
    # Check if checkpoint is a state_dict or a dict containing state_dict
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
        
    model.eval()

    test_dir = os.path.join(project_root, "datasets", "MRI_CROPPED", "test")
    if not os.path.exists(test_dir):
        print(f"❌ Error: Test dataset {test_dir} not found.")
        return

    test_dataset = datasets.ImageFolder(test_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    
    classes = test_dataset.classes
    print(f"Generating confusion matrix for classes: {classes}")

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    cm = confusion_matrix(all_labels, all_preds)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=classes, yticklabels=classes, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("MRI Dementia Classification Confusion Matrix")
    plt.tight_layout()
    
    save_path = "confusion_matrix_mri.png"
    plt.savefig(save_path)
    print(f"✅ Confusion matrix saved as {save_path}")
    
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, target_names=classes))
    
    plt.show()

if __name__ == "__main__":
    generate_confusion_matrix()
