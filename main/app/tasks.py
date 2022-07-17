from celery.decorators import task
from app.mqtt import MqttClient


@task(name="run_mqtt_server")
def run_mqtt_server():
    """
    method for data ingestion from Mqtt

    Returns:
        bool: True
    """
    mqtt_conn = MqttClient()
    client = mqtt_conn.connect_mqtt()
    mqtt_conn.subscribe(client)
    client.loop_forever()
    return True
