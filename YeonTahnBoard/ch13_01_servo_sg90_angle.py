"""
Chapter 13. 외부 확장
절 13.3 · SG90 서보 각도 제어

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
from machine import Pin, PWM
import time

servo = PWM(Pin(15))
servo.freq(50)             # 50Hz = 20ms 주기

def angle(deg):
    # 0° → 1ms → duty ~ 3277
    # 180° → 2ms → duty ~ 6553
    duty = int(3277 + (deg / 180) * 3276)
    servo.duty_u16(duty)

while True:
    for a in (0, 45, 90, 135, 180):
        angle(a); time.sleep(0.5)
