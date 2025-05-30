import typer
from sqlalchemy import create_engine
from src.schemas import Base

app = typer.Typer()

DATABASE_URL = "sqlite:///app.db"


@app.command()
def init_db():
    """Cria as tabelas no banco de dados."""
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    typer.echo("Tabelas criadas com sucesso no banco de dados SQLite.")


if __name__ == "__main__":
    app()
