from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlmodel import Session

from app.auth import get_current_user
from app.db import get_session
from app.schemas import EventsList, EventUpdate, LineEvent, EventRead, User
from app.services import events

router = APIRouter(prefix="/v1/events", tags=["Работа с событиями"])


@router.get("/{line_id}",
            status_code=status.HTTP_200_OK,
            summary="Список событий на линии",
            response_model=EventsList)
def read_lines_list_req(line_id: int, limit: int = 10, offset: int = 0, db_session: Session = Depends(get_session)):
    events_list, total = events.get_events(line_id, limit, offset, db_session=db_session)

    if not events_list:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Events list is empty."
        )

    return {
        "items": events_list,
        "offset": offset,
        "limit": limit,
        "total": total,
    }


@router.patch(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
    response_model=EventRead,
    summary="Обновить событие",
)
def update_line_by_id(
        event_id: int,
        data_for_update: EventUpdate,
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_session),
):
    event = events.get_event(event_id, db_session)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found"
        )

    if data_for_update.description:
        event.description = data_for_update.description

    db_session.commit()
    db_session.refresh(event)

    return event
