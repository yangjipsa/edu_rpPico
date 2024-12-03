from machine import Pin
import time

# GPIO 핀 설정
led_red = Pin(2, Pin.OUT)
led_blu = Pin(3, Pin.OUT)

sw_red = Pin(18, Pin.IN, Pin.PULL_UP)
sw_blu = Pin(19, Pin.IN, Pin.PULL_UP)

# 메인 루프
try:
    while True:
        valSW_red = sw_red.value()
        valSW_blu = sw_blu.value()
        time.sleep(0.01)
        
        if (not valSW_red) :
            led_red.off() # led on
        else:
            led_red.on() # led off
        
        if (not valSW_blu) :
            led_blu.off() # led on
        else:
            led_blu.on() # led off

except KeyboardInterrupt :
    print("Turn off")

