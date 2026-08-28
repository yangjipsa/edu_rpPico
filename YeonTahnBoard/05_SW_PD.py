# ================================================================
#  파일명    : 05_SW_PD.py
#  설명      : 풀다운 (Pull-Down) 스위치 상태 읽기
#             평상시 · 풀다운 저항으로 GPIO 가 LOW  → 0 출력
#             누름   · 스위치가 3V3 로 당김        → 1 출력
#             Thonny Shell 에서 값 변화를 실시간 확인
#  대상 부품 : KEY2 (GP4) · 온보드 풀다운 스위치
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep

# ---------- 핀 설정 ----------
SW_PD = Pin(4, Pin.IN)     # KEY2 · 외부 풀다운 저항 내장

# ---------- 시작 상태 · 별도 출력 동작 없음 ----------
try:
    while True:
        print(SW_PD.value())   # 가만히 있으면 0 · 누르면 1
        sleep(0.2)

except KeyboardInterrupt:
    pass
