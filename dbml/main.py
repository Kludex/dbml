from pathlib import Path
from typing import Optional, cast

from pydbml import PyDBML
from rich.console import Console
from sqlalchemy import MetaData
from typer import Argument, Option, Typer

from dbml.generate_dbml import generate_dbml_file
from dbml.generate_models import generate_sqlalchemy_models
from dbml.importer import import_from_string

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


@app.command()
def generate_models(
    path: Path = Argument(..., exists=True), output: Optional[Path] = Option(None)
) -> None:
    """Generate SQLAlchemy models from DBML."""
    console = Console(file=output if output is None else output.open("w"))
    dbml = PyDBML(path)
    content = generate_sqlalchemy_models(dbml)

    for line in content:
        console.print(line)

    if output is not None:
        output.close()
