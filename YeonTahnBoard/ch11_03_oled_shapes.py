"""
Chapter 11. I²C · SSD1306 OLED
절 11.8 · OLED 도형 그리기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
oled.pixel(64, 32, 1)              # 점
oled.hline(0, 40, 128, 1)          # 가로선
oled.vline(64, 0, 64, 1)           # 세로선
oled.rect(10, 10, 50, 30, 1)       # 사각형 (테두리)
oled.fill_rect(70, 10, 50, 30, 1)  # 사각형 (채움)
oled.show()
