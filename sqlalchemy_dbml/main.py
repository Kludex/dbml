from pathlib import Path
from typing import Optional

from sqlalchemy import MetaData
from typer import Argument, Option, Typer

from sqlalchemy_dbml.generate_dbml import generate_dbml_file
from sqlalchemy_dbml.importer import import_from_string

app = Typer()


@app.command()
def generate_dbml(
    path: str = Argument(
        ..., help="Path to import the base class, must be in format '<module>:<attr>'."
    ),
    output: Optional[Path] = Option(None),
) -> None:
    """Generate DBML output from SQLAlchemy models."""
    base = import_from_string(path)
    metadata: MetaData = getattr(base, "metadata")
    tables = metadata.tables.values()

    generate_dbml_file(tables, output)
