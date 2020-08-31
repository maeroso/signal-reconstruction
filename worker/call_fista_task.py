#!/usr/bin/env python
from pandas import pandas
import numpy
import pika
import sys
import constantes

g = pandas.read_csv('./../files/avaliacao/sinal1.csv', sep='\n',
                    decimal=',', header=None, dtype=float).to_numpy()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=constantes.nome_fila_fista, durable=True)

message = g.tobytes()

channel.basic_publish(
    exchange='',
    routing_key=constantes.nome_fila_fista,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent message on fista queue")

connection.close()
