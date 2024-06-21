import time
import RPi.GPIO as GPIO
from smbus import SMBus

# Define I2C address of the Stepper Motor HAT
I2C_ADDRESS = 0x60

# Define GPIO pins for motor control
DIR_PIN = 20
STEP_PIN = 21
ENA_PIN = 18

# Motor rotation directions
CW = 0
CCW = 1

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT, initial=GPIO.HIGH)

# Function to calculate steps
def calculate_steps(distance_cm, lead_screw_pitch=1.0, pulses_per_rev=200):
    revolutions = distance_cm / lead_screw_pitch
    steps = int(revolutions * pulses_per_rev)
    return steps

# Function to control motor steps
def step_motor(direction, steps, delay):
    GPIO.output(DIR_PIN, direction)
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

try:
    while True:
        # Get user input for distance and direction
        distance = float(input("Enter distance in cm: "))
        direction_input = input("Enter direction (CW/CCW): ").strip().upper()

        if direction_input not in ['CW', 'CCW']:
            print("Invalid direction. Please enter 'CW' or 'CCW'.")
            continue

        direction = CW if direction_input == 'CW' else CCW
        steps = calculate_steps(distance)
        step_delay = 0.001  # 1 ms delay

        # Enable the motor
        GPIO.output(ENA_PIN, GPIO.LOW)
        step_motor(direction, steps, step_delay)
        GPIO.output(ENA_PIN, GPIO.HIGH)

        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
