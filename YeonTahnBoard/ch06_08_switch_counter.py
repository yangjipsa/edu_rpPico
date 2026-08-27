"""
Chapter 6. 디지털 입력 · 스위치
절 6.12 · 실습 · 스위치 카운터

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
# 디바운싱 없는 버전 · 실험용
key1 = Pin(3, Pin.IN)
count = 0
prev = 1
while True:
    curr = key1.value()
    if prev == 1 and curr == 0:
        count += 1
        print("count =", count)
    prev = curr
