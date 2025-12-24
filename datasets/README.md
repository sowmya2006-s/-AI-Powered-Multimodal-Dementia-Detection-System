# Datasets Directory

This directory contains the datasets used for training and testing the dementia detection models.

## Required Datasets

### 1. Voice Dataset (DementiaNet)
- **Source**: https://github.com/shreyasgite/dementianet
- **Description**: Voice recordings from dementia patients and healthy controls
- **Structure**:
  ```
  datasets/voice/
  ├── dementia/
  └── normal/
  ```

### 2. MRI Dataset
- **Source**: https://www.kaggle.com/datasets/shashwatwork/dementia-prediction
- **Description**: Brain MRI scans with dementia classifications
- **Structure**:
  ```
  datasets/mri/
  ├── no_dementia/
  ├── mild_dementia/
  ├── moderate_dementia/
  └── severe_dementia/
  ```

## Dataset Preparation

1. Download datasets from the sources above
2. Extract to respective directories
3. Run preprocessing scripts:
   ```bash
   python backend/voice_analysis/preprocess_audio.py
   python backend/mri_analysis/preprocess_mri.py
   ```

## Data Split

- Training: 70%
- Validation: 15%
- Testing: 15%

## Note

Dataset files are excluded from git via .gitignore due to their large size.
Store datasets locally or in cloud storage (AWS S3) for production.
