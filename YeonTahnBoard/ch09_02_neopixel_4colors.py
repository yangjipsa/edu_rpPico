"""
Chapter 9. 네오픽셀 · WS2812B
절 9.6 · 4색 표시

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
import neopixel

np = neopixel.NeoPixel(Pin(5), 4)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
for i, c in enumerate(colors):
    np[i] = c
np.write()
