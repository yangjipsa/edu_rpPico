# ================================================================
#  파일명    : 14_WiFi_NTP.py
#  설명      : Wi-Fi 접속 후 NTP 서버에서 현재 시각(KST)을 받아온다.
#             접속 진행 상태를 온보드 네오픽셀 · LED 로 표시
#             빨강 = 접속 시도 · 노랑 = 실패
#             초록 = Wi-Fi OK  · 파랑 = 시간 동기화 완료
#             동기화 후 1초마다 KST 시각을 Shell 에 출력
#  참고      : Pico 2W 는 2.4GHz 대역만 지원 (5GHz 불가).
#             network · ntptime · neopixel 은 펌웨어 내장 (설치 불필요).
#             Thonny · Viper IDE(viper-ide.org) 양쪽에서 동일하게 실행.
#  대상 부품 : CYW43 무선 · SK6812 RGBW × 4 (GP5) · LED2 (GP0)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-09-03
# ================================================================

import network
import ntptime
import time
from machine import Pin
import neopixel

# ---------- 사용자 설정 · 본인 환경에 맞게 수정 ----------
#  ※ GitHub 공개 업로드 전, SSID · 비밀번호는 반드시 지우거나 치환
WIFI_SSID  = "여기에_와이파이_이름"       # 2.4GHz 대역만
WIFI_PASS  = "여기에_비밀번호"
NTP_HOST   = "kr.pool.ntp.org"           # 한국 NTP 서버
KST_OFFSET = 9 * 3600                     # 한국 표준시 = UTC + 9시간

# ---------- 온보드 부품 ----------
NUM = 4                                    # 네오픽셀 수 (U4 ~ U7)
led = Pin(0, Pin.OUT)                      # LED2 · 접속 중 깜빡임
np  = neopixel.NeoPixel(Pin(5), NUM, bpp=4)    # SK6812 RGBW · 4채널


def fill(r, g, b, w=0):
    """네오픽셀 4개를 같은 색으로."""
    for i in range(NUM):
        np[i] = (r, g, b, w)
    np.write()


def clear():
    """LED · 네오픽셀 모두 끄기."""
    led.value(0)
    fill(0, 0, 0)


def wifi_connect(timeout=15):
    """Wi-Fi 접속 · 성공 시 wlan 반환 · 실패 시 예외."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return wlan

    print("Wi-Fi 접속 중 :", WIFI_SSID)
    fill(30, 0, 0)                         # 빨강 · 접속 시도
    wlan.connect(WIFI_SSID, WIFI_PASS)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            fill(30, 25, 0)                # 노랑 · 실패
            raise RuntimeError("Wi-Fi 접속 실패 · SSID/비밀번호/2.4GHz 확인")
        led.toggle()                       # 접속 중 깜빡임
        time.sleep(0.3)

    led.value(1)                           # 접속되면 켜둠
    fill(0, 30, 0)                         # 초록 · Wi-Fi OK
    print("접속 완료! IP :", wlan.ifconfig()[0])
    return wlan


def sync_ntp(retry=3):
    """NTP 서버에서 시각을 받아 내부 RTC(UTC)를 맞춤."""
    ntptime.host = NTP_HOST
    for i in range(retry):
        try:
            ntptime.settime()              # RTC → UTC 기준
            fill(0, 0, 30)                 # 파랑 · 동기화 완료
            print("NTP 시간 동기화 성공 (" + NTP_HOST + ")")
            return True
        except Exception as e:
            print("NTP 재시도", i + 1, "/", retry, "·", e)
            time.sleep(2)
    return False


def now_kst():
    """UTC 에 KST offset 을 더해 '연-월-일 시:분:초' 반환."""
    t = time.localtime(time.time() + KST_OFFSET)
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5])


# ---------- 시작 상태 · 모든 동작 없음 ----------
clear()

try:
    wifi_connect()

    if sync_ntp():
        print("현재 시각을 1초마다 출력합니다. (Ctrl+C 로 중지)")
        while True:
            print("현재 시각(KST) :", now_kst())
            time.sleep(1)
    else:
        fill(30, 25, 0)                    # 노랑 · 동기화 실패
        print("시간 동기화 실패 · 인터넷 연결 상태 확인")

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    clear()
