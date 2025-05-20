import ntptime ####
import network
import urequests
import time
import json
from machine import ADC

SSID = 'MakerSpace_AP_2'
PASSWORD = '1234qwer@'

FIREBASE_URL = 'https://aict-250520-default-rtdb.firebaseio.com/' 
FIREBASE_API_KEY = 'AIzaSyBJy1g0R9vymyXW28Nfil5LmW87GMgFK3U'

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


def upload_to_firebase(data, date_text):
    headers = {'Content-Type': 'application/json'}
    url = FIREBASE_URL + date_text + '.json' 
    response = urequests.put(url, headers=headers, data=json.dumps(data))  # PUT 요청 사용
    print('Response:', response.text)
    response.close()


try :
    sensor = ADC(4)    
    connect_to_wifi(SSID, PASSWORD)
    ntptime.settime()  # NTP 서버로부터 시간 동기화
    kst_offset = 9 * 60 * 60  # UTC+9 시간 차이 (초 단위)
    day_of_week = ["월", "화", "수", "목", "금", "토", "일"]
    
    while True:
        current_time = time.localtime(time.time() + kst_offset)
        formatted_time = "{:02d}-{:02d}-{:02d}".format(
            current_time[0] % 100,  # YY
            current_time[1],  # MM
            current_time[2]  # DD
        )
        
        temperature = read_temp(sensor)
        print(f'Temperature: {temperature:.2f}°C')

        data = {
            'temp': temperature,
            'text' : "test text",
        }

        upload_to_firebase(data, formatted_time)

        time.sleep(5)

except KeyboardInterrupt :
    print("프로그램 종료")

