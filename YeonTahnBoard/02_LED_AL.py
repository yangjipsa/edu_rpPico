# ================================================================
#  파일명    : 02_LED_AL.py
#  설명      : Active Low LED 블링크 예제
#             value(0) = 켜짐 · value(1) = 꺼짐  (반대로 동작)
#             켜진 시간을 길게 · 꺼진 시간을 짧게 하여
#             HIGH / LOW 신호의 시간차를 눈으로 체감
#  대상 부품 : LED4 (GP2)  · 온보드 Active Low LED
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep

# ---------- 핀 설정 ----------
LED_AL = Pin(2, Pin.OUT)   # LED4 · Active Low

# ---------- 시작 상태 · 모든 동작 없음 ----------
LED_AL.value(1)            # AL 이므로 HIGH 가 "꺼짐"

try:
    while True:
        # LOW · 오래 켜짐 (Active Low 이므로 0이 켜짐)
        LED_AL.value(0)
        sleep(1.5)

        # HIGH · 짧게 꺼짐
        LED_AL.value(1)
        sleep(0.3)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    LED_AL.value(1)        # AL 이므로 HIGH 가 "꺼짐"
