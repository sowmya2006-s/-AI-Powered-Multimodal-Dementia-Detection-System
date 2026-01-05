import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_mfcc(input_path, output_path, sr=16000, n_mfcc=40):
    """
    Generates 3-channel MFCC features (MFCC, Delta, Delta2) and saves as a .npy file.
    """
    try:
        y, sr = librosa.load(input_path, sr=sr)
        
        # Extract features according to user requirements
        mfcc = librosa.feature.mfcc(
            y=y, 
            sr=sr, 
            n_mfcc=n_mfcc,
            n_fft=1024,
            hop_length=320
        )
        
        delta = librosa.feature.delta(mfcc)
        delta2 = librosa.feature.delta(mfcc, order=2)
        
        # Stack into 3 channels
        mfcc_feat = np.stack([mfcc, delta, delta2], axis=0) # (3, 40, T)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as numpy array
        np.save(output_path, mfcc_feat)
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
