"""
Chapter 12. Wi-Fi · NTP
절 12.3 · Wi-Fi 접속 · 대기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
import network
import time

SSID = "your_ssid"
PW   = "your_password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PW)

# 접속 대기
print("접속 중", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)

print()
print("연결됨")
print("IP :", wlan.ifconfig()[0])
