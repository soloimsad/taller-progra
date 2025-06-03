# sensor_humedad.py
import pika, json, random, time
import uuid

sensor_id = str(uuid.uuid4())
queue = 'sensores.raw'

for i in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        channel = connection.channel()
        print("✅ Conectado a RabbitMQ")
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"⏳ Intento {i+1}/10: Esperando que RabbitMQ esté disponible...")
        time.sleep(5)
else:
    raise Exception("❌ No se pudo conectar a RabbitMQ después de 10 intentos")

while True:
    humedad = random.uniform(15, 40)
    mensaje = f"humedad|{sensor_id}|{humedad:.2f}"
    channel.basic_publish(exchange='', routing_key=queue, body=mensaje)
    print(f"[Humedad] {mensaje}",flush=True)
    time.sleep(random.randint(10, 15))
