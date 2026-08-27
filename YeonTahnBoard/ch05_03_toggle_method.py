"""
Chapter 5. 디지털 출력 · LED
절 5.8 · toggle() 로 상태 반전

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
led.value(1)          # HIGH 로 설정 → Active High LED 켜짐
led.value(0)          # LOW  로 설정 → Active High LED 꺼짐
current = led.value() # 현재 상태 읽기 (0 또는 1)
