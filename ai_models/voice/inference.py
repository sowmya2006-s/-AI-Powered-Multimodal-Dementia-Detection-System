import torch
from torchvision import transforms
from PIL import Image
import os
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from swin_model import SwinTransformer
from preprocess_audio import preprocess_audio
from utils import extract_mfcc

MODEL_PATH = 'best_model.pth'
CLASSES = ['dementia', 'normal'] # Ensure this matches training order

def predict(audio_path):
    """
    Predicts whether the input audio indicates dementia.
    Returns: Probability of dementia (float)
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 1. Preprocess and Generate MFCC
    temp_mfcc = "temp_inference.png"
    temp_wav = "temp_inference.wav"
    
    try:
        # Preprocess
        preprocess_audio(audio_path, temp_wav)
        extract_mfcc(temp_wav, temp_mfcc)
        
        # 2. Load Model
        model = SwinTransformer(num_classes=len(CLASSES), pretrained=False) # No need to download pretrained weights again if reloading state dict
        if os.path.exists(MODEL_PATH):
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        else:
            print(f"Warning: Model file {MODEL_PATH} not found. Using random weights.")
            
        model.to(device)
        model.eval()
        
        # 3. Transform Image
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        image = Image.open(temp_mfcc).convert('RGB')
        image = transform(image).unsqueeze(0).to(device)
        
        # 4. Inference
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        # Assuming index 0 is dementia (alphabetical order usually: dementia, normal)
        # Wait, sorted(['dementia', 'normal']) is ['dementia', 'normal']
        # So index 0 = dementia, index 1 = normal
        dementia_prob = probabilities[0][0].item()
        
        return dementia_prob

    except Exception as e:
        print(f"Inference failed: {e}")
        return 0.0
    finally:
        # Cleanup
        if os.path.exists(temp_mfcc):
            os.remove(temp_mfcc)
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        prob = predict(file_path)
        print(f"Dementia Probability: {prob:.4f}")
    else:
        print("Usage: python inference.py <path_to_audio_file>")
