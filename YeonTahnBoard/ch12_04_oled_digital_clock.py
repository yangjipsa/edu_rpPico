"""
Chapter 12. Wi-Fi · NTP
절 12.5 · OLED 디지털 시계

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
import network, ntptime, time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Wi-Fi 접속
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "PW")
while not wlan.isconnected():
    time.sleep(0.5)

# 시간 동기
ntptime.settime()

# OLED 준비
i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = SSD1306_I2C(128, 64, i2c)

# 시계 표시
while True:
    kst = time.localtime(time.time() + 9 * 3600)
    date = f"{kst[0]}-{kst[1]:02d}-{kst[2]:02d}"
    tstr = f"{kst[3]:02d}:{kst[4]:02d}:{kst[5]:02d}"
    
    oled.fill(0)
    oled.text("Digital Clock", 0, 0)
    oled.text(date, 0, 20)
    oled.text(tstr, 0, 40)
    oled.show()
    time.sleep(1)
