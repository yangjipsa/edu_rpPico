"""
Chapter 12. Wi-Fi · NTP
절 12.7 · 웹서버 · LED 제어

YeonTahn Board V1 · TouchLabs
출처 · YeonTahn_Board_설명자료.md
"""
import socket

s = socket.socket()
s.bind(('', 80))
s.listen(1)

while True:
    conn, addr = s.accept()
    req = conn.recv(1024).decode()
    print("요청:", req.split()[1] if req else "-")
    
    html = """
    <html><body>
    <h1>Pico 2W 웹서버</h1>
    <p><a href="/on">LED ON</a></p>
    <p><a href="/off">LED OFF</a></p>
    </body></html>
    """
    conn.send("HTTP/1.1 200 OK\r\n\r\n" + html)
    conn.close()
