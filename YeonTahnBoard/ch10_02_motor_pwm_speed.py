"""
Chapter 10. DC 모터 · H-Bridge
절 10.7 · PWM 속도 조절

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM
from time import sleep

ia = PWM(Pin(17))   # 모터1 IA · PWM
ib = Pin(16, Pin.OUT)
ia.freq(1000)

# 50% 정회전
ib.value(0)
ia.duty_u16(32768)
sleep(2)

# 100% 정회전
ia.duty_u16(65535)
sleep(2)

# 정지
ia.duty_u16(0)
