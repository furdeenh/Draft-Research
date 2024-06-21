from gpiozero import LED
from time import sleep

# Define GPIO pins for motor control
DIR_PIN = 20
STEP_PIN = 21
ENA_PIN = 18

# Initialize pins
dir_pin = LED(DIR_PIN)
step_pin = LED(STEP_PIN)
ena_pin = LED(ENA_PIN)

# Motor rotation directions
CW = 0
CCW = 1

# Enable the motor initially
ena_pin.off()

# Function to calculate steps
def calculate_steps(distance_cm, lead_screw_pitch=1.0, pulses_per_rev=200):
    revolutions = distance_cm / lead_screw_pitch
    steps = int(revolutions * pulses_per_rev)
    return steps

# Function to control motor steps
def step_motor(direction, steps, delay):
    dir_pin.value = direction
    for _ in range(steps):
        step_pin.on()
        sleep(delay)
        step_pin.off()
        sleep(delay)

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
        ena_pin.off()
        step_motor(direction, steps, step_delay)
        ena_pin.on()

        sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    print("GPIO cleaned up")
