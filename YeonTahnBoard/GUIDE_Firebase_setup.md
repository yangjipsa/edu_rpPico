# Firebase Realtime Database 설정 가이드 (연탄보드용)

`15_Firebase_Upload.py` 를 돌리기 전에 Firebase 쪽에서 3가지를 준비합니다.

1. **Realtime Database 만들기**
2. **규칙(Rules) `false` → `true` 로 바꾸기** (테스트용 공개)
3. **코드에 넣을 값 2개 찾기** — ① RTDB 주소(URL), ② DB 비밀키(선택)

> ⚠️ 아래 "규칙 true" 와 "DB 비밀키"는 **테스트/교육용**입니다. 실제 서비스에서는 반드시 보안 규칙을 다시 거세요. (맨 아래 참고)

---

## 0. 사전 준비 — 프로젝트 & DB 생성

1. [console.firebase.google.com](https://console.firebase.google.com) 접속 → 구글 로그인
2. **프로젝트 추가** → 이름 입력 (예: `yeontahn-board`) → 생성
3. 좌측 메뉴 **빌드(Build) → Realtime Database** 클릭
4. **데이터베이스 만들기** 버튼
5. **위치 선택**: `Singapore (asia-southeast1)` 등 (한국에서 가깝게)
6. **보안 규칙 시작 모드**:
   - **"테스트 모드에서 시작"** 선택 ← 제일 간단 (30일간 공개)
   - 또는 "잠금 모드" 선택 후 아래 2번에서 직접 규칙 변경

---

## 1. 규칙(Rules) `false` → `true` 바꾸기

데이터가 안 올라가면 대부분 **규칙이 막혀 있어서**입니다.

1. Realtime Database 화면 상단 탭에서 **규칙(Rules)** 클릭
2. 아래처럼 보이면 **쓰기/읽기가 막힌 상태**:
   ```json
   {
     "rules": {
       ".read": false,
       ".write": false
     }
   }
   ```
3. `false` 를 **`true`** 로 바꿉니다:
   ```json
   {
     "rules": {
       ".read": true,
       ".write": true
     }
   }
   ```
4. 우측 상단 **게시(Publish)** 버튼 클릭 → 적용 완료

> ✅ 이렇게 하면 `DB_SECRET` 을 비워둔 채로 바로 업로드가 됩니다.
> ⚠️ 이 상태는 **누구나 읽고 쓸 수 있음** → 테스트가 끝나면 되돌리세요.

---

## 2. RTDB 주소(URL) 확인하는 법

코드의 `FB_URL` 에 넣을 값입니다.

1. Realtime Database → **데이터(Data)** 탭
2. 데이터 트리 **맨 위에 표시되는 URL** 이 그것입니다. 예:
   ```
   https://yeontahn-board-default-rtdb.firebaseio.com/
   ```
   또는 리전에 따라:
   ```
   https://yeontahn-board-default-rtdb.asia-southeast1.firebasedatabase.app/
   ```
3. 코드에는 **끝의 `/` 를 빼고** 넣습니다:
   ```python
   FB_URL = "https://yeontahn-board-default-rtdb.firebaseio.com"
   ```

> 💡 리전형 주소(`...firebasedatabase.app`)인데 `firebaseio.com` 으로 잘못 넣으면 업로드가 실패합니다. **콘솔에 뜬 주소를 그대로** 쓰세요.

---

## 3. DB 비밀키(비밀번호) 찾는 법  ※ 선택 (규칙을 true로 했으면 불필요)

규칙을 잠근 채 쓰려면 `DB_SECRET` 에 넣을 값이 필요합니다. (레거시 방식이지만 MCU에서 가장 간단)

1. 콘솔 좌측 상단 **⚙ (톱니바퀴) → 프로젝트 설정(Project settings)**
2. **서비스 계정(Service accounts)** 탭
3. 왼쪽 목록에서 **데이터베이스 비밀번호(Database secrets)** 클릭
   - 안 보이면: 페이지 하단 "레거시 사용 설정" 또는 "Show" 링크를 눌러 표시
4. 표시된 긴 문자열이 **DB 비밀키**입니다. **Show(표시)** 눌러 복사
5. 코드에 붙여넣기:
   ```python
   DB_SECRET = "여기에_복사한_비밀키"
   ```

> ⚠️ **DB 비밀키는 비밀번호와 같습니다.** GitHub 공개 업로드 전 반드시 지우세요.
> 💡 Google이 권장하는 최신 방식은 **서비스 계정 토큰(OAuth)** 이지만, 교육/테스트에는 위 레거시 비밀키가 훨씬 단순합니다.

---

## 4. 코드에 넣기 (요약)

`15_Firebase_Upload.py` 상단:

```python
FB_URL    = "https://프로젝트ID-default-rtdb.firebaseio.com"  # 2번에서 확인
FB_PATH   = "yeontahn"          # 원하는 이름 (자동 생성됨)
DB_SECRET = ""                  # 규칙을 true로 했으면 빈칸 그대로
```

실행 후 콘솔 **데이터(Data)** 탭을 새로고침하면 이렇게 쌓입니다:

```
yeontahn/
 └─ latest/
     ├─ time        : "2026-09-03 14:00:00"
     ├─ key1        : 1
     ├─ key2        : 0
     ├─ adc_raw     : 32000
     ├─ adc_volt    : 1.61
     └─ temp_c      : 26.4
```

---

## 5. 안 될 때 체크리스트

| 증상 | 원인 / 해결 |
|------|-------------|
| `업로드 실패` 반복 | 규칙이 아직 `false` → 1번대로 `true` 로 변경·게시 |
| 401 / Permission denied | `DB_SECRET` 필요하거나 값이 틀림 (3번) |
| 주소 관련 에러 | `FB_URL` 이 콘솔 주소와 불일치 (2번, 리전 확인) |
| Wi-Fi부터 실패 | 2.4GHz 인지, SSID/비밀번호 확인 |
| `urequests` import 에러 | Thonny → 도구 → 패키지 관리 → `urequests` 설치 |

---

## 6. 테스트 끝나면 — 보안 규칙 되돌리기 (중요)

공개(`true`) 상태로 방치하면 누구나 데이터를 지울 수 있습니다. 테스트 후:

```json
{
  "rules": {
    ".read": false,
    ".write": false
  }
}
```
→ 게시(Publish). 이후에는 `DB_SECRET`(3번) 또는 정식 인증 토큰을 사용해 접근하세요.
