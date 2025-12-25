import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import timm
import os

# ---------- CONFIG ----------
# Adjust path to be relative or absolute as needed. 
# Assuming this script is imported from Django context, 
# paths might need to be absolute or relative to project root.
# Using relative path assuming 'backend' is the root for django execution context or adjusting accordingly.
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "best_model.pth")
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------- MODEL ----------
def load_model():
    # Defining model structure matching training
    model = timm.create_model(
        "swin_tiny_patch4_window7_224",
        pretrained=False,
        num_classes=2
    )
    
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}")
        
    model.to(DEVICE)
    model.eval()
    return model

# Load model globally to avoid reloading on every request (efficiency)
# Note: In production, consider where this is loaded to avoid memory issues if multiple workers.
try:
    model = load_model()
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# ---------- TRANSFORM ----------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5]) # Matching user's requested logic
])

# ---------- PREDICT ----------
def predict_mfcc(mfcc_image_path):
    if model is None:
        raise RuntimeError("Model not loaded")

    if not os.path.exists(mfcc_image_path):
        raise FileNotFoundError(f"MFCC image not found at {mfcc_image_path}")

    try:
        image = Image.open(mfcc_image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(image)
            # Assuming outputs are raw logits. 
            # If model output was already softmaxed in training modification it would be different, 
            # but standard Swin from timm returns logits.
            probs = torch.softmax(outputs, dim=1)
            
            # Assuming class 1 is dementia based on "Dementia -> label 1" assumption in Step 7A
            dementia_prob = probs[0][1].item()

        return dementia_prob
    except Exception as e:
        print(f"Prediction error: {e}")
        return 0.0
