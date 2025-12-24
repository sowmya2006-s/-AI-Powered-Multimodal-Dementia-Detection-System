# AI-Powered Multimodal Dementia Detection System - Backend

Django REST API backend for the dementia detection system.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
backend/
├── dementia_detection/     # Main project settings
├── accounts/               # User authentication
├── voice_analysis/         # Phase 1: Voice analysis
├── memory_game/            # Phase 2: Memory assessment
├── mri_analysis/           # Phase 3: MRI analysis
├── reports/                # Report generation
└── requirements.txt        # Python dependencies
```
