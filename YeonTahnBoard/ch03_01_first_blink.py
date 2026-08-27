"""
Chapter 3. 개발 환경 준비
절 3.4 · 첫 실행 · 온보드 LED 깜빡이기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)   # Pico 2W 온보드 LED

while True:
    led.value(1)   # 켜기
    sleep(0.5)
    led.value(0)   # 끄기
    sleep(0.5)
