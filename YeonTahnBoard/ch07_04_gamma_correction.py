"""
Chapter 7. PWM · 아날로그 출력
절 7.7 · 감마 보정 (심화)

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
gamma = 2.2
for i in range(0, 101):
    ratio = i / 100
    corrected = int((ratio ** gamma) * 65535)
    pwm.duty_u16(corrected)
    sleep_ms(20)
