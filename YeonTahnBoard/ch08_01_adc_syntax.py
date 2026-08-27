"""
Chapter 8. ADC · 아날로그 입력
절 8.6 · ADC 문법

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import ADC

adc = ADC(26)                # GP26 = ADC0
raw = adc.read_u16()          # 0 ~ 65535 정수
voltage = raw * 3.3 / 65535   # 실제 전압 (V)
