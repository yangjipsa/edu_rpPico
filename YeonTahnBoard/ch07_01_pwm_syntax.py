"""
Chapter 7. PWM · 아날로그 출력
절 7.4 · PWM 문법

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM

pwm = PWM(Pin(0))           # GP0 에 PWM 객체
pwm.freq(1000)              # 주파수 1kHz
pwm.duty_u16(32768)         # 듀티 50% (32768 = 65535 / 2)
