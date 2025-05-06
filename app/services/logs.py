from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.db import get_session
from app.schemas import LogCreate, LineLog, LogRead


def add_log(log_create: LogCreate,
            db_session: Session = Depends(get_session)) -> LogRead:
    """
    Берем линию
    Кладем лог в бд
    Создаем событие если изменилась логика + обновляем линию
    """
    log = LineLog(**log_create.model_dump())
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    return log
