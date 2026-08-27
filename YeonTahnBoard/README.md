# YeonTahn Board · 예제 코드

TouchLabs 가 만든 라즈베리 파이 Pico 2W 기반 교육 보드 **YeonTahn Board V1** 의 강의 자료 예제 코드입니다.

전체 강의 자료 (마크다운) · PPT 는 별도 저장소에서 관리됩니다.

## 파일 명명 규칙

```
ch{챕터}_{순서}_{이름}.py
```

정렬하면 강의 순서대로 나옵니다.

## 챕터 · 예제 목록


### Chapter 3. 개발 환경 준비

- `ch03_01_first_blink.py` · 절 3.4 · 첫 실행 · 온보드 LED 깜빡이기

### Chapter 5. 디지털 출력 · LED

- `ch05_01_pin_out_syntax.py` · 절 5.8 · Pin OUT 문법
- `ch05_02_value_method.py` · 절 5.8 · value() 로 HIGH · LOW 지정
- `ch05_03_toggle_method.py` · 절 5.8 · toggle() 로 상태 반전
- `ch05_04_on_off_method.py` · 절 5.8 · on() / off() 편의 메서드
- `ch05_05_led2_on.py` · 절 5.9 · LED2 켜기 첫 코드
- `ch05_06_blink_while.py` · 절 5.10 · while 루프 · sleep 으로 깜빡이
- `ch05_07_three_leds_together.py` · 절 5.11 · 세 LED 동시 제어
- `ch05_08_traffic_light.py` · 절 5.12 · 실습 · 신호등 만들기

### Chapter 6. 디지털 입력 · 스위치

- `ch06_01_internal_pullup.py` · 절 6.6 · 내장 풀업 활용
- `ch06_02_pin_in_syntax.py` · 절 6.7 · Pin IN 문법
- `ch06_03_read_switch_state.py` · 절 6.7 · 스위치 상태 읽기
- `ch06_04_first_switch_code.py` · 절 6.8 · 첫 코드 · 스위치 상태 출력
- `ch06_05_debounce_sleep.py` · 절 6.10 · 디바운싱 · sleep 방식
- `ch06_06_debounce_ticks.py` · 절 6.10 · 디바운싱 · ticks_ms 방식
- `ch06_07_switch_led_link.py` · 절 6.11 · 스위치 + LED 연동
- `ch06_08_switch_counter.py` · 절 6.12 · 실습 · 스위치 카운터

### Chapter 7. PWM · 아날로그 출력

- `ch07_01_pwm_syntax.py` · 절 7.4 · PWM 문법
- `ch07_02_pwm_50_percent.py` · 절 7.5 · 50% 밝기
- `ch07_03_led_fade.py` · 절 7.6 · 페이드 · 부드러운 밝기 변화
- `ch07_04_gamma_correction.py` · 절 7.7 · 감마 보정 (심화)

### Chapter 8. ADC · 아날로그 입력

- `ch08_01_adc_syntax.py` · 절 8.6 · ADC 문법
- `ch08_02_adc_read_print.py` · 절 8.7 · ADC 값 읽어 출력
- `ch08_03_pot_led_brightness.py` · 절 8.8 · POT 로 LED 밝기 조절
- `ch08_04_ldr_night_light.py` · 절 8.9 · LDR · 자동 야간등

### Chapter 9. 네오픽셀 · WS2812B

- `ch09_01_neopixel_syntax.py` · 절 9.5 · neopixel 라이브러리 문법
- `ch09_02_neopixel_4colors.py` · 절 9.6 · 4색 표시
- `ch09_03_neopixel_rainbow.py` · 절 9.7 · 무지개 애니메이션

### Chapter 10. DC 모터 · H-Bridge

- `ch10_01_motor_forward_stop_reverse.py` · 절 10.6 · 정회전 · 정지 · 역회전
- `ch10_02_motor_pwm_speed.py` · 절 10.7 · PWM 속도 조절
- `ch10_03_motor_switch_ctrl.py` · 절 10.8 · 스위치로 모터 제어

### Chapter 11. I²C · SSD1306 OLED

- `ch11_01_i2c_scan.py` · 절 11.6 · I²C 스캔 · 주소 확인
- `ch11_02_oled_hello.py` · 절 11.7 · OLED Hello 표시
- `ch11_03_oled_shapes.py` · 절 11.8 · OLED 도형 그리기
- `ch11_04_oled_pot_realtime.py` · 절 11.9 · OLED · POT 실시간 표시
- `ch11_05_i2c_multi_devices.py` · 절 11.10 · 여러 I²C 장치 동시 사용

### Chapter 12. Wi-Fi · NTP

- `ch12_01_wifi_network_setup.py` · 절 12.2 · network 라이브러리 준비
- `ch12_02_wifi_connect_wait.py` · 절 12.3 · Wi-Fi 접속 · 대기
- `ch12_03_ntp_settime.py` · 절 12.4 · NTP 로 시간 동기
- `ch12_04_oled_digital_clock.py` · 절 12.5 · OLED 디지털 시계
- `ch12_05_webserver_led_control.py` · 절 12.7 · 웹서버 · LED 제어

### Chapter 13. 외부 확장

- `ch13_01_servo_sg90_angle.py` · 절 13.3 · SG90 서보 각도 제어
- `ch13_02_buzzer_melody.py` · 절 13.4 · 부저 · 학교종 멜로디
- `ch13_03_lm35_temperature.py` · 절 13.5 · LM35 온도 측정

## 사용 방법

1. Thonny 로 `.py` 파일 열기
2. YeonTahn Board 에 Raspberry Pi Pico 2W 를 실장 후 USB 연결
3. 각 파일 상단 주석의 챕터·절을 참고해 강의 자료와 함께 학습

## 라이선스

교육 목적으로 자유롭게 활용하세요. TouchLabs · YeonTahn Board V1