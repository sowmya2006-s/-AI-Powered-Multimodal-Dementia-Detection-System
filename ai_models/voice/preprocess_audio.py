import librosa
import soundfile as sf
import os

TARGET_SR = 22050

def preprocess_audio(input_path, output_path):
    try:
        y, sr = librosa.load(input_path, sr=TARGET_SR)
        y, _ = librosa.effects.trim(y)
        sf.write(output_path, y, TARGET_SR)
    except Exception as e:
        print(f"Error preprocessing {input_path}: {e}")
