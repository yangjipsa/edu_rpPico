"""
Chapter 12. Wi-Fi · NTP
절 12.2 · network 라이브러리 준비

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
import network

wlan = network.WLAN(network.STA_IF)  # STA (스테이션 · 클라이언트)
wlan.active(True)                     # Wi-Fi 켜기
wlan.connect("SSID", "PASSWORD")      # 접속
