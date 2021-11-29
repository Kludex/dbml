from sqlalchemy.sql.schema import ForeignKey
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

DBML_TO_SQLALCHEMY = {
    "boolean": Boolean,
    "date": Date,
    "datetime": DateTime,
    "int": Integer,
    "integer": Integer,
    "varchar": String,
    "binary": LargeBinary,
    "enum": Enum,
    "text": Text,
    "bigint": BigInteger,
    "time": Time,
}
