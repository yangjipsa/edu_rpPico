import ntptime
import time
import network

# Wi-Fi 연결 정보
SSID = 'input wifi SSID'
PASSWORD = 'input wifi password'

# Wi-Fi 연결 함수
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print(".")
        time.sleep(1)
    print('Wi-Fi 연결 완료:', wlan.ifconfig())
    
try:
    connect_wifi()
    
    ntptime.settime()  # NTP 서버로부터 시간 동기화
    kst_offset = 9 * 60 * 60  # UTC+9 시간 차이 (초 단위)
    while True:
        current_time = time.localtime(time.time() + kst_offset)
        day_of_week = ["월", "화", "수", "목", "금", "토", "일"]
        formatted_time = "{:02d}-{:02d}-{:02d} {} {:02d}:{:02d}:{:02d}".format(
            current_time[0] % 100,  # YY
            current_time[1],  # MM
            current_time[2],  # DD
            day_of_week[current_time[6]],  # 요일
            current_time[3],  # 시
            current_time[4],  # 분
            current_time[5]   # 초
        )
        print(formatted_time)
        time.sleep(1)
        
except Exception as e:
    print('시간 동기화 실패:', str(e))
    
except KeyboardInterrupt :
    print("Turn off")




