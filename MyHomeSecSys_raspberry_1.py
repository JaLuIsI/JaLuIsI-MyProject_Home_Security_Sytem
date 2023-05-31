import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Set GPIO pins for LED and Buzzer
LED_PIN = 22
BUZZER_PIN = 18

# Set MQTT broker credentials
mqtt_broker = "31bad960136343c4b62e0fbcfd943afd.s2.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_topic = "security_system/distance"

# Set MQTT client credentials
mqtt_username = "hivemq.webclient.1685513799853"
mqtt_password = "sW.w78Cc%@Q01b*BRpjA"

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Create MQTT client
client = mqtt.Client()

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(mqtt_topic)

# Callback function for MQTT message received
def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    print("Received message: " + message)  # Print the received message

    # Turn on LED and Buzzer
    GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    # Connect MQTT client with credentials
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)

    # Main loop
    client.loop_forever()

except KeyboardInterrupt:
    print("Program stopped by user")
    GPIO.cleanup()
