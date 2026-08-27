"""
Chapter 8. ADC · 아날로그 입력
절 8.7 · ADC 값 읽어 출력

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import ADC
from time import sleep

adc = ADC(26)

while True:
    raw = adc.read_u16()
    v = raw * 3.3 / 65535
    print(f"raw={raw:5d}  V={v:.2f}")
    sleep(0.5)
