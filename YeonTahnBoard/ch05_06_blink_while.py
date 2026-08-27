"""
Chapter 5. 디지털 출력 · LED
절 5.10 · while 루프 · sleep 으로 깜빡이

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

led = Pin(0, Pin.OUT)

while True:                # 무한 반복
    led.value(1)           # 켜기
    sleep(0.5)             # 0.5초 대기
    led.value(0)           # 끄기
    sleep(0.5)             # 0.5초 대기
