import network
import urequests
import time
from machine import Pin

SSID = 'Emb_lab_01'
PASSWORD = '12345678'

FIREBASE_URL = 'Realtime Database 주소' 
FIREBASE_API_KEY = 'API 키'

#FIREBASE_URL = 'https://sht-iot-2025-default-rtdb.firebaseio.com/' 
#FIREBASE_API_KEY = 'AIzaSyBjOtUMdfAVHZiy4oI5FSXBZBNiz-1hjJk'

# GPIO 핀 설정
led1 = Pin(LED, Pin.OUT)
    
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
                led1.on()
            elif (data["LED1"] == False):
                led1.off()

        else:
            print("No data received.")
        
        time.sleep(3)

except KeyboardInterrupt:
    print("프로그램 종료")
