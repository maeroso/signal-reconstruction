#!/usr/bin/env python
from pandas import pandas
import numpy
import pika
import sys

g = pandas.read_csv('./../files/avaliacao/sinal2.csv', sep='\n',
                    decimal=',', header=None, dtype=float).to_numpy()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ', '.join([str(elem) for elem in g])

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent message")
print(message)

connection.close()
