from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.db import get_session
from app.schemas import LineCreate, Line, LineRead


def create_line(line_create: LineCreate,
                db_session: Session = Depends(get_session)) -> Line:
    line = Line(**line_create.model_dump())
    db_session.add(line)
    db_session.commit()
    db_session.refresh(line)
    return line


def get_line(line_id: int,
             db_session: Session = Depends(get_session)) -> Line:
    query = select(Line).where(Line.line_id == line_id)
    line = db_session.exec(query).first()
    return line


def get_lines(limit: Optional[int] = 10,
              offset: Optional[int] = 0,
              db_session: Session = Depends(get_session)) -> List[Line]:
    query = select(Line).offset(offset).limit(limit)
    results = db_session.execute(query)
    return results.scalars().all()


def delete_line(line_id: int,
                db_session: Session = Depends(get_session)):
    query = select(Line).where(Line.line_id == line_id)
    line = db_session.exec(query).first()
    db_session.delete(line)
    db_session.commit()
