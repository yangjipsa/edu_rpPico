# ================================================================
#  파일명    : 12_ADC_POT.py
#  설명      : 가변저항 (POT) 을 읽어 raw · 전압 · 저항값까지 계산
#             POT 은 분압으로 연결되므로 wiper 위치에 따라
#             위쪽 (R_top) · 아래쪽 (R_bot) 저항 비율만 바뀜
#              R_bot = R_TOTAL × (raw / 65535)
#              R_top = R_TOTAL - R_bot
#  준비      : JP1 점퍼를 B - Center (POT) 위치로 이동
#  대상 부품 : 가변저항 (POT) · GP26 · ADC(0)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import ADC
from time import sleep

# ---------- 설정 ----------
adc = ADC(26)               # GP26 · ADC0

VREF    = 3.3               # ADC 기준 전압
FULL    = 65535             # 16-bit 최대값
R_TOTAL = 5_000             # 가변저항 총 저항 · R7 · Alps RK09K1130AU2 · 5kΩ

try:
    while True:
        raw   = adc.read_u16()
        volt  = raw * VREF / FULL
        ratio = raw / FULL
        r_bot = R_TOTAL * ratio
        r_top = R_TOTAL - r_bot

        print(f"raw={raw:5d}  V={volt:.2f}  "
              f"R_bot={r_bot:6.0f} Ω  R_top={r_top:6.0f} Ω")
        sleep(0.3)

except KeyboardInterrupt:
    pass
