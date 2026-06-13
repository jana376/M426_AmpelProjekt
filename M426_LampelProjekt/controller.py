import utime
from config import *
from traffic_light import TrafficLight

# Zustände der State Machine
STATE_A1_GREEN  = "A1_GREEN"
STATE_A2_GREEN  = "A2_GREEN"
STATE_F1_GREEN  = "F1_GREEN"
STATE_F2_GREEN  = "F2_GREEN"
STATE_ALL_RED   = "ALL_RED"

class TrafficController:

    def __init__(self):
        # Ampeln initialisieren
        self.a1 = TrafficLight(A1_R, A1_G, A1_Y)
        self.a2 = TrafficLight(A2_R, A2_G, A2_Y)
        self.f1 = TrafficLight(F1_R, F1_G)
        self.f2 = TrafficLight(F2_R, F2_G)

        self.state            = STATE_A1_GREEN
        self.state_start      = utime.time()

        # Anforderungen (gesetzt durch Webserver)
        self.request_f1 = False
        self.request_f2 = False
        self.request_a2 = False


    def _transition_to_green(self, light):
        """rot → rot+orange → grün"""
        light.set_red_yellow()
        utime.sleep(T_ROT_ORANGE)
        light.set_green()

    def _transition_to_red(self, light):
        """grün → orange → rot"""
        light.set_yellow()
        utime.sleep(T_ORANGE)
        light.set_red()

    # ── Zustandswechsel ─────────────────────────────────────────────

    def _set_state(self, new_state):
        """Wechselt den Zustand und setzt alle Ampeln korrekt."""

        # Schritt 1: aktuelle Grünampel auf rot schalten
        if self.state == STATE_A1_GREEN:
            self._transition_to_red(self.a1)
        elif self.state == STATE_A2_GREEN:
            self._transition_to_red(self.a2)
        elif self.state == STATE_F1_GREEN:
            self._transition_to_red(self.f1)
        elif self.state == STATE_F2_GREEN:
            self._transition_to_red(self.f2)

        # Kurze Allrot-Phase zur Sicherheit
        utime.sleep(1)

        # Schritt 2: neuen Zustand aktivieren
        self.state = new_state
        self.state_start = utime.time()

        if new_state == STATE_A1_GREEN:
            # A1 grün → A2, F1, F2 rot
            self._transition_to_green(self.a1)
            self.a2.set_red()
            self.f1.set_red()
            self.f2.set_red()

        elif new_state == STATE_A2_GREEN:
            # A2 grün → A1, F1, F2 rot
            self._transition_to_green(self.a2)
            self.a1.set_red()
            self.f1.set_red()
            self.f2.set_red()

        elif new_state == STATE_F1_GREEN:
            # F1 grün → A1 rot, A2 darf orange, F2 rot
            self.a1.set_red()
            self.a2.set_yellow()  # A2 darf orange sein
            self.f2.set_red()
            self._transition_to_green(self.f1)

        elif new_state == STATE_F2_GREEN:
            # F2 grün → A1, A2 rot
            self._transition_to_green(self.f2)
            self.a1.set_red()
            self.a2.set_red()
            self.f1.set_red()

    # ── Hauptloop ───────────────────────────────────────────────────

    def tick(self):
        """Wird regelmässig aufgerufen – entscheidet über Zustandswechsel."""
        elapsed = utime.time() - self.state_start

        # Fussgänger haben Priorität, aber nicht dauerhaft
        if elapsed >= T_GRUEN:
            if self.request_f2:
                self.request_f2 = False
                self._set_state(STATE_F2_GREEN)
            elif self.request_f1:
                self.request_f1 = False
                self._set_state(STATE_F1_GREEN)
            elif self.request_a2:
                self.request_a2 = False
                self._set_state(STATE_A2_GREEN)
            else:
                # Standardzyklus: abwechselnd A1 / A2
                if self.state == STATE_A1_GREEN:
                    self._set_state(STATE_A2_GREEN)
                else:
                    self._set_state(STATE_A1_GREEN)

    def get_status(self):
        """Für die Webseite: aktueller Zustand aller Ampeln."""
        return {
            "state": self.state,
            "a1": self.a1.get_state(),
            "a2": self.a2.get_state(),
            "f1": self.f1.get_state(),
            "f2": self.f2.get_state(),
        }