"""
Chapter 11. I²C · SSD1306 OLED
절 11.7 · OLED Hello 표시

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400_000)
oled = SSD1306_I2C(128, 64, i2c)

oled.fill(0)                            # 화면 지우기
oled.text("Hello, YeonTahn!", 0, 0)     # (x=0, y=0)
oled.text("Chapter 11", 0, 16)
oled.show()
