import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, Subset
import os
import sys
import numpy as np
from torchvision.datasets import ImageFolder
from sklearn.metrics import accuracy_score

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

# Hyperparameters
BATCH_SIZE = 16
LEARNING_RATE = 1e-4 # Updated to match user request
WEIGHT_DECAY = 1e-4
EPOCHS = 10 
DATA_DIR = os.path.join(project_root, 'datasets', 'MRI_CROPPED')
NUM_MODELS = 3

def train_single_model(model_idx, device):
    print(f"\n{'='*20}")
    print(f"TRAINING MRI MODEL {model_idx}")
    print(f"{'='*20}")
    
    train_dir = os.path.join(DATA_DIR, 'train')
    val_dir = os.path.join(DATA_DIR, 'val')

    full_train_dataset = ImageFolder(train_dir, transform=transform)
    classes = full_train_dataset.classes
    num_classes = len(classes)
    
    # Bootstrap sampling
    indices = np.random.choice(
        len(full_train_dataset),
        size=len(full_train_dataset),
        replace=True
    )
    train_subset = Subset(full_train_dataset, indices)
    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
    
    val_dataset = ImageFolder(val_dir, transform=transform)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Initialize Model
    model = get_model(num_classes=num_classes).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.3, patience=2)

    best_val_acc = 0.0
    model_save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'swin_bag{model_idx}.pth')

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        
        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if i % 10 == 0:
                print(f"Model {model_idx} - Epoch [{epoch+1}/{EPOCHS}] Batch {i}/{len(train_loader)} Loss: {loss.item():.4f}", flush=True)
            
        epoch_loss = running_loss / len(train_loader)
        
        # Validation
        model.eval()
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        val_acc = accuracy_score(all_labels, all_preds)
        scheduler.step(val_acc)
        
        print(f"Model {model_idx} - Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f}", flush=True)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'classes': classes,
                'num_classes': num_classes
            }, model_save_path)
            print(f"--> Saved better model for Model {model_idx} ({val_acc:.4f})", flush=True)

    print(f"Model {model_idx} Training complete. Best Val Acc: {best_val_acc:.4f}", flush=True)

def train_bagging():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}", flush=True)
    
    for i in range(1, NUM_MODELS + 1):
        train_single_model(i, device)

if __name__ == "__main__":
    train_bagging()
