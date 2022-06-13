from dataclasses import dataclass
from threading import Event


@dataclass
class ResourceRequest:
    thread_event: Event
    identification: int
    maximum_cpu_load: int = 101
    minimum_free_memory: float = -1.0
