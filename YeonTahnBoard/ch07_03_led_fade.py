"""
Chapter 7. PWM · 아날로그 출력
절 7.6 · 페이드 · 부드러운 밝기 변화

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(0))
pwm.freq(1000)

while True:
    # 밝아짐
    for duty in range(0, 65536, 1000):
        pwm.duty_u16(duty)
        sleep(0.02)
    # 어두워짐
    for duty in range(65535, -1, -1000):
        pwm.duty_u16(duty)
        sleep(0.02)
