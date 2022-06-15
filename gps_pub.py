#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import serial
import random
import os
import time
from paho.mqtt import client as mqtt_client
from micropyGPS import MicropyGPS


broker = "localhost"
port = 1883
topic = "test"
client_id = "python-mqtt-"+ str(random.randint(0, 1000))


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # シリアル通信設定
    uart = serial.Serial('/dev/serial0', 9600, timeout = 10)
    # gps設定
    my_gps = MicropyGPS(9, 'dd')

    # 10秒ごとに表示
    tm_last = 0
    while True:
        time.sleep(1)
        sentence = uart.readline()

        if len(sentence) > 0:
            for x in sentence:
                if 10 <= x <= 126:
                    stat = my_gps.update(chr(x))
                    if stat:
                        latitude = str(my_gps.latitude[0])
                        longitude = str(my_gps.longitude[0])
                        msg = "messges: " + my_gps.date_string() + ", " + latitude + ", " + longitude
                        result = client.publish(topic, msg)
                        status = result[0]
                        if status == 0:
                            print("Send " + msg + " to topic " + topic)
                        else:
                            print("Failed to send message to topic " + topic)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()
