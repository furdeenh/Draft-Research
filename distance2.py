from time import sleep
import time
import RPi.GPIO as GPIO

# Define GPIO pins
DIR_PIN = 20    # Direction pin
PUL_PIN = 21    # Pulse pin
ENA_PIN = 18    # Enable pin (optional)

# Define motor rotation directions
CW = 0          # Clockwise
CCW = 1         # Counterclockwise

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Enable pin, set to HIGH initially (disabled)

# Linear actuator specifications
LEAD_SCREW_PITCH = 1.0  # cm per revolution (adjust based on actual specs)
PULSES_PER_REV = 25000  # pulses per revolution (adjust based on actual specs)

# Function to generate step pulses
def step_motor(direction, steps, step_delay):
    GPIO.output(DIR_PIN, direction)
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        sleep(step_delay)

def calculate_steps(distance_cm):
    revolutions = distance_cm / LEAD_SCREW_PITCH
    steps = int(revolutions * PULSES_PER_REV)
    return steps

try:
    while True:
        # Get user input for distance and direction
        distance_cm = float(input("Enter distance in cm: "))
        direction = input("Enter direction (CW/CCW): ").strip().upper()

        if direction not in ['CW', 'CCW']:
            print("Invalid direction. Please enter 'CW' or 'CCW'.")
            continue

        direction_flag = CW if direction == 'CW' else CCW

        steps = calculate_steps(distance_cm)
        step_delay = 0.001  # 1 ms delay

        # Move motor
        GPIO.output(ENA_PIN, GPIO.LOW)  # Enable the driver
        step_motor(direction_flag, steps, step_delay)
        GPIO.output(ENA_PIN, GPIO.HIGH)  # Disable the driver

        sleep(1)  # Pause before next input

except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
