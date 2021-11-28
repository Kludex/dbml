from pathlib import Path
from typing import Dict, Iterator, List, Literal, Optional, TypedDict

from rich.console import Console
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DATETIME, BigInteger, Boolean, Date, DateTime, Enum
from sqlalchemy.sql.sqltypes import Integer, LargeBinary, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import Time
from sqlmodel.sql.sqltypes import AutoString

SQLALCHEMY_TO_DBML = {
    Boolean: "boolean",
    Date: "date",
    DateTime: "datetime",
    Integer: "int",
    String: "varchar",
    SmallInteger: "int",  # Is there a different one here?
    LargeBinary: "binary",
    Enum: "enum",
    Time: "time",
    Text: "text",
    ForeignKey: "foreign_key",
    BigInteger: "bigint",
    DATETIME: "datetime",
    AutoString: "varchar",
}


class FieldInfo(TypedDict):
    type: str
    pk: bool
    unique: Optional[bool]
    nullable: bool


class RelationshipInfo(TypedDict):
    type: Literal["1-1", "1-n", "n-n"]
    table_from: str
    table_from_field: str
    table_to: str
    table_to_field: str


class TableInfo(TypedDict):
    fields: Dict[str, FieldInfo]
    relationships: List[RelationshipInfo]


def generate_dbml_file(tables: Iterator[Table], output: Optional[Path]) -> None:
    tables_info = {}
    for table in tables:
        try:
            tables_info[table.name] = extract_table_info(table)
        except TypeError as exc:
            std_console = Console()
            std_console.print(
                f"{exc.args[0]} is not supported.",
                "Please fill an issue on https://github.com/Kludex/sqlalchemy-dbml.",
            )
            raise SystemExit(1)

    file = output.open("w") if output else None
    console = Console(file=file)

    for num, (table_name, info) in enumerate(tables_info.items()):
        console.print("[blue]Table", f"{table_name}", "[bold white]{")
        for name, field in info["fields"].items():
            attrs = get_attrs_from_field(field)
            output = [f"  {name}", f'[orange4]{field["type"]}']
            if attrs:
                output.append(attrs)
            console.print(*output)
        console.print("[bold white]}", end="\n")

        if info["relationships"]:
            console.print()

        for relation in info["relationships"]:
            # One to Many
            console.print(
                "[blue]Ref:",
                f"{relation['table_from']}.{relation['table_from_field']}",
                "[green]>",
                f"{relation['table_to']}.{relation['table_to_field']}",
            )
        if num < len(tables_info) - 1:
            console.print()

    if file:
        file.close()


def extract_table_info(table: Table) -> TableInfo:
    table_info = TableInfo(fields={}, relationships=[])

    for column in table.columns:
        column_type = type(column.type)
        if column_type not in SQLALCHEMY_TO_DBML:
            raise TypeError(type(column.type))
        table_info["fields"][column.name] = {
            "type": SQLALCHEMY_TO_DBML[column_type],
            "pk": column.primary_key,
            "unique": column.unique,
            "nullable": column.nullable,
        }
        for foreign_key in column.foreign_keys:
            table_info["relationships"].append(
                RelationshipInfo(
                    table_from=table.name,
                    table_to=foreign_key.column.table.name,
                    table_from_field=column.name,
                    table_to_field=foreign_key.column.name,
                )
            )
    return table_info


def get_attrs_from_field(field: FieldInfo) -> str:
    attrs = []
    if field["pk"]:
        attrs.append("pk")
    if field["unique"]:
        attrs.append("unique")
    if field["nullable"] is False:
        attrs.append("not null")
    if not attrs:
        return ""
    return "\\[{}]".format(", ".join(attrs))
