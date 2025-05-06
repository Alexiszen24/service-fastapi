from datetime import datetime
from typing import Annotated, Optional, List, Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.config import settings
from app.db import get_session
from app.schemas import Line, LineLog, LineEvent


def create_event(
        log_id: int,
        line: Line,
        start_at: datetime,
        db_session: Session = None) -> LineEvent:
    event = LineEvent(
        log_id=log_id,
        line_id=line.line_id,
        status=line.status,
        start_at=start_at
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event
