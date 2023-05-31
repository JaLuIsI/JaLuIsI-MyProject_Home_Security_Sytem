import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Set GPIO pins for Ultrasonic Sensor
TRIG_PIN = 27
ECHO_PIN = 17

# Set MQTT broker credentials
mqtt_broker = "31bad960136343c4b62e0fbcfd943afd.s2.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_topic = "security_system/distance"

# Set MQTT client credentials
mqtt_username = "hivemq.webclient.1685513799853"
mqtt_password = "sW.w78Cc%@Q01b*BRpjA"

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Create MQTT client
client = mqtt.Client()

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(mqtt_topic)

# Callback function for MQTT message received
def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    print("Received message: " + message)

# Function to measure distance using Ultrasonic Sensor
def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    # Connect MQTT client with credentials
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)

    # Main loop
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")

        # Publish motion detection message if distance is within 10 cm
        if distance < 10:
            motion_message = "Motion detected!"
            client.publish(mqtt_topic, motion_message)

        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
