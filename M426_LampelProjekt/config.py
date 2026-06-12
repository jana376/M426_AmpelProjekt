# Ampel 1 (A1)
A1_R = 6    # GPIO 6  – Rot
A1_Y = 7    # GPIO 7  – Orange
A1_G = 8    # GPIO 8  – Grün

# Ampel 2 (A2)
A2_R = 18   # GPIO 18 – Rot
A2_Y = 19   # GPIO 19 – Orange
A2_G = 20   # GPIO 20 – Grün

# Fussgänger F1 und F2 – eigene Pins definieren
F1_R = 2
F1_G = 3

F2_R = 4
F2_G = 5

# Zeiten in Sekunden
T_ROT_ORANGE = 1    # rot + orange Phase
T_GRUEN      = 5    # grün Phase
T_ORANGE     = 2    # orange Phase
T_MIN_GRUEN  = 3    # Mindestgrünzeit (Fussgänger-Priorität begrenzen)

SSID     = "Ampel-Pico"   # Name deines Pico-Netzwerks
PASSWORD = "12345678"     # Mindestens 8 Zeichen!