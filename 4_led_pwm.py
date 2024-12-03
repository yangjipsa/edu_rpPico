from machine import Pin, PWM
import time

# GPIO 핀 설정 (PWM 핀)
led_red = PWM(Pin(2))
led_blu = PWM(Pin(3))

# PWM 주파수 설정, 1kHz로 설정
led_red.freq(1000)
led_blu.freq(1000)

# 메인 루프
try:
    while True:
        # LED 밝기 증가 (0 ~ 1023)
        for duty in range(0, 1024, 10):  # 10씩 증가
            led_red.duty_u16(duty * 64)  # 0~1023을 16비트 범위로 변환
            led_blu.duty_u16((1023 - duty) * 64)  # 반대로 감소
            time.sleep(0.01)

        # LED 밝기 감소 (1023 ~ 0)
        for duty in range(1023, -1, -10):  # 10씩 감소
            led_red.duty_u16(duty * 64)  # 0~1023을 16비트 범위로 변환
            led_blu.duty_u16(1023 * 64 - duty * 64)  # 반대로 증가
            time.sleep(0.01)

except KeyboardInterrupt:
    # 종료 시 LED 끄기
    led_red.duty_u16(0)  # LED Red 끄기
    led_blu.duty_u16(0)  # LED Blue 끄기
    print("Turn off")


