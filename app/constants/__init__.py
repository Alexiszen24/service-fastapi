from enum import Enum


class StatusEnum(str, Enum):
    OFFLINE = "offline"  # линия/станок не в сети
    IN_WORK = "in_work"  # в работе
    STOPPED = "stopped"  # остановлен
