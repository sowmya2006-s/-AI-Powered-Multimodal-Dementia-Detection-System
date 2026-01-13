import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model

# Constants for inference
MODEL_PATH = "best_mri_swin.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Transforms (same as during training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    )
])

# Lazy load model
_model = None

def load_inference_model():
    global _model
    if _model is None:
        _model = get_model().to(DEVICE)
        if os.path.exists(MODEL_PATH):
            _model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
            _model.eval()
            print(f"Loaded MRI model from {MODEL_PATH}")
        else:
            print(f"Warning: Model file {MODEL_PATH} not found. Inference might fail.")
    return _model

def predict_mri(image_path):
    """
    Predicts the class and probability for an MRI image.
    Returns: (class_idx, probability)
    """
    model = load_inference_model()
    
    try:
        img = Image.open(image_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            out = model(img_tensor)
            probs = F.softmax(out, dim=1)
            prob, pred = torch.max(probs, 1)
            
            return pred.item(), prob.item()
    except Exception as e:
        print(f"Error during MRI inference: {e}")
        return -1, 0.0

if __name__ == "__main__":
    # Example usage (if an image exists)
    # test_image = "datasets/MRI_SPLIT/test/NonDemented/26 (100).jpg"
    # if os.path.exists(test_image):
    #     pred, prob = predict_mri(test_image)
    #     print(f"Prediction: {pred}, Probability: {prob:.4f}")
    pass
