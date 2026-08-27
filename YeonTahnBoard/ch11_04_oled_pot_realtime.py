"""
Chapter 11. I²C · SSD1306 OLED
절 11.9 · OLED · POT 실시간 표시

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from time import sleep

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400_000)
oled = SSD1306_I2C(128, 64, i2c)
adc = ADC(26)               # JP1 = B (POT)

while True:
    val = adc.read_u16()
    voltage = val * 3.3 / 65535
    
    oled.fill(0)
    oled.text("POT Reading", 0, 0)
    oled.text(f"raw : {val}", 0, 20)
    oled.text(f"V   : {voltage:.2f}", 0, 36)
    oled.show()
    sleep(0.1)
