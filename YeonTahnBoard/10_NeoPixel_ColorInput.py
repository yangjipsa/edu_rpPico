# ================================================================
#  파일명    : 10_NeoPixel_ColorInput.py
#  설명      : 사용자 입력으로 네오픽셀 (RGBW) 4개 색상 지정
#             현재 색에서 목표 색으로 서서히 페이드 전환 (선형 보간)
#             Thonny Shell 에서 아래 두 형식 지원 · Ctrl+C 종료
#              · "R,G,B"      → W=0     · 예 · 255,0,0
#              · "R,G,B,W"    → W 직접 · 예 · 0,0,0,180 (순수 백색)
#  참고      : 이 보드의 픽셀은 SK6812 계열 RGBW (4채널 · 32비트).
#             bpp=4 로 설정해야 색·개수가 어긋나지 않음.
#  대상 부품 : SK6812 RGBW × 4 · GP5 · 데이지체인 (U4 ~ U7)
#  보드      : YeonTahn Board V1
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-08-28
# ================================================================

from machine import Pin
from time import sleep_ms
import neopixel

# ---------- 설정 ----------
NUM = 4                           # 픽셀 수 (U4 ~ U7)
np  = neopixel.NeoPixel(Pin(5), NUM, bpp=4)   # RGBW · 4채널

FADE_STEPS = 40                   # 페이드 분할 스텝 수
FADE_DELAY = 15                   # 스텝당 ms  → 총 약 0.6초

# ---------- 밝기 게인 · 0.0 ~ 1.0 ----------
GAIN = 0.15

current = (0, 0, 0, 0)            # 현재 색 (R,G,B,W)

def apply_gain(rgbw):
    r, g, b, w = rgbw
    return (int(r * GAIN), int(g * GAIN),
            int(b * GAIN), int(w * GAIN))

def show(color):
    scaled = apply_gain(color)
    for i in range(NUM):
        np[i] = scaled
    np.write()

def fade_to(target):
    """current 에서 target 으로 선형 보간 페이드 (4채널)."""
    global current
    r0, g0, b0, w0 = current
    r1, g1, b1, w1 = target
    for s in range(1, FADE_STEPS + 1):
        r = r0 + (r1 - r0) * s // FADE_STEPS
        g = g0 + (g1 - g0) * s // FADE_STEPS
        b = b0 + (b1 - b0) * s // FADE_STEPS
        w = w0 + (w1 - w0) * s // FADE_STEPS
        show((r, g, b, w))
        sleep_ms(FADE_DELAY)
    current = target

def parse_color(text):
    """'R,G,B' 또는 'R,G,B,W' 문자열 → (R,G,B,W) 튜플. 0~255 검증."""
    parts = text.replace(" ", "").split(",")
    if len(parts) not in (3, 4):
        raise ValueError("값이 3개(RGB) 또는 4개(RGBW) 여야 합니다")
    vals = [int(p) for p in parts]
    for v in vals:
        if not 0 <= v <= 255:
            raise ValueError("0 ~ 255 사이 값만 가능")
    if len(vals) == 3:
        vals.append(0)            # W 채널 생략 시 0
    return tuple(vals)

# ---------- 시작 상태 · 모든 동작 없음 ----------
show(current)

print("네오픽셀 색상 입력 · Ctrl+C 로 종료")
print("예 · 255,0,0        (빨강 · W=0)")
print("예 · 0,128,255      (파랑 · W=0)")
print("예 · 0,0,0,200      (순수 백색)")

try:
    while True:
        text = input("R,G,B(,W) > ")
        try:
            target = parse_color(text)
        except ValueError as e:
            print("입력 오류 ·", e)
            continue
        fade_to(target)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    show((0, 0, 0, 0))
