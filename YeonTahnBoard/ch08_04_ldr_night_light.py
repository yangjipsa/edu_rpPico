"""
Chapter 8. ADC · 아날로그 입력
절 8.9 · LDR · 자동 야간등

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import ADC, Pin
from time import sleep

adc = ADC(26)                # JP1 을 A (LDR) 위치로!
led = Pin(0, Pin.OUT)
THRESHOLD = 45000            # 이 값 이상이면 어둠

while True:
    if adc.read_u16() > THRESHOLD:
        led.value(1)         # 어두우면 켜기
    else:
        led.value(0)
    sleep(0.2)
