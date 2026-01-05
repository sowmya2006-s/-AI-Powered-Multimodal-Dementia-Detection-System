# Phase 1: Audio-Based Dementia Detection - Implementation Guide

## Overview
This guide documents the setup and usage of the Phase 1 audio detection system, including dataset preparation, training, and testing.

## 1. Dataset Structure
The system expects the following directory structure (automatically handled by scripts):
`datasets/dementianet/raw_audio/` -> Contains original audio files.
`datasets/dementianet/train/` & `test/` -> Split raw audio files.
`datasets/voice_mfcc/train/` & `test/` -> Generated MFCC spectrograms (images).

## 2. Scripts
### `split_data.py`
**Purpose**: Splits raw audio into training and testing sets (80/20 split).
**Usage**:
```bash
python split_data.py
```
**Output**: 
- `datasets/dementianet/train`
- `datasets/dementianet/test`

### `build_mfcc_dataset.py`
**Purpose**: Converts audio files into MFCC images for the Swin Transformer.
**Usage**:
```bash
python build_mfcc_dataset.py
```
**Output**:
- `datasets/voice_mfcc/train`
- `datasets/voice_mfcc/test`

### `train.py`
**Purpose**: Trains the model and logs accuracy.
**Logging**: Prints `Train Acc` and `Val Acc` per epoch as required.
**Usage**:
```bash
python train.py
```

### `test_audio.py`
**Purpose**: strict testing script to calculate final accuracy on unseen data.
**Usage**:
```bash
python test_audio.py
```
**Output**: 
```
Test Accuracy: 85.00%
```

## 3. Backend Integration
### Endpoints
1. **Phase 1 (Inference)**: `POST /api/voice/upload/`
   - Uploads audio, runs MFCC conversion, runs inference.
   - **Response**:
     ```json
     {
       "probability": 0.78,
       "risk_level": "HIGH"
     }
     ```

2. **Phase 2 (Simplified Storage)**: `POST /api/voice/store/`
   - Uploads audio for simple storage (Data Intake).
   - **Response**:
     ```json
     {
       "status": "stored",
       "message": "Audio stored successfully..."
     }
     ```

## Verification Checklist
- [x] Dataset Split (`split_data.py`)
- [x] MFCC Generation (`build_mfcc_dataset.py`)
- [x] Training Logic (`train.py`)
- [x] Testing Logic (`test_audio.py`)
- [x] Backend JSON Response Format
