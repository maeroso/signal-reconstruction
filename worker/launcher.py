import os.path
from threading import Event, Thread
from time import sleep
from typing import List

import psutil
from dotenv import load_dotenv
from pandas import read_csv, DataFrame

from controller.worker import Worker
from model.rabbit_resolver import RabbitResolver
from utils.enums.file_name import FileName
from utils.enums.queues import Queues
from utils.thread_safe_tools import ThreadSafeTools

load_dotenv()

if not os.path.exists(os.path.join("static", FileName.H1_PICKLE.value)):
    ThreadSafeTools.print(" [*] Creating H-1.pickle file\n")
    matriz = read_csv(filepath_or_buffer=os.path.join("static", FileName.H1_CSV.value), header=None,
                      dtype=float).to_numpy()
    DataFrame(data=matriz, dtype=float).to_pickle(path=os.path.join("static", FileName.H1_PICKLE.value))
    DataFrame(data=matriz.transpose(), dtype=float).to_pickle(
        path=os.path.join("static", FileName.HT1_PICKLE.value))

if not os.path.exists(os.path.join("static", FileName.H2_PICKLE.value)):
    ThreadSafeTools.print(" [*] Creating H-1.pickle file\n")
    matriz = read_csv(filepath_or_buffer=os.path.join("static", FileName.H2_CSV.value), header=None,
                      dtype=float).to_numpy()
    DataFrame(data=matriz, dtype=float).to_pickle(path=os.path.join("static", FileName.H2_PICKLE.value))
    DataFrame(data=matriz.transpose(), dtype=float).to_pickle(
        path=os.path.join("static", FileName.HT2_PICKLE.value))

workers: List[Thread] = []
host_overloaded: bool = False

gigabyte_to_byte = 1000000000

while not host_overloaded:
    with RabbitResolver(queue_name=Queues.JOB_REQUEST_QUEUE, passive=True) as rabbit:
        batata = rabbit.queue.method.message_count
        if len(workers) != 0 and rabbit.queue.method.message_count == 0:
            sleep(1.0)
            continue

        sources_loaded_event = Event()

        workers.append(
            Worker(name=str(len(workers) + 1), host=os.getenv("RABBIT_HOST"), load_sources=sources_loaded_event)
        )

        sources_loaded_event.wait()

        if psutil.cpu_percent(percpu=False, interval=.1) > int(os.getenv("MAXIMUM_CPU_LOAD")) or \
                psutil.virtual_memory().available < gigabyte_to_byte * int(os.getenv("MINIMUM_FREE_MEMORY")):
            host_overloaded = True

        sources_loaded_event.set()

for worker in workers:
    worker.join()

ThreadSafeTools.print(" [*] All workers finished\n")
ThreadSafeTools.print(" [*] Exiting\n")
ThreadSafeTools.print(" [*] Bye!\n")
