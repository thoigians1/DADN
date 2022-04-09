import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_IDS = ["buzzer", "inpeople","lcd-12c","servo","outpeople","people"]


AIO_USERNAME = "duongthanhthuong"
AIO_KEY = "aio_UEXj18DdpE63SUkevlH6RNrjMXfk"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isMicrobitConnected = True


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[1] == "PEOPLE":
            client.publish("people", splitData[2])
        elif splitData[1] == "INPEOPLE":
            client.publish("inpeople", splitData[2])
        elif splitData[1] == "OUTPEOPLE":
            client.publish("outpeople", splitData[2])
    except:
        pass

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    if isMicrobitConnected:
        readSerial()
    else:
        value_servo = random.randint(0,1)
        value_lcd_12c = random.randint(2,3)
        value_buzzer = random.randint(4,5)
        value_people = random.randint(0,10)
        value_inpeople = 1
        print("Cap nhat :", value_servo)
        client.publish("servo", value_servo)
        print("Cap nhat :", value_buzzer)
        client.publish("buzzer", value_buzzer)
        print("Cap nhat :", value_lcd_12c)
        client.publish("lcd-12c", value_lcd_12c)
        print("Cap nhat :", value_people)
        client.publish("people", value_people)
        print("Cap nhat :", value_inpeople)
        client.publish("inpeople", value_inpeople)
        print("Cap nhat :", value_inpeople)
        client.publish("outpeople", value_inpeople)
    time.sleep(30)
