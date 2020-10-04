from threading import Event


class SolicitationResourceAccessContainer:
    def __init__(self, thread_wake_up_event: Event, identification: int, maximum_cpu_load=101, minimum_free_memory=-1.0
                 ) -> None:
        self.thread_event = thread_wake_up_event
        self.maximum_cpu_load = maximum_cpu_load
        self.minimum_free_memory = minimum_free_memory
        self.identification = identification
