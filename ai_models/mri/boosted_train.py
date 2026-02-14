import torch
import torch.nn as nn
from torch.optim import AdamW
import numpy as np
import os
import sys
from torchvision import datasets
from torch.utils.data import DataLoader, WeightedRandomSampler

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

def train_boosted_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load hard samples
    hard_samples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_samples.npy")
    if not os.path.exists(hard_samples_path):
        print(f"❌ Error: {hard_samples_path} not found. Run find_hard_samples.py first.")
        return
    
    hard_samples = np.load(hard_samples_path)

    dataset_path = os.path.join(project_root, "datasets", "MRI_CROPPED", "train")
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset path {dataset_path} not found.")
        return

    dataset = datasets.ImageFolder(dataset_path, transform=transform)
    classes = dataset.classes
    num_classes = len(classes)

    # Calculate weights for sampling
    # Boost hard samples by a factor of 3.0
    weights = np.ones(len(dataset))
    weights[hard_samples] = 3.0
    
    sampler = WeightedRandomSampler(weights, len(weights))
    loader = DataLoader(dataset, batch_size=16, sampler=sampler)

    # Initialize Model (Swin Transformer)
    model = get_model(num_classes=num_classes).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=1e-4)

    num_epochs = 5 # As requested by user
    print(f"Starting boosted training for {num_epochs} epochs...")

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs} | Loss: {total_loss:.4f}")

    # Save boosted model
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swin_boosted.pth")
    torch.save({
        'model_state_dict': model.state_dict(),
        'classes': classes,
        'num_classes': num_classes
    }, save_path)
    print(f"✅ Boosted model saved to: {save_path}")

if __name__ == "__main__":
    train_boosted_model()
