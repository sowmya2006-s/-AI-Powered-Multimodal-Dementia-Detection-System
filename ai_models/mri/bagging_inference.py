import torch
import torch.nn.functional as F
import os
import sys
import numpy as np
from PIL import Image

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.model import get_model
from ai_models.mri.dataset import transform

def load_model_mri(model_path, device):
    checkpoint = torch.load(model_path, map_location=device)
    num_classes = checkpoint.get('num_classes', 4)
    model = get_model(num_classes=num_classes).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model, checkpoint['classes']

def predict_mri_ensemble(image_path):
    """
    Ensemble inference for MRI using 3 bagged Swin Transformer models.
    Returns: final_class_name, confidence_score
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_dir = os.path.dirname(os.path.abspath(__file__))
    model_paths = [
        os.path.join(model_dir, 'swin_mri_1.pth'),
        os.path.join(project_root, 'best_model.pth'),  # Fallback to root model
        os.path.join(model_dir, 'swin_mri_v1.pth'),  # Possible alternative name
    ]

    # Preprocess image
    try:
        img = Image.open(image_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(device)
    except Exception as e:
        print(f"Error opening image: {e}")
        return None, 0.0

    all_probs = []
    classes = None

    with torch.no_grad():
        for m_path in model_paths:
            if not os.path.exists(m_path):
                print(f"Warning: MRI Model {m_path} not found. Skipping.")
                continue
            
            model, current_classes = load_model_mri(m_path, device)
            classes = current_classes # Assuming classes are identical across models
            
            logits = model(img_tensor)
            probs = F.softmax(logits, dim=1)
            all_probs.append(probs.cpu().numpy())

    if not all_probs:
        print("Error: No MRI models available for inference.")
        return "Unknown", 0.0

    # Average probabilities across the ensemble
    avg_probs = np.mean(all_probs, axis=0)
    final_class_idx = np.argmax(avg_probs, axis=1)[0]
    
    final_class_name = classes[final_class_idx]
    confidence = avg_probs[0][final_class_idx]

    return final_class_name, float(confidence)

if __name__ == "__main__":
    # Example usage
    # if len(sys.argv) > 1:
    #     res, conf = predict_mri_ensemble(sys.argv[1])
    #     print(f"Result: {res} ({conf*100:.1f}%)")
    pass
