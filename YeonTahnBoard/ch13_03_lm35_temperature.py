"""
Chapter 13. 외부 확장
절 13.5 · LM35 온도 측정

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import ADC
import time

sensor = ADC(26)               # GP26 · ADC0

while True:
    raw = sensor.read_u16()
    voltage = raw * 3.3 / 65535
    temp_c = voltage / 0.01    # 10mV = 1°C
    print(f"온도: {temp_c:.1f} °C")
    time.sleep(1)
