import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_mfcc(input_path, output_path, sr=22050, n_mfcc=13):
    """
    Generates an MFCC spectrogram from an audio file and saves it as an image.
    """
    try:
        y, sr = librosa.load(input_path, sr=sr)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.axis('off')  # Turn off axes for raw image data
        plt.tight_layout(pad=0)
        
        # Create directory if it doesn't exist (just in case)
        if os.path.dirname(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        # print(f"Generated MFCC: {output_path}")
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
