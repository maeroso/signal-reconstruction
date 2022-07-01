"""Arquivo contento o controlador do envio de mensagens de heartbeat de múltiplas conexões com o
    RabbitMQ.
"""
from threading import Thread
from time import sleep
from typing import List

from pika import BlockingConnection


class HeartbeatController(Thread):
    """
        The list of connections to monitor
    """

    __connections: List[BlockingConnection] = []
    __wait_time: float = 1.0

    def __init__(self):
        super().__init__(daemon=True, name="HeartbeatController")

    def add_connection(self, connection: BlockingConnection):
        """Método adiciona uma conexão a lista de conexões para qual será enviado o heartbeat.

        Parameters
        ----------
        connection : BlockingConnection
            Conexão a ser adicionada a lista de conexões.
        """

        self.__connections.append(connection)
        if len(self.__connections) == 1:
            self.start()

    def run(self):
        while True:
            if len(self.__connections) == 0:
                break
            for connection in self.__connections:
                if not connection.is_open:
                    self.__connections.remove(connection)
                    continue
                connection.process_data_events()
            sleep(self.__wait_time)
