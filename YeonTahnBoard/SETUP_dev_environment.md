# 연탄보드(YeonTahn Board V1) 개발환경 안내

네트워크·클라우드·AI 예제(14~)는 **두 가지 개발환경 어디서든** 동일하게 실행됩니다.
코드는 완전히 같고, **보드에 연결하는 방법만** 다릅니다.

> 사용 부품: Raspberry Pi **Pico 2W** + YeonTahn Board V1
> 펌웨어: **MicroPython (Pico 2W 전용 · RP2350 빌드)**
> `network`·`ntptime`·`neopixel`·`urequests` 내장이라 별도 설치 불필요

---

## 방법 A. Thonny (설치형 · PC)

가장 안정적. 초보자 교육에 권장.

1. [thonny.org](https://thonny.org) 에서 설치
2. USB 케이블로 보드 연결 (데이터 지원 케이블)
3. 우측 하단 → **인터프리터: MicroPython (Raspberry Pi Pico)** 선택
4. `.py` 파일 열고 **F5** 실행 / **Ctrl+C** 중지
5. Shell 창에서 `print()` 출력 확인

- **장점**: 오프라인 동작, 파일 관리 쉬움, 에러 메시지 명확
- **주의**: Pico 2W 첫 사용 시 **RP2350용 MicroPython UF2**를 먼저 설치 (RP2040용 아님!)

---

## 방법 B. Viper IDE (웹 · 설치 불필요)

[viper-ide.org](https://viper-ide.org) — 브라우저에서 바로. 크롬/엣지 권장.

1. 크롬/엣지로 **viper-ide.org** 접속
2. 좌측 상단 연결 버튼 → 연결 방식 선택
   - **USB (WebSerial)**: 케이블 연결 → 포트 선택 (Thonny와 동일)
   - **Wi-Fi (WebREPL)**: 보드가 이미 Wi-Fi 접속된 상태에서 무선 연결
   - **Bluetooth (BLE)**: 무선
3. `.py` 파일 업로드 → 실행 버튼 (▶)
4. 하단 Terminal에서 출력 확인

- **장점**: 설치 불필요, 태블릿·크롬북에서도 가능, 무선(WebREPL) 지원
- **주의**:
  - WebSerial은 **크롬/엣지만** 지원 (사파리·파이어폭스 ✕)
  - 한 번에 **한 프로그램만** 보드에 연결 (Thonny와 동시 연결 불가 → 하나는 닫기)

---

## 공통 주의사항

| 항목 | 내용 |
|------|------|
| Wi-Fi 대역 | Pico 2W는 **2.4GHz만** 지원 (5GHz 공유기는 2.4GHz 대역 활성화 필요) |
| 비밀번호 보안 | 코드 상단 `WIFI_SSID/PASS`에 실제 값 입력 → **GitHub 공개 업로드 전 반드시 삭제/치환** |
| 실행 중지 | `Ctrl+C` (무한 루프 예제는 이걸로 종료) |
| 자동 실행 | 전원만 넣어도 돌게 하려면 파일명을 `main.py`로 저장 후 보드에 업로드 |

---

## 네트워크/클라우드/AI 예제 목록

| # | 파일 | 내용 | 상태 |
|---|------|------|------|
| 14 | `14_WiFi_NTP.py` | Wi-Fi 접속 + NTP 현재시각(KST) 받기 | ✅ |
| 15 | `15_Firebase_Upload.py` | 스위치·ADC 값을 Firebase에 업로드 | ✅ |
| 16 | `16_AI_Control.py` | Gemini/Claude API로 보드 정보 전송 → JSON 응답으로 보드 제어 | ✅ |

> ★ **한글 대화형 입력(16번)은 Thonny 에서만** 됩니다. Viper 웹터미널은 한글
> IME 를 조합 과정(로마자+백스페이스)으로 흘려보내 대화형 한글 입력이
> 불가합니다. Viper 에서 쓰려면 `16_AI_Control.py` 의 `USE_COMMAND_LIST = True`
> 로 두어 COMMANDS 리스트를 자동 실행하세요.
