from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlmodel import Session

from app.db import get_session
from app.schemas import Line, LineCreate, LineRead, LineUpdate
from typing import List, Annotated
from app.api_docs import example_create_line
from app.services import lines

router = APIRouter(prefix="/v1/lines", tags=["Управление линиями"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=LineRead,
             summary='Добавить лог на линию')
def create_line_req(line: Annotated[
    LineCreate,
    example_create_line,
]):
    """
    Добавить лог в БД с обработкой
    """

    line_obj = lines.create_line(line)
    return line_obj
