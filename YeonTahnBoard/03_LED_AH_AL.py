# ================================================================
#  파일명    : 03_LED_AH_AL.py
#  설명      : Active High LED · Active Low LED 동시 제어 예제
#             같은 신호(HIGH/LOW)에도 두 LED 가 서로 반대로 동작함을
#             한 화면에서 비교
#              1) 같은 값 넣기   → 두 LED 상태 반대
#              2) 반대 값 넣기   → 두 LED 함께 켜짐 / 꺼짐
#  대상 부품 : LED2 (GP0) · Active High
#             LED4 (GP2) · Active Low
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep

# ---------- 핀 설정 ----------
LED_AH = Pin(0, Pin.OUT)   # LED2 · Active High
LED_AL = Pin(2, Pin.OUT)   # LED4 · Active Low

# ---------- 시작 상태 · 모든 동작 없음 ----------
LED_AH.value(0)            # AH · 0 = 꺼짐
LED_AL.value(1)            # AL · 1 = 꺼짐

try:
    while True:
        # -------- 1) 같은 값 (1) → 서로 반대로 보임 --------
        LED_AH.value(1)    # AH · 켜짐
        LED_AL.value(1)    # AL · 꺼짐
        sleep(1.5)

        # -------- 2) 같은 값 (0) → 반대로 뒤바뀜 --------
        LED_AH.value(0)    # AH · 꺼짐
        LED_AL.value(0)    # AL · 켜짐
        sleep(1.5)

        # -------- 3) 반대 값 넣어 함께 켜기 --------
        LED_AH.value(1)    # AH · 켜짐
        LED_AL.value(0)    # AL · 켜짐  → 둘 다 ON
        sleep(1.5)

        # -------- 4) 반대 값 넣어 함께 끄기 --------
        LED_AH.value(0)    # AH · 꺼짐
        LED_AL.value(1)    # AL · 꺼짐  → 둘 다 OFF
        sleep(1.5)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    LED_AH.value(0)
    LED_AL.value(1)
