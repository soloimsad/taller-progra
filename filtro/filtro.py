# filtro/filtro.py (corregido)
import pika, json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# --- Corrección: Definir channel como variable global ---
channel = None

def callback(ch, method, properties, body):
    print(f"[Filtro] Recibido: {body}",flush=True)
    dato = json.loads(body)
    alerta = False

    if dato['sensor'] == 'humedad' and dato['valor'] < 25:
        alerta = True
    elif dato['sensor'] == 'viento' and dato['valor'] > 30:
        alerta = True
    elif dato['sensor'] == 'escurrimiento' and dato['valor'] == 1:
        alerta = True
    elif dato['sensor'] == 'temperatura' and dato['valor'] > 35:
        alerta = True

    if alerta:
        print(f"[Filtro] Alerta por {dato['sensor']}",flush=True)
        # Usamos la variable global channel
        channel.basic_publish(exchange='', routing_key='sensores.alertas', body=body)

from utils.wait_for_rabbitmq import wait_for_rabbitmq

connection = wait_for_rabbitmq()
channel = connection.channel()  # Definimos la variable global
channel.queue_declare(queue='sensores.convertidos')
channel.queue_declare(queue='sensores.alertas')
channel.basic_consume(queue='sensores.convertidos', on_message_callback=callback, auto_ack=True)
print("Filtro iniciado...",flush=True)
channel.start_consuming()