# ================================================================
#  파일명    : 16_AI_Control.py
#  설명      : 자연어(한국어) 명령을 AI(Gemini 또는 Claude)에게 보내고,
#             AI 가 돌려준 JSON 을 그대로 보드 동작으로 실행한다.
#             "빨간색으로 켜줘", "천천히 앞으로 1초", "지금 몇 도야?" 처럼
#             말하면 LED · 네오픽셀 · 모터가 반응한다.
#
#             핵심 아이디어 3가지
#              1) 센서 주입 : 매 요청에 현재 온도/ADC/스위치 상태를 함께
#                 보내 "지금 몇 도야?" 를 한 번의 호출로 답한다.
#              2) 값 클램핑 : AI 가 보낸 숫자도 보드에서 다시 제한한다.
#                 원격 모델을 하드웨어의 마지막 안전장치로 두지 않는다.
#              3) 로컬 비상정지 : '정지'/'멈춰' 는 AI 를 거치지 않고
#                 즉시 전부 끈다. (AI 가 '꺼줘'를 오해할 수 있으므로)
#  참고      : Gemini/Claude 선택은 yeontahn_secrets.py 의 AI_PROVIDER.
#             MicroPython 은 공식 SDK 가 없어 REST(urequests) 로 호출.
#             LED 극성 : LED2(GP0)=AH, LED4(GP2)=AL, LED3(GP1)=AH 가정.
#  대상 부품 : LED2/3/4(GP0/1/2) · 네오픽셀×4(GP5) · 모터1(IA:GP17,IB:GP16)
#             KEY1(GP3) · KEY2(GP4) · ADC(GP26) · 내장온도(ADC4)
#  보드      : YeonTahn Board V1 (Raspberry Pi Pico 2W)
#  회사      : TouchLabs (https://touchlabs.kr)
#  작성자    : yangjipsa
#  작성일    : 2026-09-03
# ================================================================

from machine import Pin, PWM, ADC
from neopixel import NeoPixel
import network
import ntptime
import json
import time
import sys
import gc

try:
    import urequests as requests
except ImportError:
    import requests

# ---------- 설정 불러오기 (yeontahn_secrets.py) ----------
try:
    from yeontahn_secrets import (WIFI_SSID, WIFI_PASSWORD, AI_PROVIDER,
                                  GEMINI_API_KEY, GEMINI_MODEL,
                                  CLAUDE_API_KEY, CLAUDE_MODEL)
except ImportError:
    print("yeontahn_secrets.py 가 없습니다. 템플릿을 복사해 채우세요.")
    WIFI_SSID = "YOUR_WIFI";  WIFI_PASSWORD = "YOUR_PW"
    AI_PROVIDER = "gemini"
    GEMINI_API_KEY = "YOUR_GEMINI_KEY";  GEMINI_MODEL = "gemini-2.5-flash"
    CLAUDE_API_KEY = "YOUR_CLAUDE_KEY";  CLAUDE_MODEL = "claude-opus-5"

# ---------- 보드의 안전 한계 (모델 값보다 항상 우선) ----------
MAX_SPEED   = 80          # 모터 속도 상한(%)
MAX_RUN_MS  = 3000        # 모터 1회 최대 구동 시간(ms)
MAX_ACTIONS = 8           # 응답 1개당 실행할 최대 동작 수
PWM_FREQ    = 1000

KST_OFFSET  = 9 * 3600
NTP_HOST    = "kr.pool.ntp.org"

# ★ 대화형 한글 입력은 Thonny 에서만 안정적입니다.
#   Viper 웹터미널은 한글 IME 를 조합 과정(로마자+백스페이스)으로 흘려보내
#   대화형 한글 입력이 불가합니다. Viper 에서 쓰려면 아래 COMMANDS 를 켜세요.
USE_COMMAND_LIST = False   # True = 리스트 자동실행(Viper용), False = 직접 입력(Thonny)
COMMANDS = [
    "빨간색으로 켜줘",
    "지금 몇 도야?",
    "LED2 켜줘",
    "천천히 앞으로 1초",
    "다 꺼줘",
]
COMMAND_GAP_S = 2         # (리스트 모드) 명령 사이 대기(초)

# ==========================================================
#  주변장치를 TLS 호출보다 먼저 할당한다.
#  mbedtls(TLS)는 16KB 연속 메모리가 필요하다. 네오픽셀/PWM 을
#  첫 HTTPS 요청 뒤에 만들면 힙이 조각나 MemoryError 가 난다.
#  한 번만, 맨 위에서 만들어 재사용한다.
# ==========================================================
IA = PWM(Pin(17)); IB = PWM(Pin(16))          # 모터1 (L9110)
IA.freq(PWM_FREQ); IB.freq(PWM_FREQ)

NUM = 4
rgbw = NeoPixel(Pin(5), NUM, bpp=4)
cur_rgbw = [0, 0, 0, 0]

# LED 극성: True = Active Low(0이 켜짐)
led_pins   = {2: Pin(0, Pin.OUT), 3: Pin(1, Pin.OUT), 4: Pin(2, Pin.OUT)}
led_low    = {2: False, 3: False, 4: True}     # LED4=GP2 는 Active Low
led_state  = {2: False, 3: False, 4: False}

sw1 = Pin(3, Pin.IN)          # KEY1 · 풀업  : 0 = 눌림
sw2 = Pin(4, Pin.IN)          # KEY2 · 풀다운: 1 = 눌림
adc_ext  = ADC(Pin(26))       # 가변저항/CDS (JP1)
adc_temp = ADC(4)             # 내장 온도센서

wlan = network.WLAN(network.STA_IF)

gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())


# ---------- 한글 입력 (Thonny 전용) ----------
#  내장 input() 은 이 펌웨어에서 한글(0x80↑)을 버린다. 그래서 stdin 을
#  바이트로 직접 읽어 UTF-8 로 조립한다. Thonny 는 깨끗한 UTF-8 을 보내
#  정상 동작한다. (Viper 웹터미널은 IME 조합을 흘려 이 방식이 안 통함)
_pending_lf = False


def read_line(prompt=""):
    global _pending_lf
    sys.stdout.write(prompt)
    chars = []          # 확정된 문자들
    pend = b""          # 아직 완성 안 된 멀티바이트 조각
    while True:
        c = sys.stdin.buffer.read(1)
        if not c:
            time.sleep_ms(5)
            continue
        if c == b"\n" and _pending_lf and not chars and not pend:
            _pending_lf = False           # \r 뒤따라온 \n 삼키기
            continue
        _pending_lf = False
        if c == b"\r":
            _pending_lf = True
            sys.stdout.write("\n")        # 줄바꿈 에코
            break
        if c == b"\n":
            sys.stdout.write("\n")
            break
        b = c[0]
        if b == 3:                        # Ctrl+C
            raise KeyboardInterrupt
        if b in (8, 127):                 # 백스페이스/DEL
            if chars:
                chars.pop()
                sys.stdout.write("\x08 \x08")   # 화면에서 한 칸 지우기
            pend = b""
            continue
        pend += c
        try:
            ch = pend.decode("utf-8")
            chars.append(ch)
            sys.stdout.write(ch)          # 입력 글자 화면에 에코
            pend = b""
        except UnicodeError:
            if len(pend) >= 4:            # 4바이트 넘게 안 맞으면 버림
                pend = b""
    return "".join(chars).strip()


def run_commands():
    """리스트 자동실행 모드 (Viper 등 한글 입력 불가 환경용)."""
    for user_text in COMMANDS:
        print("나 >", user_text)
        handle(user_text)
        time.sleep(COMMAND_GAP_S)
    print("모든 명령 실행 완료.")


def run_interactive():
    """직접 입력 모드 (Thonny). 빈 줄 Enter 로 종료."""
    while True:
        user_text = read_line("나 > ")
        if not user_text:
            break
        handle(user_text)


# ---------- 주변장치 헬퍼 ----------
def _duty(percent):
    return int(65535 * min(100, abs(percent)) / 100)


def motor(cmd, percent):
    # 08_PWM_Motor 규칙: 정회전=IA duty, 역회전=IB duty.
    if cmd == "forward":
        IB.duty_u16(0); IA.duty_u16(_duty(percent))
    elif cmd == "backward":
        IA.duty_u16(0); IB.duty_u16(_duty(percent))
    else:                                 # stop
        IA.duty_u16(0); IB.duty_u16(0)


def stop_motor():
    IA.duty_u16(0); IB.duty_u16(0)


def set_rgbw(r, g, b, w):
    global cur_rgbw
    for j in range(NUM):
        rgbw[j] = (r, g, b, w)
    rgbw.write()
    cur_rgbw = [r, g, b, w]


def set_led(idx, on):
    if idx not in led_pins:
        return
    led_state[idx] = on
    if led_low[idx]:                      # Active Low : 0=켜짐
        led_pins[idx].value(0 if on else 1)
    else:                                 # Active High: 1=켜짐
        led_pins[idx].value(1 if on else 0)


def read_temp():
    volt = adc_temp.read_u16() / 65535 * 3.3
    return 27 - (volt - 0.706) / 0.001721


def sw1_pressed():
    return sw1.value() == 0               # 풀업: LOW=눌림


def sw2_pressed():
    return sw2.value() == 1               # 풀다운: HIGH=눌림


def all_off():
    # 로컬 비상정지 — API 안 거치고 즉시. 가장 중요한 안전장치.
    stop_motor()
    set_rgbw(0, 0, 0, 0)
    for i in (2, 3, 4):
        set_led(i, False)


def print_status():
    raw = adc_ext.read_u16()
    print("  온도    : {:.1f} C".format(read_temp()))
    print("  ADC GP26: {} ({:.0f}%)".format(raw, raw / 65535 * 100))
    print("  KEY1/2  : {} / {}".format(
        "눌림" if sw1_pressed() else "떼짐",
        "눌림" if sw2_pressed() else "떼짐"))
    print("  LED     : {}".format(
        " ".join("L{}={}".format(i, "on" if led_state[i] else "off")
                 for i in (2, 3, 4))))
    print("  RGBW    : {}".format(tuple(cur_rgbw)))


def sensor_summary():
    # 매 프롬프트에 넣는 한 줄. 센서 질문을 한 번의 호출로 답하게 한다.
    raw = adc_ext.read_u16()
    return ("temp={:.1f}C, adc_gp26={} ({:.0f}%), "
            "key1={}, key2={}, leds={}, rgbw={}").format(
        read_temp(), raw, raw / 65535 * 100,
        "pressed" if sw1_pressed() else "released",
        "pressed" if sw2_pressed() else "released",
        "".join("1" if led_state[i] else "0" for i in (2, 3, 4)),
        tuple(cur_rgbw))


# ==========================================================
#  Wi-Fi
# ==========================================================
def connect_wifi(timeout=20):
    wlan.active(True)
    if wlan.isconnected():
        return wlan.ifconfig()[0]
    print("Wi-Fi 접속 중 :", WIFI_SSID)
    if WIFI_PASSWORD:
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    else:
        wlan.connect(WIFI_SSID)
    start = time.time()
    step = 0
    while not wlan.isconnected():
        if time.time() - start > timeout:
            set_rgbw(40, 0, 0)            # 빨강 = 실패
            raise OSError("Wi-Fi 접속 실패 · SSID/비밀번호/2.4GHz 확인")
        for j in range(NUM):              # 청록 스윕 = 접속 중
            rgbw[j] = (0, 30, 40, 0) if j == step % NUM else (0, 0, 0, 0)
        rgbw.write()
        step += 1
        time.sleep(0.25)
    set_rgbw(0, 0, 0, 0)
    print("접속 완료! IP :", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]


def sync_ntp(retry=3):
    ntptime.host = NTP_HOST
    for _ in range(retry):
        try:
            ntptime.settime()
            return True
        except Exception:
            time.sleep(1)
    return False


def now_kst_text():
    tm = time.localtime(time.time() + KST_OFFSET)
    return "{}년 {}월 {}일 {:02d}:{:02d}".format(tm[0], tm[1], tm[2], tm[3], tm[4])


# ==========================================================
#  보드 설명서 + JSON 규약 (프롬프트로 매번 전달)
#  모델은 이 보드를 모른다. 학습 대신 사실을 프롬프트에 넣어준다.
# ==========================================================
BOARD_MANUAL = (
    "[연탄보드 V1 · Raspberry Pi Pico 2W]\n"
    "제어 가능한 것:\n"
    "- led  : index 2/3/4, cmd=on/off/toggle\n"
    "- rgbw : 네오픽셀 4개, cmd=set, r/g/b/w 각 0-255 (컬러는 r,g,b 로; 흰색만 w)\n"
    "- motor: 모터 1개, cmd=forward/backward/stop, speed 0-100, ms 0-3000\n"
    "색 이름→값 예: 빨강(255,0,0) 초록(0,255,0) 파랑(0,0,255) "
    "노랑(255,255,0) 보라(160,0,255) 하양 w=255 끄기(0,0,0,0)\n"
)

SYSTEM_PROMPT = (
    BOARD_MANUAL +
    "너는 위 보드를 조종하는 컨트롤러다. 사용자 말을 보드 명령으로 바꿔라.\n"
    "반드시 아래 형식의 JSON '하나만' 출력한다. 설명·코드블록·군말 금지.\n"
    '{"say":"한국어 한 문장","actions":[{"device":"led|rgbw|motor|none",'
    '"cmd":"on|off|toggle|set|forward|backward|stop",'
    '"index":2,"speed":50,"ms":1000,"r":0,"g":0,"b":0,"w":0}]}\n'
    "- 켜기=on, 끄기=off 를 정확히 골라라. '꺼줘/끄기'는 반드시 off.\n"
    "- 동작이 필요 없고 대답만 하면 actions=[] 로 둬라.\n"
    "- 센서 값을 물으면 함께 주는 SENSORS 데이터를 근거로 say 에 답해라.\n"
)


# ---------- 응답에서 JSON 뽑아내기 ----------
def parse_json(text):
    if not text:
        raise ValueError("빈 응답")
    try:
        return json.loads(text)
    except Exception:
        pass
    # 모델이 앞뒤에 군말을 붙였을 때: 첫 { ~ 마지막 } 만 잘라 재시도
    s = text.find("{")
    e = text.rfind("}")
    if s != -1 and e != -1 and e > s:
        return json.loads(text[s:e + 1])
    raise ValueError("JSON 을 찾지 못함: " + text[:120])


def _user_block(user_text):
    return "지금 시각: {}\nSENSORS: {}\n사용자: {}".format(
        now_kst_text(), sensor_summary(), user_text)


# ---------- Gemini (REST) ----------
GEMINI_URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
              "{}:generateContent")


def ask_gemini(user_text):
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": _user_block(user_text)}]}],
        "generationConfig": {"response_mime_type": "application/json",
                             "temperature": 0.2},
    }
    body = json.dumps(payload).encode("utf-8")     # 한글 Content-Length 문제 회피
    gc.collect()
    resp = None
    try:
        resp = requests.post(
            GEMINI_URL.format(GEMINI_MODEL),
            headers={"Content-Type": "application/json",
                     "x-goog-api-key": GEMINI_API_KEY},
            data=body)
        if resp.status_code != 200:
            raise OSError("HTTP {} - {}".format(resp.status_code, resp.text[:200]))
        data = resp.json()
    finally:
        if resp:
            resp.close()
        gc.collect()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return parse_json(text)


# ---------- Claude (REST · Anthropic Messages API) ----------
CLAUDE_URL = "https://api.anthropic.com/v1/messages"


def ask_claude(user_text):
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": _user_block(user_text)}],
    }
    body = json.dumps(payload).encode("utf-8")
    gc.collect()
    resp = None
    try:
        resp = requests.post(
            CLAUDE_URL,
            headers={"content-type": "application/json",
                     "x-api-key": CLAUDE_API_KEY,
                     "anthropic-version": "2023-06-01"},
            data=body)
        if resp.status_code != 200:
            raise OSError("HTTP {} - {}".format(resp.status_code, resp.text[:200]))
        data = resp.json()
    finally:
        if resp:
            resp.close()
        gc.collect()
    # content 는 블록 리스트. type=="text" 인 블록만 모은다(생각 블록 무시).
    parts = [b.get("text", "") for b in data.get("content", [])
             if b.get("type") == "text"]
    return parse_json("".join(parts))


def ask_ai(user_text, retry=2):
    # 첫 HTTPS 요청은 TLS 핸드셰이크 워밍업 때문에 가끔 실패한다
    # (MBEDTLS_ERR_SSL_CONN_EOF 등). 몇 번 재시도하면 복구된다.
    last = None
    for i in range(retry + 1):
        try:
            if AI_PROVIDER == "claude":
                return ask_claude(user_text)
            return ask_gemini(user_text)
        except Exception as e:
            last = e
            print("  재시도 {}/{} · {}".format(i + 1, retry, e))
            gc.collect()
            time.sleep(1)
    raise last


# ==========================================================
#  동작 실행 — 모델의 숫자를 믿지 않고 다시 제한한다
# ==========================================================
def _int(a, key, default=0):
    try:
        return int(a.get(key, default))
    except (TypeError, ValueError):
        return default


def _clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)


def run_action(a):
    if not isinstance(a, dict):
        return "건너뜀(형식 오류)"
    device = a.get("device")
    cmd = a.get("cmd")

    if device == "motor":
        speed = _clamp(_int(a, "speed", 50), 0, MAX_SPEED)
        ms = _clamp(_int(a, "ms", 1000), 0, MAX_RUN_MS)
        if cmd in ("forward", "backward"):
            motor(cmd, speed)
            time.sleep_ms(ms)
            stop_motor()
            return "모터 {} 속도={} {}ms".format(cmd, speed, ms)
        stop_motor()
        return "모터 정지"

    if device == "rgbw":
        if cmd == "off":
            set_rgbw(0, 0, 0, 0)
            return "RGBW 끔"
        r = _clamp(_int(a, "r"), 0, 255)
        g = _clamp(_int(a, "g"), 0, 255)
        b = _clamp(_int(a, "b"), 0, 255)
        w = _clamp(_int(a, "w"), 0, 255)
        set_rgbw(r, g, b, w)
        return "RGBW ({},{},{},{})".format(r, g, b, w)

    if device == "led":
        idx = _int(a, "index", 2)
        if idx not in led_pins:
            return "LED 번호 오류: {}".format(idx)
        on = (not led_state[idx]) if cmd == "toggle" else (cmd == "on")
        set_led(idx, on)
        return "LED{} {}".format(idx, "on" if led_state[idx] else "off")

    return "동작 없음"


def run_actions(actions):
    if not isinstance(actions, list):
        return
    for a in actions[:MAX_ACTIONS]:
        try:
            print("   ", run_action(a))
        except Exception as e:
            print("    실행 오류:", e)


def handle(user_text):
    """명령 하나 처리: 로컬 명령이면 즉시, 아니면 AI 로."""
    if user_text in ("정지", "멈춰", "다 꺼줘", "stop", "STOP"):
        all_off()
        print("  ★ 전부 정지했습니다.\n")
        return
    if user_text in ("상태", "status"):
        print_status()
        print()
        return
    try:
        print("  생각 중 ...")
        result = ask_ai(user_text)
        print("AI >", result.get("say", ""))
        run_actions(result.get("actions", []))
    except Exception as e:
        stop_motor()                      # 오류 시 모터는 절대 안 남긴다
        print("오류:", e)
    print()


# ==========================================================
#  실행
# ==========================================================
def banner(ip):
    line = "=" * 44
    prov = "Claude ({})".format(CLAUDE_MODEL) if AI_PROVIDER == "claude" \
        else "Gemini ({})".format(GEMINI_MODEL)
    print("\n" + line)
    print("  연탄보드 V1 · AI 제어 (STEP 16)")
    print(line)
    print("  AI       : {}".format(prov))
    print("  Wi-Fi    : {}  IP {}".format(WIFI_SSID, ip))
    print("  시각     : {}".format(now_kst_text() if TIME_OK else "동기화 실패"))
    print("  안전한계 : 속도 {}%, 최대 {}ms".format(MAX_SPEED, MAX_RUN_MS))
    print("  입력방식 : {}".format(
        "리스트 자동실행" if USE_COMMAND_LIST else "직접 입력(Thonny)"))
    print(line)
    print("  · '정지'/'멈춰'/'다 꺼줘' = 즉시 전부 끔 (AI 안 거침)")
    print("  · '상태' = 센서값 표시")
    if not USE_COMMAND_LIST:
        print("  · 끝내려면 빈 줄에서 Enter")
        print("  ★ 한글 입력은 Thonny 에서. Viper 는 USE_COMMAND_LIST=True 로.")
    print(line)
    print("예: 빨간색으로 켜줘 / 천천히 앞으로 1초 / LED2 켜줘 / 지금 몇 도야?\n")


TIME_OK = False

try:
    if "YOUR_" in WIFI_SSID:
        raise ValueError("yeontahn_secrets.py 를 먼저 채우세요")
    key = CLAUDE_API_KEY if AI_PROVIDER == "claude" else GEMINI_API_KEY
    if "YOUR_" in key:
        raise ValueError("API 키를 먼저 채우세요 (AI_PROVIDER={})".format(AI_PROVIDER))

    all_off()
    ip = connect_wifi()
    TIME_OK = sync_ntp()
    banner(ip)

    if USE_COMMAND_LIST:
        run_commands()            # Viper 등: 리스트 자동실행
    else:
        run_interactive()         # Thonny: 직접 한글 입력

except KeyboardInterrupt:
    pass

finally:
    # ---------- 종료 상태 · 모든 동작 없음 ----------
    all_off()
    IA.deinit(); IB.deinit()
    print("종료: 모터 정지, LED/네오픽셀 OFF")
