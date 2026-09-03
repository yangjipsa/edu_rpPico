# ================================================================
#  파일명    : yeontahn_secrets_template.py
#  설명      : Wi-Fi · AI API 키를 한 곳에 모아두는 설정 파일.
#             ★ 사용법: 이 파일을 보드에 올릴 때 이름을
#                'yeontahn_secrets.py' 로 바꿔 저장하세요.
#                (Thonny: File → Save as → Raspberry Pi Pico,
#                 파일명 yeontahn_secrets.py)
#             16_AI_Control.py 가 이 파일에서 값을 불러옵니다.
#  참고      : ★★ 실제 키를 채운 yeontahn_secrets.py 는 절대 GitHub에
#             올리지 마세요. (.gitignore 에 이미 제외돼 있습니다)
#             노출된 키는 즉시 폐기하고 재발급해야 합니다.
#  보드      : YeonTahn Board V1 (Raspberry Pi Pico 2W)
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-09-03
# ================================================================

# ---------- Wi-Fi (2.4GHz 만) ----------
WIFI_SSID     = "여기에_와이파이_이름"
WIFI_PASSWORD = "여기에_비밀번호"        # 개방망이면 "" 로 두기

# ---------- 어떤 AI 를 쓸지 : "gemini" 또는 "claude" ----------
AI_PROVIDER   = "gemini"

# ---------- Google Gemini ----------
#  키 발급: https://aistudio.google.com/apikey  (무료 등급 있음)
GEMINI_API_KEY = "여기에_GEMINI_API_KEY"
GEMINI_MODEL   = "gemini-2.5-flash"       # 404 나면 다른 flash 계열로 교체

# ---------- Anthropic Claude ----------
#  키 발급: https://console.anthropic.com/  (유료)
CLAUDE_API_KEY = "여기에_CLAUDE_API_KEY"
#  기본은 가장 똑똑한 'claude-opus-5'.
#  ★ 교실/대량 사용은 훨씬 저렴하고 빠른 'claude-haiku-4-5' 로 바꾸세요.
CLAUDE_MODEL   = "claude-opus-5"
