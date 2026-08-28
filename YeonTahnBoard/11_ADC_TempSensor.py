# ================================================================
#  파일명    : 11_ADC_TempSensor.py
#  설명      : Pico 내장 온도센서 (ADC 채널 4) 로 온도 측정
#             내부 다이오드의 순방향 전압이 온도에 따라 변하는 특성을
#             이용. 데이터시트 공식으로 섭씨 온도로 변환
#              T(°C) = 27 - (V - 0.706) / 0.001721
#             정밀도는 ±3°C 수준 (실내 온도 참고용)
#  참고      : 외부 부품 필요 없음 · Pico 내부 회로만 사용
#  대상 부품 : Pico 2W 내장 온도센서 · ADC(4)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import ADC
from time import sleep

# ---------- 핀 설정 ----------
sensor = ADC(4)             # 내장 온도센서 (핀 아님 · 채널 4)

VREF = 3.3                  # ADC 기준 전압
FULL = 65535                # 16-bit 최대값

try:
    while True:
        raw = sensor.read_u16()
        volt = raw * VREF / FULL
        temp = 27 - (volt - 0.706) / 0.001721

        print(f"raw={raw:5d}  V={volt:.3f}  T={temp:5.2f} °C")
        sleep(1)

except KeyboardInterrupt:
    pass
