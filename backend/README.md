# NailArt Backend

## Requirements
- Python 3.11+
- Redis (local or via Docker)

## Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Start Redis
```bash
docker-compose up -d
```
Or run local Redis:
```bash
redis-server
```

## Initialize Database
```bash
python -m app.db.init_db
```

## Start API
```bash
uvicorn app.main:app --reload --port 8000
```

## Start Worker
```bash
python -m app.workers.worker
# or
rq worker -u redis://localhost:6379/0 nail_jobs
```

## API
- `GET /v1/health`
- `POST /v1/extract` (form-data `file`)
- `POST /v1/tryon` (form-data `file`, `asset_id`)
- `GET /v1/jobs/{job_id}`
- `POST /v1/assets`
- `GET /v1/assets`
- `GET /v1/assets/{asset_id}`
