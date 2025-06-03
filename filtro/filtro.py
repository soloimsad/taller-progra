# filtro/filtro.py
import pika, json

def callback(ch, method, properties, body):
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
        print(f"[Filtro] Alerta por {dato['sensor']}")
        channel.basic_publish(exchange='', routing_key='sensores.alertas', body=body)

from wait_for_rabbitmq import wait_for_rabbitmq
import pika

connection = wait_for_rabbitmq()
channel = connection.channel()

channel.basic_consume(queue='sensores.convertidos', on_message_callback=callback, auto_ack=True)
print("Filtro iniciado...")
channel.start_consuming()
