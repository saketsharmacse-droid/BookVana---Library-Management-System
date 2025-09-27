# BookVana Deployment and DB Fix TODO

## Current Work
Fixing deployment issues (503 error) and database persistence/fetching problems on Render by switching to gunicorn, proper host/port binding, and migrating from ephemeral SQLite to persistent PostgreSQL.

## Key Technical Concepts
- Flask app configuration for production (gunicorn WSGI server).
- Database migration: SQLite (local/ephemeral) to PostgreSQL (persistent via Render's DATABASE_URL).
- Environment variables: Use os.environ for PORT, DATABASE_URL, FLASK_DEBUG.
- psycopg2 for Postgres connections; fallback to SQLite for local dev.
- SQL queries: Mostly compatible, but handle timestamp parsing and sample data insertion idempotently (check if empty before insert).

## Relevant Files and Code
- requirements.txt: Add psycopg2-binary for Postgres support.
- render.yaml: Update startCommand to use gunicorn, remove fixed PORT.
- app.py: 
  - Add get_db() function for dynamic connection (Postgres if DATABASE_URL, else SQLite).
  - Update init_db to use get_db(), check table counts before inserting samples.
  - Replace all sqlite3.connect with get_db() and adjust cursor/conn usage for psycopg2.
  - Conditional app.run for local dev only, with proper host/port/debug.
- No changes to templates/static as they are fine.

## Problem Solving
- 503 Error: Dev server doesn't bind to 0.0.0.0:PORT; fixed with gunicorn.
- DB Fetching/Persistence: SQLite file resets on Render; fixed with Postgres.
- Sample Data: Insert only if tables empty to avoid duplicates.
- Timestamp Handling: Ensure due_date parsing works with Postgres output.

## Pending Tasks and Next Steps
1. [x] Update requirements.txt: Add `psycopg2-binary==2.9.9`.
2. [x] Update render.yaml: Set startCommand to `"gunicorn app:app --bind 0.0.0.0:$PORT"`, remove fixed PORT envVar, keep FLASK_ENV=production and FLASK_DEBUG=false.
3. [x] Update app.py: Implement get_db(), update init_db and all API routes/DB functions to use it, adjust app.run for production/local.
4. [ ] User actions: Add free Postgres database on Render dashboard, link to service (auto-sets DATABASE_URL), commit/push changes to trigger redeploy.
5. [ ] Test: Launch browser to verify site loads (no 503), data persists (add book, refresh), check console for errors.
6. [x] Update this TODO.md after each step completion.

"User confirmed: yes do the edits"
