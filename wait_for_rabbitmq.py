import pika
import time

def wait_for_rabbitmq(host='rabbitmq', user='admin', password='admin', retries=10, delay=5):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, credentials=credentials)

    for attempt in range(retries):
        try:
            connection = pika.BlockingConnection(parameters)
            print("✅ Conexión a RabbitMQ exitosa.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[{attempt + 1}/{retries}] Esperando a RabbitMQ... Error: {e}")
            time.sleep(delay)
    raise Exception("❌ No se pudo conectar a RabbitMQ después de varios intentos.")
