# YeonTahn Board V1 · 예제 코드 가이드

**TouchLabs** 가 만든 라즈베리 파이 Pico 2W 기반 교육 보드 · **YeonTahn Board V1** 의 온보드 부품을 활용한 파이썬 예제 모음입니다.

> 홈페이지 · <https://touchlabs.kr>

---

## 준비물

| 항목 | 설명 |
|---|---|
| **YeonTahn Board V1** | 이 보드 · TouchLabs 제작 |
| **Raspberry Pi Pico 2W** | 보드에 실장 · MicroPython 펌웨어가 올라간 상태 |
| **USB 케이블** | Pico ↔ PC 연결 (데이터 통신 가능한 것) |
| **Thonny IDE** | <https://thonny.org> · 무료 · MicroPython 코드 편집·실행 |

이후 안내는 Thonny 로 Pico 에 접속되어 있는 상태라고 가정합니다.

---

## 이 예제들이 활용하는 온보드 부품

이 폴더의 예제는 **모두 온보드 부품만** 사용합니다 · 외부 부품·배선 없이 바로 실습 가능합니다.

| 블록 | 부품 | 사용 GPIO |
|---|---|---|
| LED | LED2 (AH) · LED3 (AH) · LED4 (AL) | GP0 · GP1 · GP2 |
| 스위치 | KEY1 (풀업) · KEY2 (풀다운) | GP3 · GP4 |
| 네오픽셀 | SK6812 RGBW × 4 (U4~U7) | GP5 |
| 모터 드라이버 | L9110 (모터 1) | GP17 (IA) · GP16 (IB) |
| ADC | 가변저항 R7 (5kΩ · Alps RK09K) · CDS (LDR) | GP26 (JP1 로 선택) |
| 내장 온도센서 | Pico 내부 다이오드 | ADC 채널 4 |

> **JP1 점퍼 위치** · A-Center = LDR · B-Center = POT

---

## 예제 목록

파일명은 `NN_카테고리_주제.py` 규칙 · 파일명 정렬 = 학습 순서.

### 디지털 출력 · LED (`01 ~ 03`)

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 01 | `01_LED_AH.py` | Active High LED · `value(1)` = 켜짐 |
| 02 | `02_LED_AL.py` | Active Low LED · `value(0)` = 켜짐 |
| 03 | `03_LED_AH_AL.py` | 두 극성 LED 동시 제어 · 신호값과 실제 상태의 대응 관찰 |

### 디지털 입력 · 스위치 (`04 ~ 06`)

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 04 | `04_SW_PU.py` | 풀업 스위치 상태 읽기 · 평소 `1` · 누르면 `0` |
| 05 | `05_SW_PD.py` | 풀다운 스위치 상태 읽기 · 평소 `0` · 누르면 `1` |
| 06 | `06_SW_PU_LED_AL.py` | 풀업 스위치로 AL LED 제어 · `LED.value(SW.value())` 한 줄 |

### PWM (`07 ~ 08`)

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 07 | `07_PWM_LED.py` | GP0 LED 항상 켜서 비교군 · GP1 LED 는 페이드 인/아웃 |
| 08 | `08_PWM_Motor.py` | L9110 · IA·IB PWM 으로 방향·속도 제어 · 3단 속도 시퀀스 |

### 네오픽셀 · SK6812 RGBW (`09 ~ 10`)

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 09 | `09_NeoPixel_Rainbow.py` | HSV 색공간 순환 · 4개 픽셀이 시차를 두고 무지개 흐름 |
| 10 | `10_NeoPixel_ColorInput.py` | Shell 에서 `R,G,B` 또는 `R,G,B,W` 입력 · 현재색→목표색 페이드 |

### ADC · 아날로그 입력 (`11 ~ 13`)

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 11 | `11_ADC_TempSensor.py` | Pico 내장 온도센서 · 외부 부품 없이 실습 |
| 12 | `12_ADC_POT.py` | 가변저항 · raw · 전압 · 실제 저항값(R_bot·R_top) 계산 |
| 13 | `13_ADC_CDS.py` | 조도센서 raw 값 관찰 · 빛의 밝기에 따라 어떻게 변하는지 |

---

## 실행 방법

1. Thonny 를 실행하고 Pico 에 접속 (하단 인터프리터에 "MicroPython (Raspberry Pi Pico)" 표시 확인)
2. 이 폴더에서 원하는 `.py` 파일 열기
3. `F5` 또는 실행 버튼으로 실행
4. 종료는 `Ctrl+C` · 모든 예제가 `try/finally` 로 종료 시 LED·모터를 완전히 끕니다

**JP1 관련 예제** · 12·13 은 실행 전에 JP1 점퍼 위치를 확인하세요.

- `12_ADC_POT.py` · JP1 = **B - Center**
- `13_ADC_CDS.py` · JP1 = **A - Center**

---

## 공통 코드 규칙

이 폴더의 모든 예제는 아래 규칙을 지킵니다.

1. **상단 헤더 주석** · 파일명 · 설명 · 대상 부품 · 회사 · 작성자 · 작성일
2. **시작 상태** · 모든 LED / 모터 꺼짐부터 출발
3. **종료 상태** · `try/except KeyboardInterrupt/finally` 로 Ctrl+C 시에도 무조건 꺼짐
4. **하드웨어 자원 반납** · PWM 사용 예제는 `deinit()` 호출

---

## 알아두면 좋은 것

### 네오픽셀은 RGBW 4채널

이 보드의 네오픽셀은 **SK6812 계열 RGBW** 입니다 · 일반 WS2812B (RGB 3채널) 로 다루면 데이터가 밀려 색·개수가 어긋납니다.

```python
np = neopixel.NeoPixel(Pin(5), 4, bpp=4)   # bpp=4 필수
np[0] = (255, 0, 0, 0)                      # (R, G, B, W) 4-튜플
```

W (백색) 채널을 활용하면 RGB 로만 만드는 것보다 훨씬 순수한 흰색과 파스텔 톤을 표현할 수 있습니다.

### L9110 모터 · IA/IB 조합

| IA | IB | 동작 |
|---|---|---|
| PWM | 0 | 정회전 (duty 로 속도) |
| 0 | PWM | 역회전 (duty 로 속도) |
| 0 | 0 | 정지 (브레이크) |
| 1 | 1 | 사용 금지 |

방향 전환 전에는 짧게 정지 (100ms 이상) 시키는 것이 모터·드라이버에 안전합니다.

### 가변저항 계산 공식

분압 회로에서 · POT 총 저항 R_TOTAL 이 wiper 위치에 따라 위·아래로 나뉩니다.

```
R_bot = R_TOTAL × (raw / 65535)
R_top = R_TOTAL - R_bot
```

이 보드의 R7 은 **5kΩ** 입니다.

---

## 라이선스

교육 목적으로 자유롭게 활용하세요.

**TouchLabs** · <https://touchlabs.kr> · YeonTahn Board V1
