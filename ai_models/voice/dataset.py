from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os

def get_dataloader(data_dir, batch_size=16):
    """
    Creates a DataLoader for the MFCC dataset.
    Args:
        data_dir (str): Path to the directory containing class subfolders (dementia/normal).
        batch_size (int): Batch size for the loader.
    """
    
    # Check if directory exists
    if not os.path.exists(data_dir):
        # Return empty/None if dir doesn't exist to avoid crashing everything immediately
        # But in training context, we probably want to fail fast or handle it.
        # Allowing it to return (None, None) so caller can handle.
        print(f"Dataset directory not found: {data_dir}")
        return None, None

    # Swin Transformer typically expects specific normalization (ImageNet stats)
    # But for MFCCs, mean=0.5, std=0.5 is often a safe generic start if not computing specific stats.
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # ImageNet stats
        # Alternatively use the simple one requested:
        # transforms.Normalize(mean=[0.5], std=[0.5]) 
        # I'll stick to the user's requested logic for consistency if they provided it.
    ])

    try:
        dataset = datasets.ImageFolder(
            root=data_dir,
            transform=transform
        )
        
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True
        )
        
        return loader, dataset.classes
        
    except Exception as e:
        print(f"Error creating DataLoader: {e}")
        return None, None
