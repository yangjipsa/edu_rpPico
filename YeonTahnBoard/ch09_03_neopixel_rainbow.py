"""
Chapter 9. 네오픽셀 · WS2812B
절 9.7 · 무지개 애니메이션

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin
import neopixel
from time import sleep_ms

np = neopixel.NeoPixel(Pin(5), 4)

def hsv_to_rgb(h):
    # h: 0~255, s=v=255 로 가정
    i = h // 43
    f = (h - i * 43) * 6
    p = 0; q = (255 * (255 - f)) >> 8; t = (255 * f) >> 8
    if i == 0: return (255, t, 0)
    if i == 1: return (q, 255, 0)
    if i == 2: return (0, 255, t)
    if i == 3: return (0, q, 255)
    if i == 4: return (t, 0, 255)
    if i == 5: return (255, 0, q)

offset = 0
while True:
    for i in range(4):
        np[i] = hsv_to_rgb((offset + i * 64) & 255)
    np.write()
    offset = (offset + 4) & 255
    sleep_ms(30)
