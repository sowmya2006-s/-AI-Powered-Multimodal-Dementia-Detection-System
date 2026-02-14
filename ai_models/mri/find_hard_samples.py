import torch
import os
import sys
import numpy as np
from torchvision import datasets
from torch.utils.data import DataLoader

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

def find_hard_samples():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Use the first bag model as the base for finding hard samples
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swin_bag1.pth")
    if not os.path.exists(model_path):
        print(f"❌ Error: {model_path} not found. Train bagging models first.")
        return

    checkpoint = torch.load(model_path, map_location=device)
    num_classes = checkpoint.get('num_classes', 4)
    model = get_model(num_classes=num_classes).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    dataset_path = os.path.join(project_root, "datasets", "MRI_CROPPED", "train")
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset path {dataset_path} not found.")
        return

    dataset = datasets.ImageFolder(dataset_path, transform=transform)
    loader = DataLoader(dataset, batch_size=16, shuffle=False)

    hard_indices = []

    print(f"Analyzing {len(dataset)} training samples for hard examples...")

    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(loader):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            for i in range(len(preds)):
                if preds[i] != labels[i]:
                    hard_indices.append(batch_idx * loader.batch_size + i)

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_samples.npy")
    np.save(save_path, hard_indices)
    print(f"✅ Hard samples identified: {len(hard_indices)}")
    print(f"Saved to: {save_path}")

if __name__ == "__main__":
    find_hard_samples()
