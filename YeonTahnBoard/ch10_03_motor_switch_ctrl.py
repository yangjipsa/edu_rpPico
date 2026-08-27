"""
Chapter 10. DC 모터 · H-Bridge
절 10.8 · 스위치로 모터 제어

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM
from time import sleep_ms

key1 = Pin(3, Pin.IN)   # KEY1 · 풀업
key2 = Pin(4, Pin.IN)   # KEY2 · 풀다운
ia = PWM(Pin(17)); ia.freq(1000)
ib = PWM(Pin(16)); ib.freq(1000)

while True:
    if key1.value() == 0:       # KEY1 누르면 정회전
        ia.duty_u16(45000); ib.duty_u16(0)
    elif key2.value() == 1:     # KEY2 누르면 역회전
        ia.duty_u16(0); ib.duty_u16(45000)
    else:                        # 아무것도 안 누르면 정지
        ia.duty_u16(0); ib.duty_u16(0)
    sleep_ms(50)
