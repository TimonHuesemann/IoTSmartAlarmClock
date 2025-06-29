print("Starte mqtt_listener.py")

import os
import paho.mqtt.client as mqtt


import shared_files.database_manager_API as db_manager

db = db_manager.DatabaseManager("SmartAlarmClock", "postgres", "postgres")

broker = os.getenv("MQTT_BROKER", "localhost")
topic = os.getenv("MQTT_TOPIC", "test/topic")
port = int(os.getenv("MQTT_PORT", 1883))

print(f"MQTT Broker: {broker}")
print(f"MQTT Topic: {topic}")

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.payload:
        # Assuming the payload is a string in the format "time, eventname"
        try:
            data = msg.payload.decode('utf-8').split(',')
            if len(data) == 2:
                time, eventname = data
                print(f"Received sleep event: time={time}, eventname={eventname}")
                db.connect()
                db.insert_data('sleep_events', (time, eventname), primary_key_names="time")
                db.close()
            else:
                print("Invalid payload format. Expected 'time, eventname'.")
        except Exception as e:
            print(f"Error processing message: {e}")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()



# docker run --rm eclipse-mosquitto mosquitto_pub -h host.docker.internal -p 1883 -t test/topic -m "Test von Docker" <- Befehl zum Testen des MQTT Brokers
