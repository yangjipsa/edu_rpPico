import network
import urequests
import time
import json
from machine import ADC
import ntptime  # NTP 시간 동기화 라이브러리

# Wi-Fi 연결 정보
SSID = 'YangJipsa_2.4G'  # 자신의 Wi-Fi 이름 입력
PASSWORD = 'Yangjipsa0612!'  # 자신의 Wi-Fi 비밀번호 입력

# Firebase 설정
FIREBASE_URL = 'https://yangjipsa-test-78005-default-rtdb.firebaseio.com/'  # 파이어베이스 리얼타임 데이터베이스 URL
FIREBASE_API_KEY = 'AIzaSyBM4O4DQ-17Z6_D6pxyr2U7O8xBDJOX14Q'  # 파이어베이스 웹 API 키

# 온도 값을 읽는 함수
def read_temperature():
    sensor = ADC(4)  # 피코의 온도 센서는 ADC 채널 4에 연결됨
    reading = sensor.read_u16()  # 온도 값을 읽음 (0~65535 범위의 ADC 값)
    voltage = reading * 3.3 / (65535)  # 16비트 값을 전압으로 변환
    temperature_celsius = 27 - (voltage - 0.706) / 0.001721  # 섭씨 온도 계산
    return temperature_celsius

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

# NTP 서버를 사용하여 시간 동기화 함수
def sync_time():
    try:
        ntptime.settime()  # NTP 서버와 시간을 동기화
        print("Time synchronized successfully")
    except:
        print("Failed to synchronize time")

# KST 시간을 시:분:초로 변환하는 함수
def get_kst_time():
    kst_offset = 9 * 60 * 60  # KST는 UTC보다 9시간 빠름
    kst_time = time.time() + kst_offset
    local_time = time.localtime(kst_time)  # 로컬 타임으로 변환
    return "{:02}:{:02}:{:02}".format(local_time[3], local_time[4], local_time[5])  # 시:분:초 형식으로 반환

# Firebase에 데이터 업로드 함수 (PUT 사용)
def upload_to_firebase(data):
    headers = {'Content-Type': 'application/json'}
    url = FIREBASE_URL + 'data.json'  # 'data'라는 경로로 데이터를 업로드
    response = urequests.put(url, headers=headers, data=json.dumps(data))  # PUT 요청 사용
    print('Response:', response.text)
    response.close()

# 메인 코드
def main():
    # Wi-Fi 연결
    connect_to_wifi(SSID, PASSWORD)

    # NTP 서버로 시간 동기화
    sync_time()

    while True:
        # 온도 측정
        temperature = read_temperature()
        print(f'Temperature: {temperature:.2f}°C')

        # 현재 KST 시간 가져오기
        current_time = get_kst_time()
        print(f'Current KST Time: {current_time}')

        # 업로드할 데이터
        data = {
            'temp': temperature,
            'time': current_time  # 타임스탬프 대신 KST 시:분:초 형식
        }

        # Firebase에 데이터 업로드
        upload_to_firebase(data)

        # 10초마다 데이터 업로드
        time.sleep(10)

# 코드 실행
main()

