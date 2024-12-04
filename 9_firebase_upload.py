import network
import urequests
import time
import json
from machine import ADC

SSID = '와이파이 SSID'
PASSWORD = '와이파이 패스워드'

FIREBASE_URL = 'Realtime Database 주소' 
FIREBASE_API_KEY = 'API 키'

def read_temp(sensorPin):
    reading = sensorPin.read_u16()
    voltage = reading * 3.3 / (65535)
    temperature_celsius = 27 - (voltage - 0.706) / 0.001721
    return temperature_celsius

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
    print('Network connected:', wlan.ifconfig())


def upload_to_firebase(data):
    headers = {'Content-Type': 'application/json'}
    url = FIREBASE_URL + '.json' 
    response = urequests.put(url, headers=headers, data=json.dumps(data))  # PUT 요청 사용
    print('Response:', response.text)
    response.close()


try :
    sensor = ADC(4)    
    connect_to_wifi(SSID, PASSWORD)

    while True:
        temperature = read_temp(sensor)
        print(f'Temperature: {temperature:.2f}°C')

        data = {
            'temp': temperature,
        }

        upload_to_firebase(data)

        time.sleep(5)

except KeyboardInterrupt :
    print("프로그램 종료")

