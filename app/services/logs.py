from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.constants import StatusEnum
from app.schemas import LogCreate, LineLog, LogRead, LineEvent
from .lines import get_line
from .events import create_event


def log_status_to_line(status):
    if status in [500, 501]:
        return StatusEnum.IN_WORK
    if status == 0:
        return StatusEnum.OFFLINE
    return StatusEnum.STOPPED


def add_log(log_create: LogCreate,
            db_session: Session) -> LogRead:
    """
    Обработка поступившего лога
    """
    log_data = log_create.data
    line_id = log_create.line_id

    log_status = log_data["status"]
    new_line_status = log_status_to_line(log_status)

    # Создаем лог
    log = LineLog(**log_create.model_dump(), status=new_line_status)
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    # Берем линию и проверяем текущий статус
    line = get_line(line_id=line_id, db_session=db_session)

    print('LL', new_line_status, log_status)

    # Если статус лога равен текущему, ничего не делаем
    if new_line_status == line.status:
        return log

    line.status = new_line_status
    db_session.add(line)
    db_session.commit()

    # Если нет информации (статус OFFLINE), просто меняем состояние линии
    if new_line_status == StatusEnum.OFFLINE:
        return log

    # Иначе изменяем список событий

    # Берем 2 последних события
    last_events: List[LineEvent] = db_session.execute(
        select(LineEvent).where(LineEvent.line_id == line_id).order_by(LineEvent.start_at.desc()).limit(2)
    ).scalars().all()

    last_event = None
    last_event_2 = None

    if len(last_events) > 0:
        last_event = last_events[0]
    if len(last_events) > 1:
        last_event_2 = last_events[1]

    now_time = datetime.now()

    #####################

    # Если нет ни одного события, просто добавляем новое
    if not last_event:
        create_event(log_id=log.log_id, line=line, start_at=log.created_at, db_session=db_session)
        return log

    # Смотрим, что есть вообще что проверять в случае коротких событий
    if last_event_2 is not None:
        # Если событие работы слишком маленькое (Y), и если второе предыдущее событие -- остановка,
        # то удаляем рабочее время как очень маленькое и
        # не создаем новый простой, а продолжаем предыдущий
        if (now_time - last_event.start_at).total_seconds() <= 60 and last_event_2.is_stop:
            # Если второе предыдущее событие -- остановка, то удаляем рабочее время как очень маленькое и
            # не создаем новый простой, а продолжаем предыдущий
            db_session.delete(last_event)
            db_session.commit()

            return log

        # Если предыдущая остановка была очень короткой (и не размеченной, то есть не указан description!)
        # а время работы существенное, то удаляем простой
        elif (last_event.start_at - last_event_2.start_at).total_seconds() <= 120 and \
                (not last_event_2.description) and last_event_2.is_stop:
            last_event.start_at = last_event_2.start_at
            db_session.delete(last_event_2)
            db_session.commit()
            # Дальше продолжаем обработку поступившего события

    create_event(log_id=log.log_id, line=line, start_at=log.created_at, db_session=db_session)
    return log
