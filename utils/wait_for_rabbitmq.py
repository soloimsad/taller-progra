# utils/wait_for_rabbitmq.py (mejorado)
import pika
import time
import logging

logging.basicConfig(level=logging.INFO)

def wait_for_rabbitmq(
    host='rabbitmq',
    user='admin',
    password='admin',
    max_retries=15,
    initial_delay=2,
    backoff_factor=2
):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(
        host=host,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )
    
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(parameters)
            logging.info("✅ Conexión a RabbitMQ exitosa")
            return connection
        except Exception as e:
            logging.warning(f"⚠️ Intento {attempt+1}/{max_retries}: Error conectando a RabbitMQ: {str(e)}")
            time.sleep(delay)
            delay *= backoff_factor
            if delay > 30:  # Límite máximo de espera
                delay = 30
    
    raise ConnectionError(f"❌ No se pudo conectar a RabbitMQ después de {max_retries} intentos")