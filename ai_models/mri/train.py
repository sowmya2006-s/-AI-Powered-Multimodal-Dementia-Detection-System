import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.dataset import get_loaders
from ai_models.mri.model import get_model

def train_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # The dataset can be original or cropped
    # Default: datasets/MRI_SPLIT
    dataset_name = "MRI_SPLIT" 
    if os.path.exists(os.path.join("datasets", "MRI_CROPPED")):
        dataset_name = "MRI_CROPPED"
        print(f"✨ Found cropped dataset. Using {dataset_name}")
    
    base_dir = os.path.join("datasets", dataset_name)
    train_loader, val_loader, _ = get_loaders(base_dir)

    model = get_model().to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=3e-5,
        weight_decay=1e-4
    )
    scheduler = ReduceLROnPlateau(optimizer, patience=3, factor=0.3)

    best_acc = 0
    num_epochs = 25

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        model.eval()
        correct = total = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                preds = model(x).argmax(1)
                correct += (preds == y).sum().item()
                total += y.size(0)

        acc = correct / total
        scheduler.step(acc)

        print(f"Epoch {epoch+1}/{num_epochs} | Loss {total_loss:.3f} | Val Acc {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), "best_mri_swin.pth")
            print(f"New best model saved with accuracy: {acc:.4f}")

    print("✅ Training complete")

if __name__ == "__main__":
    train_model()
