from machine import Pin
import time

# GPIO 핀 설정
sw_red = Pin(18, Pin.IN, Pin.PULL_UP)
sw_blu = Pin(19, Pin.IN, Pin.PULL_UP)

def readSWs():
    tempValSW=[]
    for i in range(numSWs):
        tempValSW.append(SW[i].value())
        
    return tempValSW

# 메인 루프
try:
    while True:
        valSW_red = sw_red.value()
        valSW_blu = sw_blu.value()
        time.sleep(0.01)
        
        print(f"redSW : {valSW_red} | bluSW : {valSW_blu}")
        
except KeyboardInterrupt :
    print("Turn off")
