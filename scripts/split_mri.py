import os, random, shutil

random.seed(42)

SRC = "datasets/MRI_BINARY"
DST = "datasets/MRI_SPLIT"

splits = {"train": 0.7, "val": 0.15, "test": 0.15}

for split in splits:
    for cls in ["Demented", "NonDemented"]:
        os.makedirs(f"{DST}/{split}/{cls}", exist_ok=True)

for cls in ["Demented", "NonDemented"]:
    src_cls_dir = f"{SRC}/{cls}"
    if not os.path.exists(src_cls_dir):
        print(f"Skipping missing directory: {src_cls_dir}")
        continue
    files = os.listdir(src_cls_dir)
    random.shuffle(files)

    n = len(files)
    train_end = int(0.7 * n)
    val_end = int(0.85 * n)

    split_map = {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:]
    }

    for split, imgs in split_map.items():
        for img in imgs:
            shutil.copy(f"{SRC}/{cls}/{img}",
                        f"{DST}/{split}/{cls}/{img}")

print("Train/Val/Test split done")
