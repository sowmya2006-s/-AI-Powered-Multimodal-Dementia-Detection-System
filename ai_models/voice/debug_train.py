import torch
import torch.nn as nn
import torch.optim as optim
from swin_model import SwinTransformer
import os
import sys
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset

# Configuration
BATCH_SIZE = 4
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'datasets', 'voice_mfcc', 'train')

def main():
    print("Debug script started.")
    device = torch.device('cpu')
    print(f"Using device: {device}")

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    print(f"Checking data dir: {DATA_DIR}")
    if not os.path.exists(DATA_DIR):
        print("Data dir not found!")
        return

    print("Loading dataset...")
    dataset = datasets.ImageFolder(root=DATA_DIR, transform=transform)
    print(f"Dataset size: {len(dataset)}")

    # Use only first 8 images
    subset = Subset(dataset, range(min(8, len(dataset))))
    loader = DataLoader(subset, batch_size=BATCH_SIZE)

    print("Initializing model (pretrained=False)...")
    model = SwinTransformer(num_classes=len(dataset.classes), pretrained=False).to(device)
    print("Model initialized.")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    print("Starting 1 epoch debug loop...")
    model.train()
    for i, (images, labels) in enumerate(loader):
        print(f"Batch {i} start...")
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        print(f"Batch {i} done. Loss: {loss.item()}")

    print("Debug script finished successfully.")

if __name__ == "__main__":
    main()
