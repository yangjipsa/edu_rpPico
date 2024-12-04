import network
import urequests
import time
from machine import Pin

SSID = 'YangJipsa_MyRoom2.4G'
PASSWORD = 'Yangjipsa0612!'

FIREBASE_URL = 'https://yangjipsa-test-78005-default-rtdb.firebaseio.com/' 

# GPIO 핀 설정
led_red = Pin(2, Pin.OUT)
led_blu = Pin(3, Pin.OUT)

def turnOffLeds(ledPin):
    ledPin.on()

def turnOnLeds(ledPin):
    ledPin.off()
    
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
    connect_to_wifi(SSID, PASSWORD)
    
    while True:
        data = fetch_from_firebase()
        if data:
            print(f"Received Data: {data}")
            #print(type(data))
            if (data["LED1"] == True):
                turnOnLeds(led_red)
            elif (data["LED1"] == False):
                turnOffLeds(led_red)

            if (data["LED2"] == True):
                turnOnLeds(led_blu)
            elif (data["LED2"] == False):
                turnOffLeds(led_blu)
        else:
            print("No data received.")
        
        time.sleep(3)

except KeyboardInterrupt:
    print("프로그램 종료")

