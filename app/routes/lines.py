from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlmodel import Session

from app.db import get_session
from app.schemas import Line, LineCreate, LineRead, LineUpdate, LinesList
from typing import List, Annotated
from app.api_docs import example_create_line
from app.services import lines

router = APIRouter(prefix="/v1/lines", tags=["Управление линиями"])


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=LineRead,
             summary='Добавить линию')
def create_line_req(
        line: Annotated[
            LineCreate,
            example_create_line,
        ],
        db_session: Session = Depends(get_session)):
    """
    Добавить линию в БД
    """

    line_obj = lines.create_line(line, db_session=db_session)
    return line_obj


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="Список линий",
            response_model=LinesList)
def read_lines_list_req(limit: int = 10, offset: int = 0, db_session: Session = Depends(get_session)):
    lines_list, total = lines.get_lines(limit, offset, db_session=db_session)

    if not lines_list:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The lines list is empty."
        )
    return {
        "items": lines_list,
        "offset": offset,
        "limit": limit,
        "total": total,
    }


@router.get("/{line_id}", response_model=LineRead)
def read_line_by_id(line_id: int, db_session: Session = Depends(get_session)):
    line = lines.get_line(line_id, db_session=db_session)

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Line with ID {line_id} not found"
        )

    return line


@router.patch("/{line_id}", status_code=status.HTTP_200_OK, response_model=LineRead)
def update_line_by_id(line_id: int, data_for_update: LineUpdate, db_session: Session = Depends(get_session)):
    line = lines.get_line(line_id, db_session=db_session)

    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Line with ID {line_id} not found"
        )

    if data_for_update.name:
        line.name = data_for_update.name
    if data_for_update.status:
        line.status = data_for_update.status

    db_session.commit()
    db_session.refresh(line)

    return line


@router.delete("/{line_id}", status_code=status.HTTP_200_OK)
def delete_line_by_id(line_id: int, db_session: Session = Depends(get_session)):
    lines.delete_line(line_id, db_session=db_session)
