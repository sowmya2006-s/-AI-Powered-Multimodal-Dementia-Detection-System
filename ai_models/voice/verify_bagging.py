import torch
import torch.nn.functional as F
import numpy as np
import os
from bagging_inference import load_model, predict_ensemble
from dataset import get_dataloader
from sklearn.metrics import accuracy_score, f1_score

def verify_bagging():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_files = ['swin_1.pth', 'swin_2.pth', 'swin_3.pth']
    single_model_file = 'best_model.pth'
    
    # Check if files exist
    all_exist = all(os.path.exists(f) for f in model_files + [single_model_file])
    if not all_exist:
        print("❌ Error: Some model files are missing. Please run training first.")
        missing = [f for f in model_files + [single_model_file] if not os.path.exists(f)]
        print(f"Missing: {missing}")
        return

    # Load Data for testing
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'datasets', 'voice_mfcc', 'val')
    test_loader, classes = get_dataloader(data_dir, batch_size=1, shuffle=False)
    
    if test_loader is None:
        print("❌ Error: Validation dataset not found.")
        return

    print("\n--- 1.1 Check diversity between models ---")
    # Take one sample
    sample_img, sample_label = next(iter(test_loader))
    
    individual_preds = []
    for m_path in model_files:
        model, mean, std, _ = load_model(m_path, device)
        img = (sample_img - mean) / (std + 1e-6)
        with torch.no_grad():
            logits = model(img.to(device))
            prob = F.softmax(logits, dim=1).cpu().numpy()
            pred_idx = np.argmax(prob)
            individual_preds.append((classes[pred_idx], np.max(prob)))
            print(f"Model {m_path}: {classes[pred_idx]} ({np.max(prob):.4f})")
            
    ensemble_class, ensemble_conf = predict_ensemble(sample_img, model_files, device)
    print(f"Ensemble: {ensemble_class} ({ensemble_conf:.4f})")
    
    # Diversity check: if they differ, it's good. 
    unique_preds = set(p[0] for p in individual_preds)
    if len(unique_preds) > 1:
        print("✔ Diversity detected! Bagging is doing something meaningful.")
    else:
        print("⚠ All models predicted the same class for this sample. (This can happen, try more samples if needed)")

    print("\n--- 1.2 Compare metrics (MANDATORY) ---")
    all_labels = []
    single_preds = []
    bagged_preds = []
    
    # Evaluation on a subset or full val set
    limit = 50 # Limit for speed
    print(f"Evaluating on {limit} samples...")
    
    for i, (img, label) in enumerate(test_loader):
        if i >= limit: break
        all_labels.append(label.item())
        
        # Single Model Prediction
        m, mean, std, _ = load_model(single_model_file, device)
        norm_img = (img - mean) / (std + 1e-6)
        with torch.no_grad():
            logits = m(norm_img.to(device))
            single_preds.append(torch.argmax(logits).item())
            
        # Bagged Model Prediction
        b_class, _ = predict_ensemble(img, model_files, device)
        bagged_preds.append(classes.index(b_class))
        
    single_acc = accuracy_score(all_labels, single_preds)
    single_f1 = f1_score(all_labels, single_preds, average='weighted', zero_division=0)
    
    bagged_acc = accuracy_score(all_labels, bagged_preds)
    bagged_f1 = f1_score(all_labels, bagged_preds, average='weighted', zero_division=0)
    
    print(f"{'Model':<20} | {'Accuracy':<10} | {'F1':<10}")
    print("-" * 45)
    print(f"{'Single Swin':<20} | {single_acc:.2%} | {single_f1:.2f}")
    print(f"{'Bagged Swin (3x)':<20} | {bagged_acc:.2%} | {bagged_f1:.2f}")

    print("\n--- 1.3 Stability test ---")
    print("Running inference 3 times on the same audio...")
    stability_preds = []
    for i in range(3):
        res_class, _ = predict_ensemble(sample_img, model_files, device)
        stability_preds.append(res_class)
        print(f"Run {i+1}: {res_class}")
        
    if len(set(stability_preds)) == 1:
        print("✔ Prediction is stable across runs.")
    else:
        print("❌ ERROR: Output flips randomly! Check for non-deterministic behavior.")

if __name__ == "__main__":
    verify_bagging()
