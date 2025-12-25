# AI-Powered Multimodal Dementia Detection System

An AI-powered system that combines voice analysis, cognitive memory games, and conditional MRI scan analysis to provide early, accurate, and cost-effective dementia diagnosis.

## 🎯 Project Overview

This system helps detect dementia through three phases:

1. **Phase 1: Voice Analysis** - Analyzes speech patterns using MFCC and Swin Transformer
2. **Phase 2: Memory Assessment** - Cognitive games (visual/auditory) to test memory retention
3. **Phase 3: MRI Analysis** (Conditional) - Brain scan analysis only if needed based on Phase 1 & 2 results

### Cost-Saving Approach

The system generates a **preliminary report** after Phase 1 & 2, allowing patients to decide if they can afford the expensive MRI scan (Phase 3) based on their risk level.

## 📋 Prerequisites

- Python 3.9 or 3.10
- Node.js 18+
- PostgreSQL 15+
- Git

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd -AI-Powered-Multimodal-Dementia-Detection-System
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### 4. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## 📁 Project Structure

```
-AI-Powered-Multimodal-Dementia-Detection-System/
├── backend/              # Django REST API
│   ├── dementia_detection/  # Main settings
│   ├── accounts/            # Authentication
│   ├── voice_analysis/      # Phase 1
│   ├── memory_game/         # Phase 2
│   ├── mri_analysis/        # Phase 3
│   └── reports/             # Report generation
├── frontend/             # Next.js application
│   └── src/
│       ├── app/         # Next.js 14 App Router
│       └── components/  # React components
├── ai_models/           # Trained ML models
├── datasets/            # Training datasets
└── docs/                # Documentation
```

## 🛠️ Tech Stack

### Backend
- Django 4.2 + Django REST Framework
- PostgreSQL
- AWS S3 (file storage)
- PyTorch + Swin Transformer
- Librosa (audio processing)

### Frontend
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS + Material-UI
- TanStack Query
- Web Audio API

## 📊 System Flow

1. Patient registers and provides information
2. Completes Phase 1: Voice recording and analysis
3. Completes Phase 2: Memory game (visual or auditory)
4. System generates **preliminary report** with MRI recommendation
5. Patient decides whether to proceed to Phase 3 (MRI)
6. If MRI completed, system generates **final comprehensive report**

## Phase 1: Voice-Based Dementia Detection

- Dataset: DementiaNet
- Feature Extraction: MFCC Spectrograms
- Model: Swin Transformer
- Output: Dementia Probability + Risk Level
- Status: ✅ Completed

## 🔒 Security

- JWT authentication
- HTTPS in production
- Environment variables for sensitive data
- CORS configuration
- Input validation and sanitization

## 📝 License

[Add your license here]

## 👥 Contributors

[Add contributors here]

## 📧 Contact

[Add contact information here]