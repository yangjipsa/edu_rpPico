"""
Chapter 11. I²C · SSD1306 OLED
절 11.6 · I²C 스캔 · 주소 확인

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400_000)
devices = i2c.scan()
print("발견:", [hex(d) for d in devices])
# 예: 발견: ['0x3c']
