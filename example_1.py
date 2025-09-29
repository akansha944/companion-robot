"""This micropython program makes the motor1 
move in forward and backward directions."""

from machine import Pin, PWM
from L298N_motor import L298N
import time

ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)

motor1 = L298N(ENA, IN1, IN2)     #create a motor1 object
motor1.setSpeed(25000)            #set the speed of motor1. Speed value varies from 25000 to 65534

while True:
    motor1.forward()      #run motor1 forward
    time.sleep(2)         #wait for 5 seconds
    motor1.backward()     #run motor1 backward
    time.sleep(2)         #run motor2 backward
    motor1.stop()