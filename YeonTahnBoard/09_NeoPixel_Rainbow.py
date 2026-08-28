# ================================================================
#  파일명    : 09_NeoPixel_Rainbow.py
#  설명      : 네오픽셀 (RGBW) 4개로 무지개 파도 애니메이션
#             HSV 색공간의 hue 만 시간에 따라 순환
#             각 픽셀은 서로 다른 hue offset 을 가져
#             U4 → U5 → U6 → U7 순으로 색이 흘러가듯 보임
#             W (백색) 채널은 0 으로 두어 순수한 컬러만 표현
#  참고      : 이 보드의 픽셀은 SK6812 계열 RGBW (4채널 · 32비트).
#             일반 WS2812B RGB (3채널 · 24비트) 로 설정하면 데이터가
#             밀려 색·개수 모두 어긋남 → 반드시 bpp=4 사용.
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

OFFSET_PER_PIXEL = 32             # 픽셀 간 hue 차이 · 시차 느낌
BASE_STEP        = 2              # base hue 증가량 · 작을수록 부드러움
DELAY_MS         = 30             # 프레임 간격

# ---------- 밝기 게인 · 0.0 ~ 1.0 ----------
#  값이 클수록 눈부심 · 낮게 두면 은은한 무드등
GAIN = 0.15

def hsv_to_rgb(h):
    """h : 0~255 · S=V=최대. 6개 구간 선형 보간."""
    i = h // 43
    f = (h - i * 43) * 6
    q = (255 * (255 - f)) >> 8
    t = (255 * f) >> 8
    if i == 0: return (255, t, 0)
    if i == 1: return (q, 255, 0)
    if i == 2: return (0, 255, t)
    if i == 3: return (0, q, 255)
    if i == 4: return (t, 0, 255)
    return (255, 0, q)

def apply_gain(rgb):
    """(R,G,B) 튜플에 밝기 게인 적용 → (R,G,B,W) 로 변환. W=0."""
    r, g, b = rgb
    return (int(r * GAIN), int(g * GAIN), int(b * GAIN), 0)

def clear():
    for i in range(NUM):
        np[i] = (0, 0, 0, 0)
    np.write()

# ---------- 시작 상태 · 모든 동작 없음 ----------
clear()

try:
    base = 0
    while True:
        for i in range(NUM):
            hue = (base + i * OFFSET_PER_PIXEL) & 0xFF
            np[i] = apply_gain(hsv_to_rgb(hue))
        np.write()
        base = (base + BASE_STEP) & 0xFF
        sleep_ms(DELAY_MS)

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    clear()
