from queue import Queue
from threading import Thread
from threading import Condition

import psutil

from model.solicitation_resource_access_container import SolicitationResourceAccessContainer
from utils.thread_safe_tools import ThreadSafeTools


class ResourceControllerThread(Thread):

    def __init__(self):
        super().__init__()
        self.fifo_solicitation_resource = Queue()
        self.fifo_semaphore = Condition()
        self.start()

    def request_resource(self, request: SolicitationResourceAccessContainer) -> None:
        with self.fifo_semaphore:
            self.fifo_solicitation_resource.put(item=request)
            if not self.fifo_solicitation_resource.empty():
                ThreadSafeTools.print(" [*] Thread " + str(request.identification) + " are waiting  some resources\n")
        request.thread_event.wait()

    @staticmethod
    def __resource_lock(maximum_cpu_load=101, minimum_free_memory=-1, memory_lock_warning_message="",
                        cpu_lock_warning_message="") -> None:
        enable_memory_warning_message = len(memory_lock_warning_message) > 0
        enable_cpu_warning_message = len(cpu_lock_warning_message) > 0

        warning_was_show = False

        overload = psutil.cpu_percent(percpu=False, interval=.1) > maximum_cpu_load

        low_memory = psutil.virtual_memory().free < ThreadSafeTools.convert_gigabytes_to_bytes(minimum_free_memory)

        while overload or low_memory:
            if (enable_memory_warning_message or enable_cpu_warning_message) and not warning_was_show:
                if overload and enable_cpu_warning_message:
                    ThreadSafeTools.print(" [!] " + cpu_lock_warning_message + "\n")

                if low_memory and enable_memory_warning_message:
                    ThreadSafeTools.print(" [!] " + memory_lock_warning_message + "\n")

                warning_was_show = True

            overload = psutil.cpu_percent(percpu=False, interval=0.1) > maximum_cpu_load

            low_memory = psutil.virtual_memory().free < ThreadSafeTools.convert_gigabytes_to_bytes(minimum_free_memory)

    def run(self) -> None:

        while True:
            first_queue_request: SolicitationResourceAccessContainer = self.fifo_solicitation_resource.get(block=True)

            self.__resource_lock(
                minimum_free_memory=first_queue_request.minimum_free_memory,
                maximum_cpu_load=first_queue_request.maximum_cpu_load,
                memory_lock_warning_message=" [X] The thread " + str(
                    first_queue_request.identification) + " is waiting to release " + str(
                    ThreadSafeTools.convert_gigabytes_to_bytes(
                        first_queue_request.minimum_free_memory)) + "GB of RAM to continue\n",
                cpu_lock_warning_message=" [X] Thread " + str(
                    first_queue_request.identification) + " is waiting for cpu to stay below " + str(
                    first_queue_request.maximum_cpu_load) + "% load to continue\n"
            )

            first_queue_request.thread_event.set()
