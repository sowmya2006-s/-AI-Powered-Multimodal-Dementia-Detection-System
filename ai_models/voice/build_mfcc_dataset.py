import os
import sys
from pathlib import Path

# Ensure current directory is in path for imports
sys.path.append(os.getcwd())

from preprocess_audio import preprocess_audio
from utils import extract_mfcc

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RAW_ROOT = PROJECT_ROOT / "datasets" / "dementianet"
MFCC_ROOT = PROJECT_ROOT / "datasets" / "voice_mfcc"

SPLITS = ["train_audio", "val_audio", "test_audio"]
CLASSES = ["dementia", "healthy"]

def main():
    print("Starting MFCC Dataset Building...")

    for split in SPLITS:
        # Determine target split name (e.g., train_audio -> train)
        target_split = split.split('_')[0]
        
        for class_name in CLASSES:
            input_dir = RAW_ROOT / split / class_name
            output_dir = MFCC_ROOT / target_split / class_name
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if not input_dir.exists():
                print(f"Warning: Input directory not found: {input_dir}")
                continue

            all_files = list(input_dir.glob("*.wav"))

            print(f"Processing {split}/{class_name} -> {target_split}: {len(all_files)} files...")

            for input_audio in all_files:
                output_mfcc = output_dir / (input_audio.stem + ".npy")
                
                clean_audio = "temp.wav"

                try:
                    preprocess_audio(str(input_audio), clean_audio)
                    extract_mfcc(clean_audio, str(output_mfcc))
                except Exception as e:
                    print(f"Failed to process {input_audio}: {e}")
                finally:
                    if os.path.exists(clean_audio):
                        try:
                            os.remove(clean_audio)
                        except:
                            pass

    print("MFCC dataset built successfully")

if __name__ == "__main__":
    main()
