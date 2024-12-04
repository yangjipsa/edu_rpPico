import network
import urequests
import time
import json
from machine import Pin
from machine import ADC

SSID = '와이파이 SSID'
PASSWORD = '와이파이 패스워드'

FIREBASE_URL = 'Realtime Database 주소' 
FIREBASE_API_KEY = 'API 키'

# GPIO 핀 설정
led_red = Pin(2, Pin.OUT)
led_blu = Pin(3, Pin.OUT)

def turnOffLeds(ledPin):
    ledPin.on()

def turnOnLeds(ledPin):
    ledPin.off()
    
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
    response = urequests.patch(url, headers=headers, data=json.dumps(data))
    #response = urequests.put(url, headers=headers, data=json.dumps(data))
    print('Response:', response.text)
    response.close()    

def fetch_from_firebase():
    url = FIREBASE_URL + '.json'
    #url = FIREBASE_URL + 'PICO.json'
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            print('Data from Firebase:', data)
            response.close()
            return data
        else:
            print('Failed to fetch data:', response.status_code)
            response.close()
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

try:
    sensor = ADC(4)    
    connect_to_wifi(SSID, PASSWORD)
    
    while True:
        temperature = read_temp(sensor)
        print(f'Temperature: {temperature:.2f}°C')

        data = {
            'temp': temperature,
        }

        upload_to_firebase(data)
        
        data = fetch_from_firebase()
        if data:
            print(f"Received Data: {data}")
            #print(type(data))
            if (data["LED1"] == "true"):
                turnOnLeds(led_red)
            elif (data["LED1"] == "false"):
                turnOffLeds(led_red)

            if (data["LED2"] == "true"):
                turnOnLeds(led_blu)
            elif (data["LED2"] == "false"):
                turnOffLeds(led_blu)
        else:
            print("No data received.")
        
        time.sleep(3)

except KeyboardInterrupt:
    print("프로그램 종료")


