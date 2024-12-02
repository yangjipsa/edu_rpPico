from machine import Pin
import time

# 내장 LED 설정 (피코 W에서는 'LED' 사용)
led = Pin('EXT_GPIO0', Pin.OUT)

# 블링크 함수: 지정한 시간 동안 LED를 깜빡이기
def blink(delay):
    while True:
        led.on()   # LED 켜기
        time.sleep(delay)  # delay만큼 대기
        led.off()  # LED 끄기
        time.sleep(delay)  # delay만큼 대기

# 0.5초 간격으로 깜빡이기
blink(0.5)
