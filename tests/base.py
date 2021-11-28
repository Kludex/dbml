from typing import Any, Dict, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship


@as_declarative()
class Base:
    __name__: str

    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    items = relationship("Item", back_populates="owner", lazy="selectin")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")


from typing import List

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    full_name: str = Field(index=True)
    email: EmailStr = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    items: List["Items"] = Relationship(back_populates="owner")


class Items(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    owner_id: int = Field(default=None, foreign_key="users.id")
    owner: List["Users"] = Relationship(back_populates="items")
