from machine import Pin
import time

# GPIO 핀 설정
LED = [Pin(2, Pin.OUT),Pin(3, Pin.OUT),Pin(4, Pin.OUT),Pin(5, Pin.OUT)]

numLEDs = len(LED)

# LED를 켜는 함수
def turnOffLeds(*ledPin):
    for i in ledPin:
        LED[i].on()

# LED를 끄는 함수
def turnOnLeds(*ledPin):
    for i in ledPin:
        LED[i].off()


# 메인 루프
try:
    
  timeDelay = 0.1

  while True:
    turnOnLeds(0,2)
    turnOffLeds(1,3)
    time.sleep(timeDelay)
     
    turnOnLeds(1,3)
    turnOffLeds(0,2)
    time.sleep(timeDelay)

    
except KeyboardInterrupt :
    print("Turn off")
