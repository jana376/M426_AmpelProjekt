from machine import Pin

class TrafficLight:
    """Repräsentiert eine einzelne Ampel (Auto oder Fussgänger)."""

    def __init__(self, red_pin, green_pin, yellow_pin=None):
        self.red    = Pin(red_pin,   Pin.OUT)
        self.green  = Pin(green_pin, Pin.OUT)
        self.yellow = Pin(yellow_pin, Pin.OUT) if yellow_pin else None
        self.set_red()  # Startzustand: rot

    def set_red(self):
        self.red.on()
        self.green.off()
        if self.yellow:
            self.yellow.off()

    def set_red_yellow(self):
        """rot + orange (Übergang zu grün)"""
        if self.yellow:
            self.red.on()
            self.yellow.on()
            self.green.off()

    def set_green(self):
        self.red.off()
        self.green.on()
        if self.yellow:
            self.yellow.off()

    def set_yellow(self):
        """nur orange (Übergang zu rot)"""
        if self.yellow:
            self.red.off()
            self.yellow.on()
            self.green.off()

    def get_state(self):
        """Gibt den aktuellen Zustand als String zurück (für Webseite)."""
        if self.green.value():
            return "green"
        if self.yellow and self.yellow.value() and self.red.value():
            return "red_yellow"
        if self.yellow and self.yellow.value():
            return "yellow"
        return "red"