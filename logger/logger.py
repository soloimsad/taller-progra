# logger.py
import pika, json, csv
from datetime import datetime

csvfile = open("registro_eventos.csv", "a", newline="")
writer = csv.writer(csvfile)
writer.writerow(["timestamp", "evento"])

def callback(ch, method, properties, body):
    datos = json.loads(body)
    writer.writerow([datos["ts"], datos["evento"]])
    print(f"[Logger] Registrado: {datos['evento']}")
from wait_for_rabbitmq import wait_for_rabbitmq

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue='logger.eventos')
channel.basic_consume(queue='logger.eventos', on_message_callback=callback, auto_ack=True)
print("Logger iniciado...")
channel.start_consuming()
