from machine import ADC
import time

# 내부 온도 센서 초기화 (ADC4 채널에 연결)
sensor_temp = ADC(4)

# 섭씨 온도 계산에 필요한 상수
CONVERSION_FACTOR = 3.3 / (65535)  # 16비트 ADC의 분해능과 전압 기준 (3.3V)

while True:
    # ADC 값을 읽기
    raw_value = sensor_temp.read_u16()
    
    # 전압으로 변환
    voltage = raw_value * CONVERSION_FACTOR
    
    # 온도 계산 (공식은 데이터시트를 참조)
    temperature = 27 - (voltage - 0.706) / 0.001721
    
    # 온도 출력
    print(f"Temperature: {temperature:.2f} °C")
    
    # 1초 대기
    time.sleep(1)

