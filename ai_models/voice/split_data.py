import os
import shutil
import random
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BASE_DIR = PROJECT_ROOT / "datasets" / "dementianet"
RAW_AUDIO_DIR = BASE_DIR / "raw_audio"
TRAIN_DIR = BASE_DIR / "train_audio" # Using _audio to distinguish from preprocessed
VAL_DIR = BASE_DIR / "val_audio"
TEST_DIR = BASE_DIR / "test_audio"

# Class mapping (source_name -> target_name)
CLASS_MAPPING = {
    "dementia": "dementia",
    "normal": "healthy",  # Rename normal to healthy
    "healthy": "healthy"
}

TRAIN_SPLIT = 0.70
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

def setup_dirs():
    for d in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
        for target_class in set(CLASS_MAPPING.values()):
            (d / target_class).mkdir(exist_ok=True)

def split_data():
    setup_dirs()
    random.seed(RANDOM_SEED)

    for source_dir_name, target_class in CLASS_MAPPING.items():
        source_path = RAW_AUDIO_DIR / source_dir_name
        if not source_path.exists():
            continue
            
        # Get all speaker subdirectories
        speakers = [d for d in source_path.iterdir() if d.is_dir()]
        random.shuffle(speakers)
        
        num_speakers = len(speakers)
        train_idx = int(num_speakers * TRAIN_SPLIT)
        val_idx = train_idx + int(num_speakers * VAL_SPLIT)
        
        train_speakers = speakers[:train_idx]
        val_speakers = speakers[train_idx:val_idx]
        test_speakers = speakers[val_idx:]
        
        print(f"Processing '{source_dir_name}' -> '{target_class}': {len(train_speakers)} train, {len(val_speakers)} val, {len(test_speakers)} test speakers")
        
        def copy_speaker_files(speaker_dirs, dest_root):
            for speaker_dir in speaker_dirs:
                # Add speaker name to flat filename to keep it unique
                speaker_name = speaker_dir.name.replace(" ", "_")
                for audio_file in speaker_dir.glob("*.wav"):
                    flat_name = f"{speaker_name}_{audio_file.name}"
                    shutil.copy2(audio_file, dest_root / target_class / flat_name)

        copy_speaker_files(train_speakers, TRAIN_DIR)
        copy_speaker_files(val_speakers, VAL_DIR)
        copy_speaker_files(test_speakers, TEST_DIR)

    print("Data split complete.")

if __name__ == "__main__":
    split_data()
