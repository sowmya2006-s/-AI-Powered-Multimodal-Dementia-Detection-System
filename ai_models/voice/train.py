import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from swin_model import SwinTransformer
from dataset import get_dataloader
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

# Hyperparameters
BATCH_SIZE = 16
LEARNING_RATE = 3e-5
WEIGHT_DECAY = 1e-4
EPOCHS = 25
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'datasets', 'voice_mfcc')
MODEL_SAVE_PATH = 'best_model.pth'

def compute_dataset_stats(loader):
    print("Computing training dataset mean/std...", flush=True)
    all_data = []
    for i, (images, _) in enumerate(loader):
        if i % 10 == 0:
            print(f"Stats batch {i}...", flush=True)
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
    
    print("Evaluating...", flush=True)
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

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}", flush=True)

    # Load Data
    train_dir = os.path.join(DATA_DIR, 'train')
    val_dir = os.path.join(DATA_DIR, 'val')
    
    print(f"Loading datasets from {train_dir} and {val_dir}...", flush=True)
    train_loader, classes = get_dataloader(train_dir, batch_size=BATCH_SIZE, shuffle=True)
    val_loader, _ = get_dataloader(val_dir, batch_size=BATCH_SIZE, shuffle=False)
    
    if train_loader is None or val_loader is None:
        print("Failed to load datasets.", flush=True)
        return

    # Compute normalization stats from train set
    mean, std = compute_dataset_stats(train_loader)

    # Initialize Model
    print("Initializing SwinTransformer Model (pretrained=True)...", flush=True)
    model = SwinTransformer(num_classes=len(classes)).to(device)
    print("Model ready.", flush=True)
    
    criterion = nn.CrossEntropyLoss()
    
    # Optimizer (Step 6.2)
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )
    
    # Scheduler (Step 7)
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.3, patience=3)

    best_val_acc = 0.0

    print("Starting training loop...", flush=True)
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        
        for i, (images, labels) in enumerate(train_loader):
            # Normalize
            images = (images - mean) / (std + 1e-6)
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if i % 5 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}] Batch {i}/{len(train_loader)} Loss: {loss.item():.4f}", flush=True)
            
        epoch_loss = running_loss / len(train_loader)
        
        # Validation
        val_acc, val_p, val_r, val_f1 = evaluate(model, val_loader, device, mean, std)
        
        scheduler.step(val_acc)
        
        print(f"Epoch [{epoch+1}/{EPOCHS}] Summary - Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f} | F1: {val_f1:.4f}", flush=True)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'mean': mean,
                'std': std,
                'classes': classes
            }, MODEL_SAVE_PATH)
            print(f"--> Saved better model ({val_acc:.4f})", flush=True)

    print(f"Training complete. Best Val Acc: {best_val_acc:.4f}", flush=True)

if __name__ == "__main__":
    train()
