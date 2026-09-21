# E-Waste Advisor

An AI-assisted decision-support system for e-waste classification, visible-condition assessment, safe disposal guidance, and recycler discovery. This is **not** a certified inspection or an official recycler-authorisation service.

## Phase 1 implemented

- FastAPI API with interactive documentation at `/docs` and `/redoc`
- Replaceable multi-agent workflow and explicit `LocationAgent`
- Validated image-upload endpoint with a safe local fallback
- Haversine distance, recycler filtering, ranking, and demo-data safeguards
- CSV repository with only clearly labelled **DEMO DATA** records
- Backend unit tests

## Start the backend (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. Copy `.env.example` to `.env` before configuring real integrations.

## PostgreSQL / pgAdmin setup and user accounts

The application now stores registered users and their hashed passwords in PostgreSQL. It creates the `users` and `user_sessions` tables automatically when the API starts.

1. In pgAdmin, connect to your local PostgreSQL server, right-click **Databases**, and create a database named `ewaste_advisor`.
2. Copy `.env.example` to `backend/.env` and set `DATABASE_URL` to your local credentials. For example:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/ewaste_advisor
SECRET_KEY=replace-with-a-long-random-value
```

3. Install the updated backend requirements, then start the API. On first connection it creates the tables; refresh pgAdmin's **Schemas → public → Tables** to see them.
4. Open the site and select **Sign in → Create an account**. Use an email address and a password of at least eight characters. Login sessions expire after 24 hours by default.

If PostgreSQL is unavailable, core e-waste features continue to work and the login form displays setup guidance instead of storing credentials.

## API quick check

`GET /api/health` returns service health. `GET /api/recyclers/nearby?latitude=17.385&longitude=78.4867` demonstrates ranking with demo data.

## Responsible AI and data

The local starter intentionally does not claim it can see internal damage or infer chemical composition. A production vision provider, PostgreSQL/PostGIS repository, and authoritative recycler import are planned for the subsequent phases.
