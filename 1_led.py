from machine import Pin
import time

# GPIO 핀 설정
led_red = Pin(2, Pin.OUT)
led_blu = Pin(3, Pin.OUT)

# High Signal function
def turnOffLeds(ledPin):
    ledPin.on()

# Low Signal function
def turnOnLeds(ledPin):
    ledPin.off()

# 메인 루프
try:
    timeDelay = 0.2

    while True:
        turnOnLeds(led_red)
        turnOffLeds(led_blu)
        time.sleep(timeDelay)
         
        turnOffLeds(led_red)
        turnOnLeds(led_blu)
        time.sleep(timeDelay)

except KeyboardInterrupt :
    print("Turn off")
