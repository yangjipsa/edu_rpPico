"""
Chapter 6. 디지털 입력 · 스위치
절 6.11 · 스위치 + LED 연동

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep_ms

key1 = Pin(3, Pin.IN)      # KEY1 (풀업 · 평상 시 1)
led  = Pin(0, Pin.OUT)     # LED2 (Active High)

led_state = 0
prev = 1                   # 이전 스위치 상태

while True:
    curr = key1.value()
    # 눌린 순간 (HIGH → LOW) 만 감지
    if prev == 1 and curr == 0:
        led_state = 1 - led_state    # 토글 (0↔1)
        led.value(led_state)
        print("LED", "ON" if led_state else "OFF")
        sleep_ms(50)                  # 디바운싱
    prev = curr
    sleep_ms(10)
