import socket
import network
import utime
from config import SSID, PASSWORD

def connect_wifi():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)
    while not ap.active():
        utime.sleep(0.1)
    print("Access Point aktiv!")
    print("IP:", ap.ifconfig()[0])
    return ap.ifconfig()[0]

def start_server(controller):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(addr)
    except OSError:
        s.close()
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
    s.listen(1)
    s.setblocking(False)
    print("Webserver läuft auf Port 80")
    return s

def handle_request(s, controller):
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()

        if 'GET /request_f2' in request:
            controller.request_f2 = True
            response = 'HTTP/1.0 200 OK\r\n\r\nOK'

        elif 'GET /request_f1' in request:
            controller.request_f1 = True
            response = 'HTTP/1.0 200 OK\r\n\r\nOK'

        elif 'GET /status' in request:
            import ujson
            body = ujson.dumps(controller.get_status())
            response = 'HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n' + body

        else:
            with open('index.html', 'r') as f:
                html = f.read()
            response = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n' + html

        conn.send(response)
        conn.close()

    except OSError:
        pass