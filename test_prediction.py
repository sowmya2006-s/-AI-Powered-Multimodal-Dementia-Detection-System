import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from ai_models.mri.inference import predict_mri

def run_test():
    # Find the first image in mri_roi_dataset/images
    img_dir = "mri_roi_dataset/images"
    if not os.path.exists(img_dir):
        print("Error: mri_roi_dataset/images folder not found.")
        return

    images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png'))]
    if not images:
        print("Error: No images found in mri_roi_dataset/images.")
        return

    test_image = os.path.join(img_dir, images[0])
    print(f"[RUNNING] Running prediction on: {test_image}")

    pred_idx, prob = predict_mri(test_image)
    
    classes = ["MildDemented", "ModerateDemented", "NonDemented", "VeryMildDemented"]
    
    if pred_idx != -1:
        print(f"Result: {classes[pred_idx]}")
        print(f"Confidence: {prob*100:.2f}%")
        print("--- Project is fully functional! ---")
    else:
        print("Error: Prediction failed.")

if __name__ == "__main__":
    run_test()
