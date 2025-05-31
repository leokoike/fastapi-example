run:
	uv run uvicorn src.main:app --reload

create-db:
	uv run python cli.py

populate-db:
	sqlite3 app.db < populate-user.sql
	sqlite3 app.db < populate-tvshows.sql
	sqlite3 app.db < populate-user-tvshow.sql