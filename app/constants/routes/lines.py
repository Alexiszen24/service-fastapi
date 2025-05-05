from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from app.schemas import Line, LineCreate, LineRead
from typing import List, Annotated
from app.api_docs import example_create_line

router = APIRouter(prefix="/v1/lines", tags=["Управление линиями"])


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=LineRead,
             summary='Добавить линию')
def create_line(line: Annotated[
    LineCreate,
    example_create_line,
]):
    """
    Добавить линию в БД
    """

    new_task = write_task_to_csv(task)
    return new_task


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema_task.TaskRead])
def read_tasks(limit: int = 10, offset: int = 0):
    query = select(Line).offset(offset).limit(limit)

    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The task list is empty."
        )
    return tasks


@router.get("/{task_id}", response_model=schema_task.TaskRead)
def read_task_by_id(task_id: int):
    task = read_task_from_csv(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


@router.patch("/{task_id}", status_code=status.HTTP_200_OK, response_model=schema_task.TaskRead)
def update_task_by_id(task_id: int, data_for_update: dict):
    task_fields = set(schema_task.TaskCreate.model_fields.keys())

    if not set(data_for_update.keys()) <= task_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An update request must only contain one or more of the following fields: {', '.join(task_fields)}."
        )

    task = update_task_in_csv(task_id, data_for_update)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(task_id: int):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Unable to delete task with ID {task_id}: "
               f"method is not implemented yet."
    )
