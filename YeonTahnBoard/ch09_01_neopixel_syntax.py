"""
Chapter 9. 네오픽셀 · WS2812B
절 9.5 · neopixel 라이브러리 문법

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
import neopixel

NUM = 4
np = neopixel.NeoPixel(Pin(5), NUM)   # GP5, 4개

np[0] = (255, 0, 0)         # 첫 번째 = 빨강 (RGB 자동 변환)
np[1] = (0, 255, 0)         # 초록
np[2] = (0, 0, 255)         # 파랑
np[3] = (255, 255, 0)       # 노랑
np.write()                   # 실제로 전송
