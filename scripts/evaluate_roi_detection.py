from ultralytics import YOLO
import os
import numpy as np

# Load the trained YOLO model
MODEL_PATH = "runs/detect/train/weights/best.pt"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: {MODEL_PATH} not found. Train the YOLO model first.")
    exit(1)

model = YOLO(MODEL_PATH)

image_folder = "mri_roi_dataset/images/test"
label_folder = "mri_roi_dataset/labels/test"

if not os.path.exists(image_folder) or not os.path.exists(label_folder):
    print(f"❌ Error: Test dataset folders not found. Expected {image_folder} and {label_folder}")
    exit(1)

ious = []

print(f"Evaluating ROI Detection on {image_folder}...")

for img_name in os.listdir(image_folder):
    if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    img_path = os.path.join(image_folder, img_name)
    # Handle different extensions for labels
    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(label_folder, label_name)

    if not os.path.exists(label_path):
        continue

    results = model(img_path, verbose=False)[0]

    if len(results.boxes) == 0:
        print(f"⚠️ No brain detected in: {img_name}")
        ious.append(0.0) # Penalty for miss
        continue

    # Predicted box [x1, y1, x2, y2]
    pred_box = results.boxes.xyxy[0].cpu().numpy()

    # True box from annotations
    with open(label_path, "r") as f:
        line = f.readline().strip()
        if not line:
            continue
            
        data = line.split()
        if len(data) < 5:
            continue
            
        _, x_center, y_center, w, h = map(float, data)

    img = results.orig_img
    H, W = img.shape[:2]

    # Convert normalized YOLO format to pixel coordinates
    x1 = (x_center - w/2) * W
    y1 = (y_center - h/2) * H
    x2 = (x_center + w/2) * W
    y2 = (y_center + h/2) * H
    true_box = np.array([x1, y1, x2, y2])

    # Compute IoU (Intersection over Union)
    xi1 = max(pred_box[0], true_box[0])
    yi1 = max(pred_box[1], true_box[1])
    xi2 = min(pred_box[2], true_box[2])
    yi2 = min(pred_box[3], true_box[3])

    inter_width = max(0, xi2 - xi1)
    inter_height = max(0, yi2 - yi1)
    inter_area = inter_width * inter_height
    
    pred_area = (pred_box[2] - pred_box[0]) * (pred_box[3] - pred_box[1])
    true_area = (true_box[2] - true_box[0]) * (true_box[3] - true_box[1])
    union_area = pred_area + true_area - inter_area

    if union_area == 0:
        iou = 0.0
    else:
        iou = inter_area / union_area
        
    ious.append(iou)

if not ious:
    print("❌ No images were evaluated.")
else:
    mean_iou = np.mean(ious)
    print(f"\n🧠 Brain ROI Detection Mean IoU: {mean_iou:.3f}")
    print(f"📦 Bounding Box Accuracy (IoU%): {mean_iou*100:.2f}%\n")
