# traductor.py
import pika, json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

def convertir(mensaje_raw):
    tipo, sensor_id, valor = mensaje_raw.decode().split('|')
    return json.dumps({"sensor": tipo, "id": sensor_id, "valor": float(valor)})

def callback(ch, method, properties, body):
    mensaje_json = convertir(body)
    channel.basic_publish(exchange='', routing_key='sensores.convertidos', body=mensaje_json)
    print(f"[Traductor] {mensaje_json}")

from utils.wait_for_rabbitmq import wait_for_rabbitmq

connection = wait_for_rabbitmq()
channel = connection.channel()


channel.queue_declare(queue='sensores.raw')
channel.queue_declare(queue='sensores.convertidos')

channel.basic_consume(queue='sensores.raw', on_message_callback=callback, auto_ack=True)
print("Traductor iniciado...")
channel.start_consuming()
