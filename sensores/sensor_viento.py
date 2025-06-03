# sensores/sensor_viento.py
import pika, json, random, time, uuid

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
    viento = random.uniform(0, 50)
    mensaje = f"viento|{sensor_id}|{viento:.2f}"
    channel.basic_publish(exchange='', routing_key=queue, body=mensaje)
    print(f"[Viento] {mensaje}")
    time.sleep(random.randint(10, 15))
