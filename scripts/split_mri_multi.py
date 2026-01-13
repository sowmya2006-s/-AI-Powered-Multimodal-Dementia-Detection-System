import os
import shutil
import random
from pathlib import Path

def split_data():
    base_dir = Path(r"c:\sowmya\AI-Powered-Multimodal-Dementia-Detection-System\-AI-Powered-Multimodal-Dementia-Detection-System\datasets")
    source_dir = base_dir / "MRI_BINARY_SPLIT" # This actually contains the 4 class folders
    target_dir = base_dir / "MRI_MULTI_SPLIT"

    classes = ["NonDemented", "VeryMildDemented", "MildDemented", "ModerateDemented"]
    
    # Split ratios
    train_ratio = 0.7
    val_ratio = 0.15
    test_ratio = 0.15

    for cls in classes:
        print(f"Processing class: {cls}")
        src_cls_dir = source_dir / cls
        if not src_cls_dir.exists():
            print(f"Warning: {src_cls_dir} does not exist. Skipping.")
            continue

        images = [f for f in os.listdir(src_cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)

        n = len(images)
        train_idx = int(n * train_ratio)
        val_idx = int(n * (train_ratio + val_ratio))

        train_files = images[:train_idx]
        val_files = images[train_idx:val_idx]
        test_files = images[val_idx:]

        for split, files in zip(["train", "val", "test"], [train_files, val_files, test_files]):
            dst_dir = target_dir / split / cls
            dst_dir.mkdir(parents=True, exist_ok=True)
            for f in files:
                shutil.copy(src_cls_dir / f, dst_dir / f)

    print(f"Done! 4-class split created at {target_dir}")

if __name__ == "__main__":
    split_data()
