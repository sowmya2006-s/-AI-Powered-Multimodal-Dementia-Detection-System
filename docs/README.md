# Documentation

This directory contains project documentation.

## Contents

- **API Documentation**: API endpoint specifications
- **Database Schema**: Database design and relationships
- **Architecture**: System architecture diagrams
- **User Guide**: End-user documentation
- **Developer Guide**: Setup and development instructions

## Generating API Docs

The backend uses `drf-spectacular` for automatic API documentation:

```bash
cd backend
python manage.py spectacular --file ../docs/api-schema.yml
```

Access interactive API docs at: http://localhost:8000/api/schema/swagger-ui/
