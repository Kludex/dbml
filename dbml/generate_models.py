from pathlib import Path
from typing import Optional, cast

from pydbml.classes import Column, Table
from pydbml.parser import PyDBML
from rich.pretty import pprint


def generate_sqlalchemy_models(dbml: PyDBML) -> None:
    imports = ["sqlalchemy.ext.declarative.declarative_base"]
    for table in dbml:
        table = cast(Table, table)
        pprint(table.refs)
        for column in table:
            column = cast(Column, column)
            pprint(column.ref_blueprints)
            # pprint(i.dbml)

    return []
