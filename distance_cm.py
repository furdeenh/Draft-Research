from time import sleep
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
GPIO.setup(ENA_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Enable pin, set to HIGH initially (enabled)

# Constants
STEPS_PER_REV = 1600  # Set according to microstepping configuration (e.g., 1600 for 8 microsteps/rev)
LEAD_MM_PER_REV = 5   # Lead of the screw in mm per revolution

# Calculate steps per cm
STEPS_PER_CM = (STEPS_PER_REV / LEAD_MM_PER_REV) * 10

# Function to generate step pulses
def step_motor(direction, steps, step_delay):
    GPIO.output(DIR_PIN, direction)
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        sleep(step_delay)

# Get user input for distance
distance_cm = float(input("Enter the distance to move in cm: "))
steps = int(STEPS_PER_CM * distance_cm)

try:
    while True:
        # Move motor in CW direction for user-specified distance
        print(f'Moving CW for {distance_cm} cm')
        GPIO.output(ENA_PIN, GPIO.LOW)  # Enable the driver
        step_motor(CW, steps, 0.001)  # 1 ms delay
        sleep(1)

        # Move motor in CCW direction for user-specified distance
        print(f'Moving CCW for {distance_cm} cm')
        step_motor(CCW, steps, 0.001)  # 1 ms delay
        GPIO.output(ENA_PIN, GPIO.HIGH)  # Disable the driver
        sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
