from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.db import get_session
from app.schemas import LogCreate, Line, LineLog


def add_log(line_create: LogCreate,
            db_session: Session = Depends(get_session)) -> LineLog:
    """
    Берем линию
    Кладем лог в бд
    Создаем событие если изменилась логика + обновляем линию
    """
    line = Line(**line_create.model_dump())
    db_session.add(line)
    db_session.commit()
    db_session.refresh(line)
    return line
