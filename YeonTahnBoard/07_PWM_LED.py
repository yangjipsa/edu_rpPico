# ================================================================
#  파일명    : 07_PWM_LED.py
#  설명      : PWM 을 이용한 LED 밝기 조절 예제
#             비교를 위해 GP0 LED 는 항상 최대 밝기로 켜 두고
#             GP1 LED 만 PWM duty 를 서서히 바꿔 밝아졌다 어두워짐
#             두 LED 밝기 차이를 눈으로 비교
#  대상 부품 : GP0 (LED2) · Active High · 항상 켜짐 (비교군)
#             GP1 (LED3) · Active High · PWM 페이드
#             GP2 (LED4) · 사용 안 함 · 꺼진 상태 유지
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin, PWM
from time import sleep_ms

# ---------- 핀 설정 ----------
LED_REF  = Pin(0, Pin.OUT)        # GP0 · 비교군 · 상시 켜짐
LED_PWM  = PWM(Pin(1))            # GP1 · PWM 대상
LED_OFF  = Pin(2, Pin.OUT)        # GP2 · 사용 안 함 (AL)

LED_PWM.freq(1000)                # 1kHz · 눈에 깜빡임 안 보임

# ---------- 시작 상태 · 모든 동작 없음 ----------
LED_REF.value(0)                  # AH · 0 = 꺼짐
LED_PWM.duty_u16(0)               # duty 0 = 꺼짐
LED_OFF.value(1)                  # AL · 1 = 꺼짐

# ---------- 비교군 켜기 ----------
LED_REF.value(1)                  # 상시 최대 밝기

STEP  = 512                       # duty 증감 스텝 (65535 / 128)
DELAY = 10                        # ms · 한 스텝 유지 시간

try:
    while True:
        # 페이드 인 · 어두움 → 밝음
        for duty in range(0, 65536, STEP):
            LED_PWM.duty_u16(duty)
            sleep_ms(DELAY)

        # 페이드 아웃 · 밝음 → 어두움
        for duty in range(65535, -1, -STEP):
            LED_PWM.duty_u16(duty)
            sleep_ms(DELAY)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    LED_PWM.duty_u16(0)
    LED_PWM.deinit()              # PWM 자원 해제
    LED_REF.value(0)
    LED_OFF.value(1)
