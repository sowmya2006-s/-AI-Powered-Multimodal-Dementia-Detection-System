import os
import shutil

SRC = "datasets/MRI_BINARY_SPLIT"     # original dataset directory
DST = "datasets/MRI_BINARY"           # new binary dataset directory

os.makedirs(f"{DST}/Demented", exist_ok=True)
os.makedirs(f"{DST}/NonDemented", exist_ok=True)

demented_classes = ["VeryMildDemented", "MildDemented", "ModerateDemented"]

for cls in demented_classes:
    src_dir = os.path.join(SRC, cls)
    if not os.path.exists(src_dir):
        print(f"Skipping missing directory: {src_dir}")
        continue
    for img in os.listdir(src_dir):
        shutil.copy(os.path.join(src_dir, img),
                    os.path.join(f"{DST}/Demented", img))

non_demented_src = os.path.join(SRC, "NonDemented")
if os.path.exists(non_demented_src):
    for img in os.listdir(non_demented_src):
        shutil.copy(os.path.join(non_demented_src, img),
                    os.path.join(f"{DST}/NonDemented", img))

print("MRI Binary dataset prepared")
