# ================================================================
#  파일명    : 01_LED_AH.py
#  설명      : Active High LED 블링크 예제
#             value(1) = 켜짐 · value(0) = 꺼짐
#             켜진 시간을 길게 · 꺼진 시간을 짧게 하여
#             HIGH / LOW 신호의 시간차를 눈으로 체감
#  대상 부품 : LED2 (GP0)  · 온보드 Active High LED
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep

# ---------- 핀 설정 ----------
LED_AH = Pin(0, Pin.OUT)   # LED2 · Active High

# ---------- 시작 상태 · 모든 동작 없음 ----------
LED_AH.value(0)            # 꺼진 상태로 시작

try:
    while True:
        # HIGH · 오래 켜짐 (사용자가 "켜진 상태"라고 느낌)
        LED_AH.value(1)
        sleep(1.5)

        # LOW · 짧게 꺼짐 (전환이 바로 보임)
        LED_AH.value(0)
        sleep(0.3)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    LED_AH.value(0)
