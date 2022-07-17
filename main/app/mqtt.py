from app.helpers import save_meter_data_in_db
from paho.mqtt import client as mqtt_client
import random
from django.conf import settings
import json


class MqttClient:
    """
    class for mqttclient related operations and defintions

    """
    broker = settings.MQTT_BROKER
    port = settings.MQTT_PORT
    topic = settings.MQTT_TOPIC
    client_id = f"python-mqtt-{random.randint(0, 1000)}"
    username = settings.MQTT_USERNAME
    password = settings.MQTT_PASSWORD

    def connect_mqtt(self):
        """
        connect to the mqtt client
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt_client):
        """
        this method subscribes to a topic for a mqtt client

        Args:
            client (mqtt_client): mqtt client connection
        """
        def on_message(client, userdata, msg):
            data = json.loads(msg.payload)
            save_meter_data_in_db(data)
        client.subscribe(self.topic)
        client.on_message = on_message

