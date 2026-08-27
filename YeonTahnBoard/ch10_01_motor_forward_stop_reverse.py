"""
Chapter 10. DC 모터 · H-Bridge
절 10.6 · 정회전 · 정지 · 역회전

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
from time import sleep

ia = Pin(17, Pin.OUT)      # 모터1 IA
ib = Pin(16, Pin.OUT)      # 모터1 IB

# 정회전 2초
ia.value(1); ib.value(0)
sleep(2)

# 정지 1초
ia.value(0); ib.value(0)
sleep(1)

# 역회전 2초
ia.value(0); ib.value(1)
sleep(2)

# 정지
ia.value(0); ib.value(0)
