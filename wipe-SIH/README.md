# WipeChain

A secure data wiping and verification system with a modern, polished UI and simulated device workflow.

## Tech Stack

- Frontend: React + Vite + TailwindCSS + ShadCN-inspired components + Framer Motion + Lucide Icons
- Backend: FastAPI (Python) + SQLAlchemy + JWT auth + ReportLab PDF
- Database: PostgreSQL
- Docker: Docker Compose dev environment with hot reload

## Quick Start (Docker)

1. Prerequisites: Docker, Docker Compose
2. Run:
   ```bash
   docker compose up --build
   ```
3. Open the app:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000/docs

Login with:
- Email: `demo@wipechain.dev`
- Password: `demo1234`

## Features

- JWT authentication (signup/login)
- Device simulator: scan → choose wipe method → start wipe (simulated) → verify → certificate (PDF)
- Logs: history table with statuses and certificate downloads
- Analytics: pie chart of wipe methods
- Modern UI: glassmorphism, soft shadows, gradients, dark/light modes, smooth animations
- Seed data for immediate demo

## Development

Frontend:
```bash
cd frontend
npm i
npm run dev
```

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set environment variables for backend (defaults work with Docker):
```
DATABASE_URL=postgresql+psycopg2://wipechain:wipechain@localhost:5432/wipechain
JWT_SECRET_KEY=supersecretkeychangeinprod
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
CORS_ORIGINS=http://localhost:5173
```

## API Endpoints

- Auth: POST `/auth/signup`, POST `/auth/login`
- Devices: POST `/devices/scan`
- Wipes:
  - POST `/wipes/start` { device_uid, method }
  - POST `/wipes/verify` { wipe_id }
  - GET `/wipes`
- Certificates: GET `/certificates/{wipe_id}.pdf`

## Notes

- The wipe process and AI verification are simulated for prototyping purposes.
- PDF certificate is generated on demand and streamed by the backend.