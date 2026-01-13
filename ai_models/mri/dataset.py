import os
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    )
])

def get_loaders(base_dir, batch_size=16):
    # Determine the absolute path to the datasets directory relative to this file
    # Or just use the paths relative to the project root
    train_path = os.path.join(base_dir, "train")
    val_path = os.path.join(base_dir, "val")
    test_path = os.path.join(base_dir, "test")

    train = ImageFolder(train_path, transform=transform)
    val   = ImageFolder(val_path, transform=transform)
    test  = ImageFolder(test_path, transform=transform)

    return (
        DataLoader(train, batch_size=batch_size, shuffle=True),
        DataLoader(val, batch_size=batch_size),
        DataLoader(test, batch_size=batch_size)
    )
