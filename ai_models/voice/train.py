import torch
import torch.nn as nn
import torch.optim as optim
from swin_model import SwinTransformer
from dataset import get_dataloader
import os

# Hyperparameters
BATCH_SIZE = 16
LEARNING_RATE = 1e-4
EPOCHS = 10
DATA_DIR = '../../datasets/voice_mfcc'
MODEL_SAVE_PATH = 'best_model.pth'

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load Data
    train_loader, classes = get_dataloader(DATA_DIR, batch_size=BATCH_SIZE)
    
    if train_loader is None:
        print("Failed to load dataset. Exiting training.")
        return

    print(f"Classes found: {classes}")

    # Initialize Model
    model = SwinTransformer(num_classes=len(classes)).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_loss = float('inf')

    # Training Loop
    print("Starting training...")
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {epoch_loss:.4f}")
        
        # Save best model
        if epoch_loss < best_loss:
            best_loss = epoch_loss
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"Saved best model with loss: {best_loss:.4f}")

    print("Training complete.")

if __name__ == "__main__":
    train()
