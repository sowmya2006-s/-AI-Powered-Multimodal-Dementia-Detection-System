import os
import random
import shutil

random.seed(42)

BASE_DIR = "mri_roi_dataset"
IMG_DIR = os.path.join(BASE_DIR, "images")
LBL_DIR = os.path.join(BASE_DIR, "labels")

# Check if directories exist
if not os.path.exists(IMG_DIR) or not os.path.exists(LBL_DIR):
    print(f"❌ Error: {IMG_DIR} or {LBL_DIR} not found. Please ensure you have labeled the images.")
    exit(1)

images = [f for f in os.listdir(IMG_DIR) if f.endswith(('.jpg', '.png'))]
random.shuffle(images)

total = len(images)
if total == 0:
    print("❌ Error: No images found in the dataset folder.")
    exit(1)

train_split = int(0.7 * total)
val_split = int(0.85 * total)

splits = {
    "train": images[:train_split],
    "val": images[train_split:val_split],
    "test": images[val_split:]
}

for split, files in splits.items():
    os.makedirs(os.path.join(IMG_DIR, split), exist_ok=True)
    os.makedirs(os.path.join(LBL_DIR, split), exist_ok=True)

    for file in files:
        name = os.path.splitext(file)[0]
        
        src_img = os.path.join(IMG_DIR, file)
        dst_img = os.path.join(IMG_DIR, split, file)
        
        src_lbl = os.path.join(LBL_DIR, name + ".txt")
        dst_lbl = os.path.join(LBL_DIR, split, name + ".txt")

        if os.path.exists(src_img):
            shutil.move(src_img, dst_img)
        
        if os.path.exists(src_lbl):
            shutil.move(src_lbl, dst_lbl)

print("✅ Dataset split complete!")
