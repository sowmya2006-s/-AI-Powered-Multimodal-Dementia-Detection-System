from ultralytics import YOLO
import cv2
import os

# Load the trained YOLO model
# Make sure you have trained the model and have the best.pt file
MODEL_PATH = "runs/detect/train/weights/best.pt"

if not os.path.exists(MODEL_PATH):
    print(f"⚠️ Warning: Model weights not found at {MODEL_PATH}")
    print("Please train the YOLO model first using: yolo detect train model=yolov8n.pt data=brain_roi.yaml epochs=50 imgsz=640 batch=8")

roi_model = None

def load_model():
    global roi_model
    if os.path.exists(MODEL_PATH):
        roi_model = YOLO(MODEL_PATH)
        return True
    return False

def crop_brain(image_path, save_path):
    global roi_model
    if roi_model is None:
        if not load_model():
            return False

    img = cv2.imread(image_path)
    if img is None:
        return False
        
    results = roi_model(img)

    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()  # x1,y1,x2,y2

        if len(boxes) == 0:
            return False  # no detection

        # Take the first detected box (assume it's the brain)
        x1, y1, x2, y2 = map(int, boxes[0])
        
        # Add some padding if needed or ensure it's within bounds
        h, w = img.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        brain_crop = img[y1:y2, x1:x2]

        if brain_crop.size == 0:
            return False

        brain_crop = cv2.resize(brain_crop, (224, 224))
        cv2.imwrite(save_path, brain_crop)

    return True

def process_dataset(input_root, output_root):
    if not os.path.exists(input_root):
        print(f"❌ Error: Input directory {input_root} not found.")
        return

    for class_name in os.listdir(input_root):
        class_input = os.path.join(input_root, class_name)
        if not os.path.isdir(class_input):
            continue
            
        class_output = os.path.join(output_root, class_name)
        os.makedirs(class_output, exist_ok=True)

        print(f"Processing class: {class_name}")
        for img_name in os.listdir(class_input):
            if not img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                continue
                
            in_path = os.path.join(class_input, img_name)
            out_path = os.path.join(class_output, img_name)

            success = crop_brain(in_path, out_path)
            if not success:
                print(f"No brain detected in: {img_name}")

if __name__ == "__main__":
    # You can change these paths as needed
    INPUT_DATASET = "datasets/MRI_SPLIT/train" # Process training data
    OUTPUT_DATASET = "datasets/MRI_CROPPED/train"
    
    # Alternatively process the whole structure if it's organized by class
    # INPUT_DATASET = "original_dataset"
    # OUTPUT_DATASET = "dataset_cropped"
    
    process_dataset(INPUT_DATASET, OUTPUT_DATASET)
    print("✅ Cropping complete!")
