"""
Chapter 13. 외부 확장
절 13.4 · 부저 · 학교종 멜로디

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM
import time

buzzer = PWM(Pin(14))

def tone(freq, ms):
    if freq == 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(32768)     # 50% duty
    time.sleep_ms(ms)
    buzzer.duty_u16(0)
    time.sleep_ms(30)

# "학교종" 첫 소절
song = [(392, 400), (392, 400), (440, 400), (440, 400),
        (392, 400), (392, 400), (330, 800)]

for f, d in song:
    tone(f, d)
