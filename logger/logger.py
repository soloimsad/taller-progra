# logger.py
import pika, json, csv
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
csvfile = open("registro_eventos.csv", "a", newline="")
writer = csv.writer(csvfile)
writer.writerow(["timestamp", "evento"])

def callback(ch, method, properties, body):
    datos = json.loads(body)
    writer.writerow([datos["ts"], datos["evento"]])
    csvfile.flush()  # Forzar escritura en disco
    print(f"[Logger] Registrado: {datos['evento']}")
from utils.wait_for_rabbitmq import wait_for_rabbitmq

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue='logger.eventos')
channel.basic_consume(queue='logger.eventos', on_message_callback=callback, auto_ack=True)
print("Logger iniciado...",flush=True)
channel.start_consuming()
