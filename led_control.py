from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import RPi.GPIO as GPIO
import threading
import time
import paho.mqtt.client as mqtt

app = Flask(__name__)

#JWT
app.config["JWT_SECRET_KEY"] = "@bar4kadAbara"
jwt = JWTManager(app)

#Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per second"])

# GPIO konfiguracija
LED_PIN = 17
BUTTON_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up upor

#MQTT
MQTT_BROKER = "localhost"  # Spremeni, če uporabljaš zunanji MQTT strežnik
MQTT_TOPIC = "led_control/button_status"

# Ustvari MQTT odjemalca
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()  # MQTT v  loopu
except Exception as e:
    print(f"Napaka pri povezavi na MQTT strežnik: {e}")

# Status LED in gumb
led_status = {"state": "off"}
button_state = "released"

# Funkcija za spremljanje pritiska gumba in pošiljanje MQTT sporočil
def monitor_button():
    global button_state
    while True:
        current_state = GPIO.input(BUTTON_PIN)
        new_state = "pressed" if current_state == GPIO.LOW else "released"

        if new_state != button_state:
            button_state = new_state
            mqtt_client.publish(MQTT_TOPIC, button_state)
            print(f"Objavljeno MQTT: {MQTT_TOPIC} -> {button_state}")

        time.sleep(0.1)  # sparaj CPU

# Zaženi spremljanje gumba ločeno
button_thread = threading.Thread(target=monitor_button, daemon=True)
button_thread.start()

# ============================[ JWT AVTENTIKACIJA ]============================ #

# Testni uporabnik (v resničnem sistemu bi se preverjalo iz baze)
USERS = {
    "admin": "password123"
}

@app.route("/login", methods=["POST"])
def login():
    """Ustvari JWT žeton za overjene uporabnike."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token})

    return jsonify({"msg": "Neveljavno uporabniško ime ali geslo"}), 401

# API-ji

@app.route('/')
@limiter.limit("5 per second")  # Omeji zahtev na 5/s za to pot
def index():
    return render_template('index.html', led_status=led_status["state"])

@app.route('/led/on', methods=['POST'])
@jwt_required() #zahteva za JWT avtentikacijo
@limiter.limit("3 per second")  # Omeji zahtev na 3/s za LED
def led_on():
    global led_status
    GPIO.output(LED_PIN, GPIO.HIGH)
    led_status["state"] = "on"
    mqtt_client.publish("led_control/status", "on")
    return jsonify({"status": "LED prižgana"})

@app.route('/led/off', methods=['POST'])
@jwt_required()
@limiter.limit("3 per second")
def led_off():
    global led_status
    GPIO.output(LED_PIN, GPIO.LOW)
    led_status["state"] = "off"
    mqtt_client.publish("led_control/status", "off")
    return jsonify({"status": "LED ugasnjena"})

@app.route('/button/status', methods=['GET'])
@jwt_required()
def button_status():
    # Preveri stanje stikala
    button_state = GPIO.input(BUTTON_PIN)
    return jsonify({"status": "pressed" if button_state == GPIO.LOW else "released"})

# Zagon aplikacije 

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()

