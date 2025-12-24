# AI Models Directory

This directory contains the trained machine learning models for the dementia detection system.

## Models

### 1. Voice Analysis Model (Swin Transformer)
- **File**: `swin_voice_model.pth`
- **Purpose**: Analyzes audio spectrograms for dementia detection
- **Input**: MFCC features from voice recordings
- **Output**: Dementia risk score (0-100) + confidence

### 2. MRI Analysis Model (Swin Transformer)
- **File**: `swin_mri_model.pth`
- **Purpose**: Analyzes brain MRI scans for structural abnormalities
- **Input**: Preprocessed MRI image patches
- **Output**: Classification (No Dementia/MCI/Dementia) + severity

## Training Scripts

Training scripts are located in:
- `backend/voice_analysis/train_voice_model.py`
- `backend/mri_analysis/train_mri_model.py`

## Model Storage

In production, models should be stored in AWS S3 and loaded on-demand to reduce server memory usage.

## Pretrained Models

Download pretrained Swin Transformer weights from:
- https://github.com/microsoft/Swin-Transformer

## Note

Model files (*.pth, *.pt) are excluded from git via .gitignore due to their large size.
