# ================================================================
#  파일명    : 06_SW_PU_LED_AL.py
#  설명      : 풀업 스위치로 Active Low LED 켜기
#             풀업 스위치와 AL LED 는 신호 극성이 자연스럽게 맞음
#              · 안 누름 → SW = 1 → LED value(1) → AL 이므로 꺼짐
#              · 누름   → SW = 0 → LED value(0) → AL 이므로 켜짐
#             스위치 값을 그대로 LED 에 흘려주는 한 줄로 해결
#  대상 부품 : KEY1  (GP3) · 풀업 스위치
#             LED4  (GP2) · Active Low LED
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep

# ---------- 핀 설정 ----------
SW_PU  = Pin(3, Pin.IN)    # KEY1 · 풀업
LED_AL = Pin(2, Pin.OUT)   # LED4 · Active Low

# ---------- 시작 상태 · 모든 동작 없음 ----------
LED_AL.value(1)            # AL · 1 = 꺼짐

try:
    while True:
        LED_AL.value(SW_PU.value())   # 스위치 값 = LED 입력값
        sleep(0.02)                   # CPU 여유 · 반응성 유지

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    LED_AL.value(1)        # AL · 1 = 꺼짐
