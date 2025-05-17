import network
import urequests
import time
import json

from machine import Pin, PWM
import time

pinServo = 14

servo = PWM(Pin(pinServo))
servo.freq(50) # Period : 20ms


# Wi-Fi 연결 정보
SSID = '네트워크 SSID'  # 자신의 Wi-Fi 이름 입력
PASSWORD = '네트워크 PASSWORD'  # 자신의 Wi-Fi 비밀번호 입력

# Firebase 설정
FIREBASE_URL = '파이어베이스 리얼타임데이터베이스 URL'  # 파이어베이스 리얼타임 데이터베이스 URL
FIREBASE_API_KEY = '웹API키'  # 파이어베이스 웹 API 키


# Wi-Fi 연결 함수
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network connected:', wlan.ifconfig())


# Pico에서는 duty_u16 (0 ~ 65535) 기준
def set_angle(angle):
    # angle (0~180) → duty_u16 (1638 ~ 8192)
    min_duty = 1638  # 약 0.5ms
    max_duty = 8192   # 약 2.5ms
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

def doorOpen():
    set_angle(0)
def doorClose():
    set_angle(90)
    
# Firebase에서 doorlock 상태를 받아오는 함수 (GET 방식)
def get_doorlock_status():
    try:
        url = FIREBASE_URL + 'doorOpen.json'
        response = urequests.get(url)
        if response.status_code == 200:
            result = response.json()  # True 또는 False가 올 것임
            print('doorOpen status from Firebase:', result)
            return result
        else:
            print('Failed to fetch doorOpen status, status code:', response.status_code)
            return None
    except Exception as e:
        print('Error fetching doorOpen status:', e)
        return None
    finally:
        if 'response' in locals():
            response.close()

doorClose()
time.sleep(1)
# Wi-Fi 연결
connect_to_wifi(SSID, PASSWORD)
while True:

    # doorlock 상태 가져오기
    doorOpen_status = get_doorlock_status()
    if doorOpen_status is not None:
        if doorOpen_status:
            print("Door is OPEN")
            doorOpen()
        else:
            print("Door is LOCKED")
            doorClose()
            

    # 10초마다 반복
    time.sleep(10)


