"""
Chapter 6. 디지털 입력 · 스위치
절 6.7 · Pin IN 문법

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
key1 = Pin(3, Pin.IN)                   # 기본 (외부 풀업 사용)
key1 = Pin(3, Pin.IN, Pin.PULL_UP)      # 내장 풀업 활성화
key2 = Pin(4, Pin.IN, Pin.PULL_DOWN)    # 내장 풀다운 활성화
