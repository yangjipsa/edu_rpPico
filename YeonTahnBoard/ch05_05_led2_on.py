"""
Chapter 5. 디지털 출력 · LED
절 5.9 · LED2 켜기 첫 코드

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin      # 1

led = Pin(0, Pin.OUT)         # 2

led.value(1)                  # 3
