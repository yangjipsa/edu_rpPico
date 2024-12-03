import time
from machine import Pin
import neopixel

# GPIO 핀 설정 및 NeoPixel 초기화
NEOPIXEL_PIN = 9  # GPIO 9번 핀
NUM_PIXELS = 4   # NeoPixel LED 개수

# NeoPixel 객체 생성
pixel = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# 색상 설정 함수 (R, G, B 값 설정)
def set_color(r, g, b):
    for i in range(NUM_PIXELS):
        pixel[i] = (r, g, b)  # 각 LED에 RGB 값 설정
    pixel.write()  # LED에 색상 데이터 전송

# 메인 코드
try:
    while True:
        # 1. 빨강, 초록, 파랑 순서로 색 변경
        set_color(255, 0, 0)  # 빨강
        time.sleep(1)
        set_color(0, 255, 0)  # 초록
        time.sleep(1)
        set_color(0, 0, 255)  # 파랑
        time.sleep(1)

except KeyboardInterrupt:
    # 종료 시 모든 LED 끄기
    set_color(0, 0, 0)
    print("Program stopped")

