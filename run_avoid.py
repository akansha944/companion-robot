# run_avoid.py
from machine import Pin, PWM
import time
from hcsr04 import HCSR04          # <-- NOTE: your file is "hcr04.py"; class is HCSR04
from L298N_motor import L298N

# ---------------- Pin setup ----------------
# L298N (one motor, Channel A)
ENA = PWM(Pin(0))                 # ENA (remove the ENA jumper on the L298N if you want PWM speed control)
IN1 = Pin(1, Pin.OUT)             # IN1
IN2 = Pin(2, Pin.OUT)             # IN2

motor = L298N(ENA, IN1, IN2)
motor.setSpeed(30000)             # 0..65535 (your driver sets 15kHz PWM internally)

# HC-SR04
# Make sure wiring matches these pins! (Trigger -> GP28, Echo -> GP27)
sensor = HCSR04(trigger_pin=28, echo_pin=27, echo_timeout_us=30000)

# --------------- Behavior tuning ---------------
STOP_MM   = 150   # stop if object is nearer than this (e.g., 15 cm)
START_MM = 180   # only resume when distance grows beyond this (e.g., 20 cm)
MIN_STOP_MS = 500 # minimum stop time to avoid rapid start/stop

last_stop = 0
moving = False

def read_mm():
    try:
        return sensor.distance_mm()
    except OSError:
        # treat timeout as "very far"
        return 5000

while True:
    d = read_mm()
    action = None

    if d < STOP_MM:
        if moving:
            motor.stop()
            moving = False
            action = "STOP"
    elif d >= START_MM:
        if not moving:
            motor.forward()
           # time.sleep(4)
            moving = True
            action = "FORWARD"

    print("d={} mm | moving={} {}".format(d, moving, f"-> {action}" if action else ""))
    time.sleep(1)