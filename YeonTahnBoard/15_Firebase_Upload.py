# ================================================================
#  파일명    : 15_Firebase_Upload.py
#  설명      : 스위치 · ADC · 내장온도 값을 1초마다 읽어
#             Firebase Realtime Database 의 /yeontahn/latest 에
#             현재값을 덮어쓴다(PUT). 이력(logs)은 남기지 않음.
#             상태 표시등 없음 → 진행 상황은 Shell 출력으로 확인.
#             시작·종료 시 LED · 네오픽셀을 모두 끈다.
#  참고      : LED 극성 주의
#               LED2(GP0) = Active High → value(0) 이 꺼짐
#               LED4(GP2) = Active Low  → value(1) 이 꺼짐  ★잔류 점등 방지
#               LED3(GP1) = 극성 미확인 → 켜지면 leds_off() 의 값을 1로
#             Realtime Database REST API 사용 (urequests).
#             DB 규칙이 test 모드(공개)면 DB_SECRET 는 비워둔다.
#  대상 부품 : KEY1(GP3) · KEY2(GP4) · ADC(GP26·JP1) · 내장온도(ADC4)
#             CYW43 무선 · LED2/3/4(GP0/1/2) · SK6812 RGBW × 4(GP5)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-09-03
# ================================================================

import network
import ntptime
import time
import json
from machine import Pin, ADC
import neopixel

try:
    import urequests as requests          # 대부분의 Pico 펌웨어
except ImportError:
    import requests                        # 신형 빌드는 requests

# ---------- 사용자 설정 · 본인 환경에 맞게 수정 ----------
#  ※ GitHub 공개 업로드 전, 아래 개인정보는 반드시 지우거나 치환
WIFI_SSID  = "여기에_와이파이_이름"        # 2.4GHz 대역만
WIFI_PASS  = "여기에_비밀번호"

#  Firebase 콘솔 → Realtime Database 에서 확인한 DB 주소 (끝에 / 없이)
FB_URL     = "https://프로젝트ID-default-rtdb.firebaseio.com"
FB_PATH    = "yeontahn"                    # 데이터를 담을 최상위 경로
DB_SECRET  = ""                            # test 모드면 빈칸 · 보안이면 DB 비밀키

NTP_HOST   = "kr.pool.ntp.org"
KST_OFFSET = 9 * 3600
PERIOD_S   = 1                             # 업로드 주기(초)
# ------------------------------------------------------

# ---------- 온보드 부품 ----------
NUM  = 4
LED2 = Pin(0, Pin.OUT)                     # Active High · 0=꺼짐
LED3 = Pin(1, Pin.OUT)                     # 극성 미확인 (AH 가정)
LED4 = Pin(2, Pin.OUT)                     # Active Low  · 1=꺼짐
key1 = Pin(3, Pin.IN)                      # KEY1 · 풀업  (평상시 1 · 누름 0)
key2 = Pin(4, Pin.IN)                      # KEY2 · 풀다운(평상시 0 · 누름 1)
adc  = ADC(Pin(26))                        # 가변저항/CDS · JP1 선택
tsen = ADC(4)                              # 내장 온도센서 · ADC 채널 4
np   = neopixel.NeoPixel(Pin(5), NUM, bpp=4)   # SK6812 RGBW

# ---------- Firebase URL 조립 ----------
_auth = ("?auth=" + DB_SECRET) if DB_SECRET else ""
URL_LATEST = FB_URL + "/" + FB_PATH + "/latest.json" + _auth


def leds_off():
    """LED 3개를 각 극성에 맞게 모두 끈다."""
    LED2.value(0)                          # AH · 0 = 꺼짐
    LED3.value(0)                          # 미확인 · 켜지면 1 로 변경
    LED4.value(1)                          # AL · 1 = 꺼짐  ★LED4 잔류 점등 방지


def np_off():
    """네오픽셀 4개 모두 끈다."""
    for i in range(NUM):
        np[i] = (0, 0, 0, 0)
    np.write()


def all_off():
    """LED · 네오픽셀 전부 OFF."""
    leds_off()
    np_off()


def wifi_connect(timeout=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return wlan
    print("Wi-Fi 접속 중 :", WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            raise RuntimeError("Wi-Fi 접속 실패 · SSID/비밀번호/2.4GHz 확인")
        time.sleep(0.3)
    print("접속 완료! IP :", wlan.ifconfig()[0])
    return wlan


def sync_ntp(retry=3):
    ntptime.host = NTP_HOST
    for i in range(retry):
        try:
            ntptime.settime()
            print("NTP 시간 동기화 성공")
            return True
        except Exception as e:
            print("NTP 재시도", i + 1, "/", retry, "·", e)
            time.sleep(2)
    return False


def now_kst():
    t = time.localtime(time.time() + KST_OFFSET)
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5])


def read_temp():
    """내장 온도센서 → 섭씨(℃). 표준 변환식."""
    volt = tsen.read_u16() * 3.3 / 65535
    return 27 - (volt - 0.706) / 0.001721


def read_sensors():
    """온보드 센서를 모아 dict 로 반환."""
    adc_raw = adc.read_u16()
    return {
        "time"        : now_kst(),
        "key1"        : key1.value(),          # 풀업  : 1=안눌림 0=눌림
        "key2"        : key2.value(),          # 풀다운: 0=안눌림 1=눌림
        "key1_pressed": key1.value() == 0,
        "key2_pressed": key2.value() == 1,
        "adc_raw"     : adc_raw,               # 0 ~ 65535
        "adc_volt"    : round(adc_raw * 3.3 / 65535, 3),
        "temp_c"      : round(read_temp(), 1),
    }


def upload(data):
    """latest 에 PUT(덮어쓰기). 성공 여부 반환."""
    try:
        r = requests.put(URL_LATEST, data=json.dumps(data))
        r.close()
        return True
    except Exception as e:
        print("업로드 실패 :", e)
        return False


# ---------- 시작 상태 · 모든 동작 없음 ----------
all_off()

try:
    wifi_connect()
    sync_ntp()                             # 실패해도 계속(시각만 부정확)
    print("1초마다 Firebase 로 업로드합니다. (Ctrl+C 로 중지)")

    while True:
        data = read_sensors()
        if upload(data):
            print("업로드 OK :", data)
        time.sleep(PERIOD_S)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    all_off()
