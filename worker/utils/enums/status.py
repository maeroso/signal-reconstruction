from enum import IntEnum


class Status(IntEnum):
    QUEUE = 1
    PROCESSING = 2
    FINISHED = 3
