from enum import Enum


class StatusEnum(str, Enum):
    OFFLINE = "offline"  # линия/станок не в сети или вырублен
    IN_WORK = "in_work"  # в работе
    STOPPED = "stopped"  # остановлен
