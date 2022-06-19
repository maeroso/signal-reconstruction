import os.path
from threading import Event, Thread
from typing import List

from dotenv import load_dotenv
from pandas import read_csv, DataFrame

from controller.worker import Worker
from utils.enums.file_name import FileName
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

while not host_overloaded:
    sources_loaded_event = Event()

    workers.append(Worker(name=str(len(workers) + 1), host=os.getenv("RABBIT_HOST"), load_sources=sources_loaded_event))

    sources_loaded_event.wait()

    # TODO verify system load

for worker in workers:
    worker.join()

ThreadSafeTools.print(" [*] All workers finished\n")
ThreadSafeTools.print(" [*] Exiting\n")
ThreadSafeTools.print(" [*] Bye!\n")
