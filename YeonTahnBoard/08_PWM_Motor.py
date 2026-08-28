# ================================================================
#  파일명    : 08_PWM_Motor.py
#  설명      : PWM 으로 DC 모터 속도 · 방향 제어 예제
#              · 정회전  30% → 60% → 100% 로 3단 가속
#              · 정지 후 방향 전환
#              · 역회전  30% → 60% → 100% 로 3단 가속
#              · 정지 후 반복
#             L9110 은 IA·IB 두 핀으로 방향을 결정하고
#             한쪽 핀의 PWM duty 로 속도를 조절
#  대상 부품 : 모터 1 (CN1)
#              · IA · GP17 · PWM
#              · IB · GP16 · PWM
#  준비      : CN1 커넥터에 DC 모터 1개를 연결
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin, PWM
from time import sleep, sleep_ms

# ---------- PWM 설정 ----------
IA = PWM(Pin(17))          # 모터1 IA
IB = PWM(Pin(16))          # 모터1 IB
IA.freq(1000)              # 1kHz · 500~5000Hz 권장 범위 안
IB.freq(1000)

# 듀티 표 · 백분율 → 16-bit 값
def duty(percent):
    return int(65535 * percent / 100)

# 정회전 · IA 에 duty · IB = 0
def forward(percent):
    IB.duty_u16(0)
    IA.duty_u16(duty(percent))
    print(f"정회전 · {percent:3d}%")

# 역회전 · IA = 0 · IB 에 duty
def reverse(percent):
    IA.duty_u16(0)
    IB.duty_u16(duty(percent))
    print(f"역회전 · {percent:3d}%")

# 정지 · 둘 다 0
def stop():
    IA.duty_u16(0)
    IB.duty_u16(0)
    print("정지")

# ---------- 시작 상태 · 모든 동작 없음 ----------
stop()

SPEEDS = (30, 60, 100)     # 3단 속도

try:
    while True:
        # ---------- 정회전 3단 ----------
        for p in SPEEDS:
            forward(p)
            sleep(1.5)

        stop()
        sleep(1)            # 방향 전환 전 잠깐 정지 (급역전 방지)

        # ---------- 역회전 3단 ----------
        for p in SPEEDS:
            reverse(p)
            sleep(1.5)

        stop()
        sleep(1)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    IA.duty_u16(0)
    IB.duty_u16(0)
    IA.deinit()
    IB.deinit()
