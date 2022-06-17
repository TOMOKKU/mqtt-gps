import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883
topic = "test"
client_id = "python-mqtt-" + str(random.randint(0, 100))

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connect to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client):
    def on_message(client, userdata, msg):
        sub_msg = msg.payload.decode()
        print("Received " + sub_msg + "from " + msg.topic + " topic")
        #select supecific string
        target = ','
        idx = sub_msg.find(target)
        lati = sub_msg[:idx]
        target = ' '
        idx = sub_msg.find(target)
        longi = sub_msg[idx+1:]
        print(lati + ", " + longi)
        #translate string to float
        lati_f = float(lati)
        longi_f = float(longi)
        print(lati_f)
        print(longi_f)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
