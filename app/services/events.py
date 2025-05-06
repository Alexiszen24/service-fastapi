from datetime import datetime
from typing import Annotated, Optional, List, Tuple
from sqlalchemy import func
from sqlmodel import Session, select

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


def get_event(event_id: int,
              db_session: Session = None) -> LineEvent:
    query = select(LineEvent).where(LineEvent.event_id == event_id)
    event = db_session.exec(query).first()
    return event


def get_events(line_id: int,
               limit: Optional[int] = 10,
               offset: Optional[int] = 0,
               db_session: Session = None) -> Tuple[List[LineEvent], int]:
    # db_session: Session = get_session()
    query = select(LineEvent).where(LineEvent.line_id == line_id).offset(offset).limit(limit)
    results = db_session.execute(query)
    total = db_session.execute(select(func.count()).select_from(Line))
    return results.scalars().all(), total.scalar()
