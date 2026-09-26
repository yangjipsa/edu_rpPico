# ================================================================
#  파일명    : 17_PIO_Blink.py
#  설명      : PIO(Programmable I/O) 첫 예제.
#             CPU 가 아니라 PIO(State Machine)가 스스로 LED 를 깜빡인다.
#             sm.active(1) 이후 CPU 는 print 로 놀고 있어도 LED 는
#             계속 깜빡임 → "핀 제어를 알바생(PIO)에게 떠넘긴다"는 감각.
#
#             두 가지를 보여준다:
#              A) fast_blink : 단순 4줄. 너무 빨라 눈엔 떨림으로 보임
#              B) slow_blink : 대기 루프로 약 1초에 한 번 (권장)
#             MODE 로 골라 실행.
#  참고      : 자세한 개념은 GUIDE_PIO.md 참고.
#             LED2(GP0)=Active High → 1=켜짐.
#  대상 부품 : LED2 (GP0)
#  보드      : YeonTahn Board V1 (Raspberry Pi Pico 2W)
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-09-26
# ================================================================

import rp2
from machine import Pin
import time

LED_PIN = 0                 # LED2 = GP0 (Active High)
MODE    = "slow"           # "slow"(약 1초) 또는 "fast"(빠른 떨림)


# ---------- A) 단순 깜빡임 (너무 빨라 떨림으로 보임) ----------
#  한 사이클 = 128박자. freq=2000 → 128/2000 = 0.064초 → 1초에 약 15번.
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def fast_blink():
    wrap_target()
    set(pins, 1)   [31]     # 켜기 + 31박자
    nop()          [31]     # 더 켜두기
    set(pins, 0)   [31]     # 끄기 + 31박자
    nop()          [31]     # 더 꺼두기
    wrap()


# ---------- B) 천천히 깜빡임 (약 1초에 한 번, 권장) ----------
#  대기 루프로 시간을 크게 늘린다.
#  켜짐: set(x,31) 후 (nop[31]+jmp) 를 32번 ≈ 1000박자, 꺼짐도 동일.
#  freq=2000 → 한 사이클 약 2000박자 ≈ 1초.
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def slow_blink():
    wrap_target()
    set(pins, 1)            # LED 켜기
    set(x, 31)              # 바깥 카운터 x=31
    label("on_delay")
    nop()          [31]     # 32박자 대기
    jmp(x_dec, "on_delay")  # x 1 줄이고, 0 아니면 반복

    set(pins, 0)            # LED 끄기
    set(x, 31)
    label("off_delay")
    nop()          [31]
    jmp(x_dec, "off_delay")
    wrap()


# ---------- 실행 ----------
prog = slow_blink if MODE == "slow" else fast_blink
sm = rp2.StateMachine(0, prog, freq=2000, set_base=Pin(LED_PIN))

print("PIO 시작 — LED2(GP0)가", "약 1초에 한 번" if MODE == "slow" else "빠르게", "깜빡입니다.")
print("(LED 는 PIO 가, 아래 카운트는 CPU 가 → 동시에 동작)")
sm.active(1)

try:
    n = 0
    while True:
        print("  CPU 는 다른 일 하는 중 ...", n)
        n += 1
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    sm.active(0)                       # 알바생 정지
    Pin(LED_PIN, Pin.OUT).value(0)    # LED 끄기
    print("종료: PIO 정지, LED OFF")
