"""
Chapter 6. 디지털 입력 · 스위치
절 6.10 · 디바운싱 · sleep 방식

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep_ms

key1 = Pin(3, Pin.IN)
prev = 1                          # 이전 상태 기억 (평상 시 1)

while True:
    curr = key1.value()
    if prev == 1 and curr == 0:   # HIGH → LOW 전이 = 눌린 순간
        print("눌림 감지!")
        sleep_ms(50)              # 50ms 채터링 무시
    prev = curr
    sleep_ms(10)
