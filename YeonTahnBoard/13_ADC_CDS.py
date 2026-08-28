# ================================================================
#  파일명    : 13_ADC_CDS.py
#  설명      : CDS (LDR · 조도센서) 값 읽기 · raw 만 출력
#             빛이 많을수록 · 어두울수록 값이 어떻게 변하는지 관찰
#  준비      : JP1 점퍼를 A - Center (LDR) 위치로 이동
#  대상 부품 : CDS 조도센서 (LDR) · GP26 · ADC(0)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import ADC
from time import sleep

# ---------- 설정 ----------
adc = ADC(26)               # GP26 · ADC0

try:
    while True:
        raw = adc.read_u16()
        print(f"CDS raw: {raw}")
        sleep(0.3)

except KeyboardInterrupt:
    pass
