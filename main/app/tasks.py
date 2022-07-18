from app.mqtt import MqttClient


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
