"""
Chapter 12. Wi-Fi · NTP
절 12.4 · NTP 로 시간 동기

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
import ntptime, time

ntptime.host = "pool.ntp.org"    # 전세계 공용 서버
ntptime.settime()                 # RTC 에 시각 설정

# 현재 UTC 시각
now = time.localtime(time.time())
print(f"UTC: {now[0]}-{now[1]:02d}-{now[2]:02d} "
      f"{now[3]:02d}:{now[4]:02d}:{now[5]:02d}")

# 한국은 UTC+9
kst = time.localtime(time.time() + 9 * 3600)
print(f"KST: {kst[0]}-{kst[1]:02d}-{kst[2]:02d} "
      f"{kst[3]:02d}:{kst[4]:02d}:{kst[5]:02d}")
