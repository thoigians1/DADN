import sys
import time

# Import AdaruitIO MQTTClient
from Adafruit_IO import MQTTClient

import requests

# Define AIO variable
AIO_FEED_ID = ["people", "buzzer"]
AIO_USERNAME = "duongthanhthuong"
AIO_KEY = "aio_yAwb29538GaONNlzu2ZOXMKeQhmR"

BASE = "http://127.0.0.1:8000/api"

client = MQTTClient(AIO_USERNAME, AIO_KEY)

# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called when the client connects.
    """
    for id in AIO_FEED_ID:
        client.subscribe(id)

def disconnected(client):
    """Disconnected function will be called when the client disconnects.
    """
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """

    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    
    if feed_id == "people":
        requests.post(BASE + f"/room/log?nop={payload}")
    elif feed_id == "buzzer" and int(payload) == 4:
        requests.post(BASE + f"/buzzer/log")
        

# Create an MQTT client instance.
client = MQTTClient(AIO_USERNAME, AIO_KEY)
# Setup the callback functions defined above.
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message
client.connect()
client.loop_background()
while True:
    pass