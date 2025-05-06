from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlmodel import Session

from app.db import get_session
from app.schemas import Line, LogCreate, LineLog, LogRead
from typing import List, Annotated
from app.api_docs import example_create_line
from app.services import logs

router = APIRouter(prefix="/v1/logs", tags=["Добавление логов"])


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=LogRead,
             summary='Добавить и обработать лог')
def create_log(
        log: LogCreate,
        db_session: Session = Depends(get_session)):
    """
    Добавить лог в БД
    """

    log_obj = logs.add_log(log, db_session=db_session)
    return log_obj
