"""
Chapter 7. PWM · 아날로그 출력
절 7.5 · 50% 밝기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM

led = PWM(Pin(0))       # LED2
led.freq(1000)
led.duty_u16(32768)     # 50% → 반 밝기
