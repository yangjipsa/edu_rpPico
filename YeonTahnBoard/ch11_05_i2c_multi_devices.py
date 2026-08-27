"""
Chapter 11. I²C · SSD1306 OLED
절 11.10 · 여러 I²C 장치 동시 사용

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
# 예: OLED (0x3C) + 온도센서 BME280 (0x76)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400_000)
devs = i2c.scan()
# ['0x3c', '0x76'] 두 개 모두 나오면 성공
