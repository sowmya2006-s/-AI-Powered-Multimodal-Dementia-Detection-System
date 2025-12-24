import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def verify():
    print("--- VERIFICATION START ---")
    
    # 1. Check DB
    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        print(f"[OK] Database exists at: {db_path}")
    else:
        print(f"[FAIL] Database missing at: {db_path}")

    # 2. Check Media Dirs
    media_root = settings.MEDIA_ROOT
    voice_dir = os.path.join(media_root, 'voice')
    mfcc_dir = os.path.join(media_root, 'mfcc')
    
    if os.path.exists(voice_dir):
        print(f"[OK] Voice dir exists: {voice_dir}")
    else:
        print(f"[FAIL] Voice dir missing: {voice_dir}")
        
    if os.path.exists(mfcc_dir):
        print(f"[OK] MFCC dir exists: {mfcc_dir}")
    else:
        print(f"[FAIL] MFCC dir missing: {mfcc_dir}")

    # 3. Check Librosa
    try:
        import librosa
        print(f"[OK] Librosa imported version: {librosa.__version__}")
    except ImportError:
        print("[FAIL] Librosa not installed")

    print("--- VERIFICATION END ---")

if __name__ == "__main__":
    verify()
