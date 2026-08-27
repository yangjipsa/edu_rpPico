"""
Chapter 8. ADC · 아날로그 입력
절 8.8 · POT 로 LED 밝기 조절

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import ADC, Pin, PWM

adc = ADC(26)               # JP1 을 B (POT) 위치로!
led = PWM(Pin(0)); led.freq(1000)

while True:
    led.duty_u16(adc.read_u16())
