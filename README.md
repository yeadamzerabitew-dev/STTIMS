# STTIMS - Short-Term Training Institution Management System

Web-based training institution management system (trainees, instructors,
courses, batches, enrollments, attendance, assessments, and certificates).

## Structure
- `backend/`  - Flask + SQLAlchemy REST API (MySQL)
- `frontend/` - Static HTML/JS/Bootstrap dashboard consuming the API

## Backend setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your real DB credentials
python run.py
```

## Frontend setup
Serve `frontend/` with any static file server (e.g. `python3 -m http.server`)
and open `index.html`. It expects the API at the URL configured in
`frontend/js/api.js`.
