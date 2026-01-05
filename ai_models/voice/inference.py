import torch
import numpy as np
import os
import sys
from pathlib import Path
import torch.nn.functional as F

# Ensure current directory is in path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from swin_model import SwinTransformer
from preprocess_audio import preprocess_audio
from utils import extract_mfcc

SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / 'best_model.pth'

def predict(audio_path):
    """
    Predicts whether the input audio indicates dementia using the stable Swin pipeline.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 1. Load Checkpoint
    if not MODEL_PATH.exists():
        print(f"Error: Model file {MODEL_PATH} not found.")
        return 0.5 # Return 0.5 as neutral fallback
        
    checkpoint = torch.load(MODEL_PATH, map_location=device)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model_state = checkpoint['model_state_dict']
        mean = checkpoint.get('mean', 0.0)
        std = checkpoint.get('std', 1.0)
        classes = checkpoint.get('classes', ['dementia', 'healthy'])
    else:
        model_state = checkpoint
        mean = 0.0
        std = 1.0
        classes = ['dementia', 'healthy']
    
    # 2. Preprocess and Generate MFCC (.npy)
    temp_npy = SCRIPT_DIR / "temp_inference.npy"
    temp_wav = SCRIPT_DIR / "temp_inference.wav"
    
    try:
        # Standardize audio (5s, 16kHz)
        preprocess_audio(audio_path, str(temp_wav))
        
        # Extract 3-channel features (MFCC, Delta, Delta2)
        extract_mfcc(str(temp_wav), str(temp_npy.with_suffix(""))) # extract_mfcc appends .npy
        
        # Load and Prepare Tensor
        mfcc_feat = np.load(str(temp_npy))
        mfcc_tensor = torch.from_numpy(mfcc_feat).float()
        
        # Resize to (224, 224) matching dataset.py logic
        mfcc_tensor = mfcc_tensor.unsqueeze(0) # (1, 3, 40, T)
        mfcc_tensor = F.interpolate(mfcc_tensor, size=(224, 224), mode="bilinear", align_corners=False)
        
        # Normalize with stored stats
        mfcc_tensor = (mfcc_tensor - mean) / (std + 1e-6)
        mfcc_tensor = mfcc_tensor.to(device)
        
        # 3. Load Model
        model = SwinTransformer(num_classes=len(classes), pretrained=False)
        model.load_state_dict(model_state)
        model.to(device)
        model.eval()
        
        # 4. Inference
        with torch.no_grad():
            outputs = model(mfcc_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        # Get index for 'dementia' class
        try:
            dementia_idx = classes.index('dementia')
        except ValueError:
            dementia_idx = 0 # Fallback
            
        dementia_prob = probabilities[0][dementia_idx].item()
        return dementia_prob

    except Exception as e:
        print(f"Inference failed: {e}")
        return 0.5
    finally:
        # Cleanup
        if temp_npy.exists():
            os.remove(temp_npy)
        if temp_wav.exists():
            os.remove(temp_wav)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        prob = predict(file_path)
        print(f"Dementia Probability: {prob:.4f}")
    else:
        print("Usage: python inference.py <path_to_audio_file>")
