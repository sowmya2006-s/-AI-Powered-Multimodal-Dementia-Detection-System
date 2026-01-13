import torch
from sklearn.metrics import classification_report, confusion_matrix
import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai_models.mri.dataset import get_loaders
from ai_models.mri.model import get_model

def test_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    base_dir = os.path.join("datasets", "MRI_SPLIT")
    _, _, test_loader = get_loaders(base_dir)

    model = get_model().to(device)
    model_path = "best_mri_swin.pth"
    
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} not found. Please train the model first.")
        return

    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    y_true, y_pred = [], []

    with torch.no_grad():
        for x, y in test_loader:
            x = x.to(device)
            preds = model(x).argmax(1).cpu()
            y_true.extend(y.tolist())
            y_pred.extend(preds.tolist())

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["NonDemented", "Demented"]))

if __name__ == "__main__":
    test_model()
