from machine import Pin, time_pulse_us
import time

# 핀 설정
TRIG_PIN = 6  # TRIG 핀 연결 (GPIO 6번)
ECHO_PIN = 7  # ECHO 핀 연결 (GPIO 7번)

# GPIO 핀 초기화
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def measure_distance():
    # 트리거 신호 초기화
    trig.low()
    time.sleep_us(2)
    # 트리거 신호 발생 (10μs HIGH)
    trig.high()
    time.sleep_us(10)
    trig.low()
    # 에코 신호의 HIGH 지속 시간 측정
    pulse_duration = time_pulse_us(echo, 1, 30000)  # 최대 30ms 대기
    # 거리를 계산 (음속: 343 m/s -> 0.0343 cm/μs)
    distance = (pulse_duration * 0.0343) / 2  # 왕복 시간을 나눔
    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)  # 1초 간격으로 측정

except KeyboardInterrupt:
    print("Measurement stopped")

