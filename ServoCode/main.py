from adafruit_motor import servo
import pwmio
import analogio
import time
import board
import usb_cdc

# Define pins for servos
SERVO_YAW_PIN = board.A0
SERVO_PITCH_PIN = board.A1
SERVO_TRIGGER_PIN = board.GP22
BATTERY_PIN = board.A2

# Define servo objects
servo_yaw = servo.Servo(pwmio.PWMOut(SERVO_YAW_PIN, frequency=300), min_pulse=500, max_pulse=2500, actuation_range=270)
servo_pitch = servo.Servo(pwmio.PWMOut(SERVO_PITCH_PIN, frequency=300), min_pulse=500, max_pulse=2500, actuation_range=270)
servo_trigger = servo.Servo(pwmio.PWMOut(SERVO_TRIGGER_PIN, frequency=300), min_pulse=500, max_pulse=2500, actuation_range=270)

# Define battery voltage object
battery_voltage = analogio.AnalogIn(BATTERY_PIN)
battery_ratio = 3.3 / 65536 * 5.016

time.sleep(0.1)  # Wait for servo to move

# Define servo positions
servo_yaw.angle = 135
servo_pitch.angle = 135
servo_trigger.angle = 135
yaw, pitch, trigger = 135, 135, 135

time.sleep(0.1)  # Wait for servo to move

# Define function for receiving servo positions over serial
# Servo positions are received as a string of the form "yaw,pitch,trigger"
# where yaw, pitch, and trigger are integers between 0 and 180
def read_serial(serial):
    available = serial.in_waiting
    text = ""
    while available:
        raw = serial.read(available)
        text = raw.decode("utf-8")
        available = serial.in_waiting
    return text

def get_servo_positions(input_line):
    positions = input_line.split(",")
    yaw = int(positions[0])
    pitch = int(positions[1])
    trigger = int(positions[2])
    return yaw, pitch, trigger

def update_servo_positions(yaw, pitch, trigger):
    servo_yaw.angle = yaw
    servo_pitch.angle = pitch
    servo_trigger.angle = trigger

# main
buffer = ""
old_buffer = ""
serial = usb_cdc.console
while True:
    old_buffer = buffer
    buffer += read_serial(serial)
    if buffer != old_buffer:
        print(buffer)
    if buffer.endswith("!"):
        # strip line end
        input_line = buffer[:-1]
        # clear buffer
        buffer = ""
        # handle input
        yaw, pitch, trigger = get_servo_positions(input_line)
        voltage = battery_voltage.value * battery_ratio
        print("yaw: {}, pitch: {}, trigger: {}, voltage: {}".format(yaw, pitch, trigger, voltage))

    update_servo_positions(yaw, pitch, trigger)
