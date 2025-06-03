# activador.py
import pika, json, csv
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
def callback(ch, method, properties, body):
    evento = json.loads(body)
    accion = "activar" if evento['sensor'] == "humedad" else "detener"
    mensaje = f"{evento['sensor']}|zona1|{accion}"
    channel.basic_publish(exchange='', routing_key='riego.control', body=mensaje)
    channel.basic_publish(exchange='', routing_key='logger.eventos', body=json.dumps({"evento": mensaje, "ts": datetime.now().isoformat()}))
    print(f"[Activador] Acción: {mensaje}")
from utils.wait_for_rabbitmq import wait_for_rabbitmq

connection = wait_for_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='sensores.alertas')
channel.queue_declare(queue='riego.control')
channel.queue_declare(queue='logger.eventos')

channel.basic_consume(queue='sensores.alertas', on_message_callback=callback, auto_ack=True)
print("Activador iniciado...")
channel.start_consuming()
