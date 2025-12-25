import os
import sys

# Ensure current directory is in path for imports
sys.path.append(os.getcwd())

from preprocess_audio import preprocess_audio
from utils import extract_mfcc

RAW_DIR = "../../datasets/dementianet/raw_audio"
MFCC_DIR = "../../datasets/voice_mfcc"

LABELS = {
    "normal": "normal",
    "dementia": "dementia"
}

def main():
    os.makedirs(MFCC_DIR, exist_ok=True)

    print("Starting MFCC Dataset Building...")

    for label, folder_name in LABELS.items():
        input_dir = os.path.join(RAW_DIR, folder_name)
        output_dir = os.path.join(MFCC_DIR, label)
        os.makedirs(output_dir, exist_ok=True)
        
        if not os.path.exists(input_dir):
            print(f"Warning: Input directory not found: {input_dir}")
            continue

        # Get list of all files recursively
        all_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith((".wav", ".mp3")):
                    all_files.append(os.path.join(root, file))

        print(f"Processing {len(all_files)} files in {label}...")

        for input_audio in all_files:
            # Create a unique filename for the output to avoid collisions if multiple subdirs have same filenames
            # combining parent folder name with filename
            rel_path = os.path.relpath(input_audio, input_dir)
            # flatten path for filename: PersonName_file.wav
            filename_flat = rel_path.replace(os.path.sep, "_").replace("/", "_") 
            
            clean_audio = "temp.wav"
            output_mfcc = os.path.join(output_dir, filename_flat.rsplit('.', 1)[0] + ".png")

            try:
                preprocess_audio(input_audio, clean_audio)
                extract_mfcc(clean_audio, output_mfcc)
            except Exception as e:
                print(f"Failed to process {input_audio}: {e}")
            finally:
                if os.path.exists(clean_audio):
                    os.remove(clean_audio)

    print("MFCC dataset built successfully")

if __name__ == "__main__":
    main()
