from datetime import date, timedelta, datetime
from pydantic import BaseModel, Field, BeforeValidator, EmailStr
from pydantic_settings import SettingsConfigDict
from typing import Optional, Annotated, TypeAlias, List
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField, JSON

from app.constants import StatusEnum


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    user_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str

    model_config = SettingsConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty"
            }
        })


class UserCredentials(BaseModel):
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "querty"
            }
        })


def _empty_str_or_none(value: str | None) -> None:
    if value is None or value == "":
        return None
    raise ValueError("Expected empty value")


EmptyStrOrNone: TypeAlias = Annotated[None, BeforeValidator(_empty_str_or_none)]


class Line(SQLModel, table=True):
    line_id: int = SQLField(default=None, nullable=False, primary_key=True)
    name: str
    status: StatusEnum = SQLField(nullable=False, default=StatusEnum.OFFLINE)


class LineLog(SQLModel, table=True):
    log_id: int = SQLField(default=None, nullable=False, primary_key=True)
    line_id: int = SQLField(default=None, nullable=False, foreign_key="line.line_id")
    created_at: datetime = SQLField(nullable=False, default_factory=lambda: datetime.now())
    status: StatusEnum = SQLField(nullable=False, default=StatusEnum.OFFLINE)
    data: dict = SQLField(sa_type=JSON)


class LineEvent(SQLModel, table=True):
    event_id: int = SQLField(default=None, nullable=False, primary_key=True)
    line_id: int = SQLField(default=None, nullable=False, foreign_key="line.line_id")
    log_id: int = SQLField(default=None, nullable=True, foreign_key="linelog.log_id")
    start_at: datetime = SQLField(nullable=False, default_factory=lambda: datetime.now())
    status: StatusEnum = SQLField(nullable=False, default=StatusEnum.OFFLINE)
    description: Optional[str] = SQLField(default=None, nullable=True)

    @property
    def is_stop(self):
        return self.status == StatusEnum.STOPPED


class LineCreate(BaseModel):
    name: str = Field(description="Название линии", max_length=100,)
    status: StatusEnum = Field(default=StatusEnum.OFFLINE)


class LineUpdate(LineCreate):
    status: Optional[StatusEnum] = Field(default=None)


class LineRead(LineCreate):
    line_id: int


class LinesList(BaseModel):
    items: List[LineRead]
    offset: int
    limit: int
    total: int


class LogCreate(BaseModel):
    line_id: int
    data: dict


class LogRead(LogCreate):
    log_id: int
    line_id: int
    data: dict
    created_at: datetime
    status: StatusEnum
