from controller import TrafficController
from webserver import connect_wifi, start_server, handle_request
import utime

# WLAN starten
connect_wifi()

# Ampelsteuerung
controller = TrafficController()

# Webserver starten
server = start_server(controller)

print("System gestartet")

while True:
    handle_request(server, controller)
    controller.tick()
    utime.sleep_ms(100)