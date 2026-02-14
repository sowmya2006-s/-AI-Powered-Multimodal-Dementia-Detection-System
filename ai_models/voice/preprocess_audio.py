import librosa
import soundfile as sf
import os
import numpy as np

TARGET_SR = 16000
TARGET_DURATION = 5 # seconds
TARGET_LEN = TARGET_SR * TARGET_DURATION

def preprocess_audio(input_path, output_path):
    try:
        y, sr = librosa.load(input_path, sr=TARGET_SR)
        
        # Trim silence
        y, _ = librosa.effects.trim(y)
        
        # Enforce duration (pad or truncate)
        if len(y) < TARGET_LEN:
            y = np.pad(y, (0, TARGET_LEN - len(y)))
        else:
            y = y[:TARGET_LEN]
            
        sf.write(output_path, y, TARGET_SR)
    except Exception as e:
        print(f"Error preprocessing {input_path}: {e}")
