"""
Chapter 6. 디지털 입력 · 스위치
절 6.8 · 첫 코드 · 스위치 상태 출력

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

key1 = Pin(3, Pin.IN)    # KEY1 · 풀업 방식 (평상 시 1)

while True:
    val = key1.value()
    print("KEY1 =", val)
    sleep(0.2)
