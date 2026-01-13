import torch
import torch.nn.functional as F
from swin_model import SwinTransformer
import numpy as np
import os

def load_model(model_path, device):
    checkpoint = torch.load(model_path, map_location=device)
    classes = checkpoint['classes']
    model = SwinTransformer(num_classes=len(classes)).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model, checkpoint['mean'], checkpoint['std'], classes

def predict_ensemble(mfcc_tensor, model_paths, device):
    """
    🔹 STEP 4: Ensemble inference (BAGGING)
    p1 = softmax(model1(x))
    p2 = softmax(model2(x))
    p3 = softmax(model3(x))
    final_pred = (p1 + p2 + p3) / 3
    Final class = argmax(final_pred)
    """
    all_probs = []
    
    # We assume all models share the same classes and preprocessing logic for simplicity,
    # but we load mean/std from each checkpoint as saved in bagging_train.py
    
    with torch.no_grad():
        for m_path in model_paths:
            if not os.path.exists(m_path):
                print(f"Warning: Model {m_path} not found. Skipping.")
                continue
                
            model, mean, std, classes = load_model(m_path, device)
            
            # Normalize specific to this model's training stats
            img = (mfcc_tensor - mean) / (std + 1e-6)
            img = img.to(device)
            if img.dim() == 3:
                img = img.unsqueeze(0) # Add batch dim
            
            logits = model(img)
            probs = F.softmax(logits, dim=1)
            all_probs.append(probs.cpu().numpy())
            
    if not all_probs:
        return None, None
        
    # Average softmax probabilities
    avg_probs = np.mean(all_probs, axis=0)
    final_class_idx = np.argmax(avg_probs, axis=1)[0]
    
    # Get the class name using the last loaded classes (assuming they are identical)
    final_class_name = classes[final_class_idx]
    confidence = avg_probs[0][final_class_idx]
    
    return final_class_name, confidence

if __name__ == "__main__":
    # Example usage (requires swin_1.pth, swin_2.pth, swin_3.pth to exist)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_files = ['swin_1.pth', 'swin_2.pth', 'swin_3.pth']
    
    # For testing, we need an MFCC tensor. 
    # This is normally provided by the dataset or the preprocessing pipeline.
    print("Bagging Inference script ready. Use predict_ensemble() in your application pipeline.")
