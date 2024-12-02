from machine import Pin
import time

# GPIO 핀 설정
SW  = [Pin(6, Pin.IN),Pin(7, Pin.IN),Pin(8, Pin.IN),Pin(9, Pin.IN)]

numSWs  = len(SW)


def readSWs():
    tempValSW=[]
    for i in range(numSWs):
        tempValSW.append(SW[i].value())
        
    return tempValSW

# 메인 루프
try:

    while True:
        valSWs = readSWs()
        #print(valSWs)
        time.sleep(0.01)
        
        for i in range(numSWs) :
            if not valSWs[i] :
                print("sw",i,"on")
            else :
                print("sw",i,"off")

    
except KeyboardInterrupt :
    print("Turn off")
