from machine import Pin, PWM
import time

# SG90은 약 50Hz (20ms 주기), GPIO 2는 D2에 해당
servo = PWM(Pin(2))
servo.freq(50)

# Pico에서는 duty_u16 (0 ~ 65535) 기준
def set_angle(angle):
    # angle (0~180) → duty_u16 (1638 ~ 8192)
    min_duty = 1638  # 약 0.5ms
    max_duty = 8192   # 약 2.5ms
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

while True:
    set_angle(0)
    time.sleep(1)
    set_angle(90)
    time.sleep(1)
    set_angle(180)
    time.sleep(1)
