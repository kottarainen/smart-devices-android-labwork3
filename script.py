import os
import json
import subprocess
import paho.mqtt.client as mqtt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

MQTT_BROKER = "localhost"  
MQTT_PORT = 1883
MQTT_TOPIC = "your/mqtt/topic"

def create_json_file():
    try:
        data = {
            "message": "This is a sample JSON content",
            "status": "success"
        }
        with open("/tmp/message.json", "w") as json_file:
            json.dump(data, json_file)
        logger.info("JSON file created successfully.")
    except Exception as e:
        logger.error(f"Failed to create JSON file: {e}")

def execute_system_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.info(f"Command executed: {command}")
        logger.info(f"Output: {result.stdout}")
    except Exception as e:
        logger.error(f"Failed to execute command '{command}': {e}")

def perform_reboot():
    try:
        if os.name == 'posix':
            logger.info("Rebooting the system.")
            subprocess.run(["sudo", "reboot"], capture_output=True, text=True)
        else:
            logger.warning("Reboot command is not supported on this OS.")
    except Exception as e:
        logger.error(f"Failed to reboot: {e}")

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    logger.info(f"Message received: {msg.payload.decode()}")
    create_json_file()
    execute_system_command("ls /tmp")
    perform_reboot()

if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)  
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
