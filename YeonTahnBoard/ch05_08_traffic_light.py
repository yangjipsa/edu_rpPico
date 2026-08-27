"""
Chapter 5. 디지털 출력 · LED
절 5.12 · 실습 · 신호등 만들기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

red    = Pin(0, Pin.OUT)   # LED2
yellow = Pin(1, Pin.OUT)   # LED3 (노랑 대용)
green  = Pin(2, Pin.OUT)   # LED4 (Active Low)

def all_off():
    red.value(0); yellow.value(0); green.value(1)

while True:
    # 1) 빨강
    all_off(); red.value(1)
    sleep(3)
    
    # 2) 초록
    all_off(); green.value(0)
    sleep(3)
    
    # 3) 초록 깜빡임
    for _ in range(3):
        green.value(1); sleep(0.3)
        green.value(0); sleep(0.3)
    
    # 4) 노랑
    all_off(); yellow.value(1)
    sleep(1)
