from gpiozero import MCP3008, PWMOutputDevice
from time import sleep

# Potentiometer connected to channel 0 of MCP3008
pot = MCP3008(channel=0)

# MOSFET Gate connected to GPIO18 (must support PWM!)
mosfet = PWMOutputDevice(18)

while True:
    speed = pot.value  # Value between 0.0 and 1.0
    mosfet.value = speed  # Set PWM to that value
    print(f"Motor Speed: {speed:.2f}")
    sleep(0.8)
