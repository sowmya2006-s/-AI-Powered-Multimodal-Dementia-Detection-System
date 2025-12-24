import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend

def extract_mfcc(audio_path, output_path):
    y, sr = librosa.load(audio_path, sr=22050)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc = librosa.util.normalize(mfcc)

    plt.figure(figsize=(4, 4))
    librosa.display.specshow(mfcc, sr=sr, x_axis='time')
    plt.axis('off')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return output_path
