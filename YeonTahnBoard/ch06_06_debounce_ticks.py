"""
Chapter 6. 디지털 입력 · 스위치
절 6.10 · 디바운싱 · ticks_ms 방식

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
def stable_read(pin, count=5):
    v = pin.value()
    for _ in range(count):
        sleep_ms(3)
        if pin.value() != v:
            return -1   # 흔들리는 중 → 무효
    return v
