# AI API 발급 · 비용 · 사용법 가이드 (16_AI_Control.py)

자연어로 연탄보드를 제어하는 `16_AI_Control.py` 를 쓰려면 **Gemini 또는 Claude**
API 키가 필요합니다. 둘 중 하나만 있어도 됩니다.

| | Google Gemini | Anthropic Claude |
|---|---|---|
| 무료 등급 | ✅ 있음 (교실 실습에 충분) | ❌ 없음 (충전식 유료) |
| 키 발급 | Google 계정만 있으면 즉시 | 결제수단 등록 필요 |
| 교육 추천 | ⭐ 입문·수업용 | 응답 품질이 필요할 때 |

> 💡 **처음이라면 Gemini 로 시작**하세요. 무료 등급으로 바로 실습할 수 있습니다.

---

## 1. Gemini API 키 발급 (무료)

1. [aistudio.google.com/apikey](https://aistudio.google.com/apikey) 접속 → Google 로그인
2. **Create API key(API 키 만들기)** 클릭
3. 프로젝트 선택(없으면 자동 생성) → 키 생성
4. `AIza...` 로 시작하는 키를 **복사**
5. `yeontahn_secrets.py` 에 붙여넣기:
   ```python
   AI_PROVIDER    = "gemini"
   GEMINI_API_KEY = "AIza........................"
   GEMINI_MODEL   = "gemini-2.5-flash"   # 무료 등급에서 잘 되는 flash 계열
   ```

> 모델 이름이 404 나면 다른 flash 계열(예: `gemini-2.5-flash`, `gemini-flash-latest`)로
> 바꿔보세요. 사용 가능한 모델은 aistudio 문서에서 확인할 수 있습니다.

---

## 2. Claude API 키 발급 (유료)

1. [console.anthropic.com](https://console.anthropic.com) 접속 → 가입/로그인
2. **Billing(결제)** 메뉴에서 결제수단 등록 + 크레딧 충전 (최소 $5 정도)
3. **API Keys** 메뉴 → **Create Key** → 키 생성
4. `sk-ant-...` 로 시작하는 키를 **복사** (이때 한 번만 보이니 잘 저장)
5. `yeontahn_secrets.py` 에 붙여넣기:
   ```python
   AI_PROVIDER    = "claude"
   CLAUDE_API_KEY = "sk-ant-........................"
   CLAUDE_MODEL   = "claude-haiku-4-5"   # 교실용 저렴·빠름 (아래 비용 참고)
   ```

---

## 3. 비용

### Gemini
- **무료 등급**이 있습니다. 분당/일일 요청 수 제한이 있으나 **교실 실습에는 충분**합니다.
- 유료로 올려도 flash 계열은 매우 저렴합니다.
- 정확한 현재 단가·한도: [ai.google.dev/pricing](https://ai.google.dev/pricing)

### Claude (1M 토큰당, 입력/출력)
| 모델 | 입력 | 출력 | 용도 |
|------|------|------|------|
| `claude-haiku-4-5` | $1 | $5 | ⭐ 교실·대량 (빠르고 저렴) |
| `claude-sonnet-5` | $2 | $10 | 중간 |
| `claude-opus-5` | $5 | $25 | 최고 품질 |

*(표는 참고용 캐시값 — 최신 단가는 [console.anthropic.com](https://console.anthropic.com) 확인)*

### 이 보드 기준 대략 비용 (요청 1회 ≈ 입력 1,000 + 출력 150 토큰)
| | 요청 1회 | 요청 1,000회 |
|---|---|---|
| Gemini flash (무료 등급 내) | **0원** | **0원** |
| Claude Haiku 4.5 | 약 $0.0018 (≈2.4원) | 약 $1.8 |
| Claude Opus 5 | 약 $0.0088 (≈12원) | 약 $8.8 |

> 💡 **비용 절약 팁**
> - 교실에선 **Gemini 무료** 또는 **Claude Haiku** 사용
> - 설명서(프롬프트)가 매 요청 전송되므로, 너무 길게 만들지 않기
> - 필요 없을 때 프로그램 종료(빈 줄 Enter) → 불필요한 요청 방지

---

## 4. 코드 사용법 (16_AI_Control.py)

### ① 준비물
- 연탄보드 V1 + Raspberry Pi Pico 2W (MicroPython 설치)
- Wi-Fi (2.4GHz) · AI API 키 (위 1 또는 2)

### ② 설정 파일 만들기
1. `yeontahn_secrets_template.py` 를 열어 내 값으로 채우기
2. **이름을 `yeontahn_secrets.py` 로 바꿔** 보드에 저장
   (Thonny: File → Save as → Raspberry Pi Pico → 파일명 `yeontahn_secrets.py`)
3. `16_AI_Control.py` 도 보드에 저장

### ③ 입력 방식 선택 (파일 상단)
```python
USE_COMMAND_LIST = False   # False = 직접 한글 입력(Thonny 권장)
                           # True  = COMMANDS 리스트 자동 실행(Viper 등)
```

| 환경 | 설정 | 사용법 |
|------|------|--------|
| **Thonny** | `False` | `나 >` 에 한글 직접 타이핑 |
| **Viper IDE** | `True` | `COMMANDS` 리스트에 한글 명령 적어두고 자동 실행 |

> ⚠️ Viper 웹터미널은 한글 IME 를 조합 과정으로 흘려보내 **대화형 한글 입력이
> 안 됩니다.** Viper 에서는 반드시 `USE_COMMAND_LIST = True` 로 두세요.

### ④ 실행
- Thonny 에서 `16_AI_Control.py` 열고 **F5**
- `나 >` 프롬프트에 명령 입력 (또는 리스트 자동 실행)

### ⑤ 명령 예시
```
나 > 빨간색으로 켜줘          → 네오픽셀 빨강
나 > 초록색으로 LED 켜줘       → 네오픽셀 초록
나 > LED2 켜줘                → LED2 점등
나 > 천천히 앞으로 1초         → 모터 정회전 (바퀴 띄우고!)
나 > 지금 몇 도야?            → 현재 온도 답변
나 > 상태                    → 센서값 표시 (AI 안 거침)
나 > 정지  /  멈춰  /  다 꺼줘  → 즉시 전부 끔 (AI 안 거침)
(빈 줄에서 Enter → 종료)
```

### ⑥ 안전장치
- AI 가 보낸 숫자도 보드에서 다시 제한(속도 ≤80%, 구동 ≤3000ms)
- `정지/멈춰/다 꺼줘` 는 AI 를 거치지 않는 **로컬 비상정지**
- 종료·오류 시 모터 정지 + LED/네오픽셀 OFF

---

## 5. 문제 해결

| 증상 | 원인 / 해결 |
|------|-------------|
| `MBEDTLS_ERR_SSL_CONN_EOF` (첫 요청) | 첫 TLS 연결 워밍업. **자동 재시도로 복구**되니 정상 |
| `HTTP 401 / 403` | API 키 오류 → 키 재확인 (Gemini `AIza...`, Claude `sk-ant-...`) |
| `HTTP 404` (Gemini) | 모델 이름 문제 → `GEMINI_MODEL` 을 다른 flash 계열로 |
| `HTTP 429` | 무료 등급 요청 한도 초과 → 잠시 후 재시도 |
| 한글 입력이 화면에 안 보임/깨짐 | Viper 사용 중 → `USE_COMMAND_LIST=True` 또는 Thonny 사용 |
| Wi-Fi 실패 | 2.4GHz 인지, SSID/비밀번호 확인 |
| `urequests` import 에러 | Thonny → 도구 → 패키지 관리 → `urequests` 설치 |

---

## 6. 보안 (중요)

- **실제 키가 담긴 `yeontahn_secrets.py` 는 GitHub 에 올리지 마세요.**
  (`.gitignore` 에 이미 제외되어 있습니다. 저장소엔 `*_template.py` 만 올라감)
- 키가 노출되면(스크린샷·저장소 등) **즉시 폐기하고 재발급**하세요.
  - Gemini: aistudio.google.com/apikey 에서 삭제
  - Claude: console.anthropic.com → API Keys 에서 삭제
