import time
import RPi.GPIO as GPIO
from stepper_motor_hat import Motor

# Define motor rotation directions
CW = 1          # Clockwise
CCW = 0         # Counterclockwise

# Initialize the motor
motor = Motor(1)  # Motor 1 on the HAT

# Linear actuator specifications
LEAD_SCREW_PITCH = 1.0  # cm per revolution (adjust based on actual specs)
PULSES_PER_REV = 200    # pulses per revolution

# Function to move the motor
def move_motor(direction, steps, step_delay):
    motor.setMicroStep('1/16')  # Set microstepping to 1/16
    motor.setSpeed(5)  # Set speed (adjust as needed)
    motor.setDirection(direction)  # Set direction

    for _ in range(steps):
        motor.oneStep()
        time.sleep(step_delay)

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
        move_motor(direction_flag, steps, step_delay)

        time.sleep(1)  # Pause before next input

except KeyboardInterrupt:
    print("Program interrupted")
finally:
    motor.release()  # Release the motor
    GPIO.cleanup()
    print("GPIO cleaned up")
