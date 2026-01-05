import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
from pathlib import Path
import torch.nn.functional as F

class MFCCDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = Path(data_dir)
        self.files = []
        self.labels = []
        self.classes = sorted([d.name for d in self.data_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
        
        for cls_name in self.classes:
            cls_dir = self.data_dir / cls_name
            for f in cls_dir.glob("*.npy"):
                self.files.append(f)
                self.labels.append(self.class_to_idx[cls_name])
                
    def __len__(self):
        return len(self.files)
        
    def __getitem__(self, idx):
        file_path = self.files[idx]
        label = self.labels[idx]
        
        # Load (3, 40, T) numpy array
        mfcc_feat = np.load(file_path)
        mfcc_tensor = torch.from_numpy(mfcc_feat).float()
        
        # Internal Resize to (224, 224)
        # Shape is (3, 40, T)
        mfcc_tensor = mfcc_tensor.unsqueeze(0) # (1, 3, 40, T)
        mfcc_tensor = F.interpolate(mfcc_tensor, size=(224, 224), mode="bilinear", align_corners=False)
        mfcc_tensor = mfcc_tensor.squeeze(0) # (3, 224, 224)
        
        return mfcc_tensor, label

def get_dataloader(data_dir, batch_size=16, shuffle=True):
    if not os.path.exists(data_dir):
        print(f"Dataset directory not found: {data_dir}")
        return None, None
        
    dataset = MFCCDataset(data_dir)
    if len(dataset) == 0:
        print(f"No .npy files found in {data_dir}")
        return None, None
        
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return loader, dataset.classes
