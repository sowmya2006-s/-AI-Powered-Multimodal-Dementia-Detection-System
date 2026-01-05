import torch
import torch.nn as nn
from swin_model import SwinTransformer
from dataset import get_dataloader
import os
import sys
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import numpy as np

# Configuration
BATCH_SIZE = 16
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'datasets', 'voice_mfcc', 'test')
MODEL_PATH = 'best_model.pth'

def test():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load Checkpoint
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found at {MODEL_PATH}")
        return
        
    checkpoint = torch.load(MODEL_PATH, map_location=device)
    model_state = checkpoint['model_state_dict']
    mean = checkpoint['mean']
    std = checkpoint['std']
    classes = checkpoint['classes']
    
    print(f"Loaded model from {MODEL_PATH}")
    print(f"Classes: {classes}")

    # Load Test Data
    print(f"Loading test data from: {DATA_DIR}")
    test_loader, _ = get_dataloader(DATA_DIR, batch_size=BATCH_SIZE, shuffle=False)
    
    if test_loader is None:
        print("Failed to load test dataset.")
        return

    # Initialize Model
    model = SwinTransformer(num_classes=len(classes)).to(device)
    model.load_state_dict(model_state)
    model.eval()
    
    all_preds = []
    all_labels = []
    
    print("Starting evaluation...")
    with torch.no_grad():
        for images, labels in test_loader:
            # Apply normalization stored in checkpoint
            images = (images - mean) / (std + 1e-6)
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Metrics
    acc = accuracy_score(all_labels, all_preds)
    p = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
    r = recall_score(all_labels, all_preds, average='weighted', zero_division=0)
    f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
    
    print("-" * 30)
    print(f"Test Accuracy: {acc*100:.2f}%")
    print(f"Precision: {p:.4f}")
    print(f"Recall: {r:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("-" * 30)
    
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, target_names=classes))
    
    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title='Confusion Matrix',
           ylabel='Actual',
           xlabel='Predicted')

    # Loop over data dimensions and create text annotations.
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print("Confusion matrix saved to confusion_matrix.png")

if __name__ == "__main__":
    test()
