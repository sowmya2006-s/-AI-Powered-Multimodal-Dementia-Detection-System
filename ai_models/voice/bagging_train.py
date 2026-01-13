import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, Subset
from swin_model import SwinTransformer
from dataset import MFCCDataset, get_dataloader
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

# Hyperparameters
BATCH_SIZE = 16
LEARNING_RATE = 3e-5
WEIGHT_DECAY = 1e-4
EPOCHS = 25 # Set to your desired number of epochs
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'datasets', 'voice_mfcc')
NUM_MODELS = 3

def compute_dataset_stats(loader):
    print("Computing training dataset mean/std...", flush=True)
    all_data = []
    for i, (images, _) in enumerate(loader):
        all_data.append(images)
    all_data = torch.cat(all_data, dim=0)
    mean = all_data.mean().item()
    std = all_data.std().item()
    print(f"Dataset stats: mean={mean:.4f}, std={std:.4f}", flush=True)
    return mean, std

def evaluate(model, loader, device, mean, std):
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in loader:
            # Normalize
            images = (images - mean) / (std + 1e-6)
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    acc = accuracy_score(all_labels, all_preds)
    p = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
    r = recall_score(all_labels, all_preds, average='weighted', zero_division=0)
    f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
    
    return acc, p, r, f1

def train_single_model(model_idx, device, train_dir, val_dir, global_mean, global_std):
    print(f"\n{'='*20}")
    print(f"TRAINING MODEL {model_idx}")
    print(f"{'='*20}")
    
    # Load Full Data for bootstrapping
    full_train_dataset = MFCCDataset(train_dir)
    classes = full_train_dataset.classes
    
    # 🔹 STEP 2: Create bootstrap datasets
    indices = np.random.choice(
        len(full_train_dataset),
        size=len(full_train_dataset),
        replace=True
    )
    train_subset = Subset(full_train_dataset, indices)
    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Validation data
    val_loader, _ = get_dataloader(val_dir, batch_size=BATCH_SIZE, shuffle=False)
    
    if train_loader is None or val_loader is None:
        print(f"Failed to load datasets for Model {model_idx}.", flush=True)
        return

    # Initialize Model
    print(f"Initializing SwinTransformer Model {model_idx} (pretrained=True)...", flush=True)
    model = SwinTransformer(num_classes=len(classes)).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.3, patience=3)

    best_val_acc = 0.0
    model_save_path = f'swin_{model_idx}.pth'

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        
        for i, (images, labels) in enumerate(train_loader):
            # Normalize with global stats
            images = (images - global_mean) / (global_std + 1e-6)
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        epoch_loss = running_loss / len(train_loader)
        
        # Validation
        val_acc, val_p, val_r, val_f1 = evaluate(model, val_loader, device, global_mean, global_std)
        scheduler.step(val_acc)
        
        print(f"Model {model_idx} - Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f}", flush=True)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'mean': global_mean,
                'std': global_std,
                'classes': classes
            }, model_save_path)
            print(f"--> Saved better model for Model {model_idx} ({val_acc:.4f})", flush=True)

    print(f"Model {model_idx} Training complete. Best Val Acc: {best_val_acc:.4f}", flush=True)

def train_bagging():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}", flush=True)

    train_dir = os.path.join(DATA_DIR, 'train')
    val_dir = os.path.join(DATA_DIR, 'val')
    
    # Compute Global Stats Once
    print("Computing global normalization stats from full training set...", flush=True)
    full_train_loader, _ = get_dataloader(train_dir, batch_size=BATCH_SIZE, shuffle=False)
    global_mean, global_std = compute_dataset_stats(full_train_loader)
    
    for i in range(1, NUM_MODELS + 1):
        train_single_model(i, device, train_dir, val_dir, global_mean, global_std)

if __name__ == "__main__":
    train_bagging()
