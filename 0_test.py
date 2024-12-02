from machine import Pin
import time

# 내장 LED 설정 (피코 W에서는 'LED' 사용)
led = Pin('EXT_GPIO0', Pin.OUT)

try:
    delay = 0.5
    
    while True:
        led.on()   # LED 켜기
        time.sleep(delay)  # delay만큼 대기
        led.off()  # LED 끄기
        time.sleep(delay)  # delay만큼 대기

except KeyboardInterrupt :
    print("Turn Off")
    
