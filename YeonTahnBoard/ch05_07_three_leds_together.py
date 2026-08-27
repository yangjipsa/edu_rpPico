"""
Chapter 5. 디지털 출력 · LED
절 5.11 · 세 LED 동시 제어

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

led2 = Pin(0, Pin.OUT)   # Red · Active High
led3 = Pin(1, Pin.OUT)   # Red · Active High
led4 = Pin(2, Pin.OUT)   # Green · Active Low

while True:
    # 세 LED 모두 켜기
    led2.value(1)   # 1 = 켜짐 (Active High)
    led3.value(1)
    led4.value(0)   # 0 = 켜짐 (Active Low)
    sleep(0.5)
    
    # 세 LED 모두 끄기
    led2.value(0)
    led3.value(0)
    led4.value(1)   # 1 = 꺼짐 (Active Low)
    sleep(0.5)
