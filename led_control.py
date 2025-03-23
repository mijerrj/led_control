from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import RPi.GPIO as GPIO
import threading
import time
import paho.mqtt.client as mqtt

# ======================[ Flask konfiguracija ]======================
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "@bar4kadAbara"
jwt = JWTManager(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per second"])

# ======================[ GPIO konfiguracija ]=======================
LED_PIN = 17
BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
# Gumb je vezan med GPIO in GND, zato uporabljamo pull-up (brez pritiska je HIGH, pritisnjen pa LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ======================[ Globalne spremenljivke ]===================
web_led_state = "off"    # Spletni ukaz ("on" oz. "off")
button_state = "released"  # Fizično stanje gumba ("pressed" oz. "released")
led_is_on = False          # Trenutno stanje LED (True = LED sveti)

# ======================[ MQTT konfiguracija ]=======================
MQTT_BROKER = "localhost"
MQTT_TOPIC = "led_control/button_status"

mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"MQTT error: {e}")

# ======================[ Funkcija za spremljanje gumba in LED ]========
def monitor_button():
    global button_state, web_led_state, led_is_on
    prev_button_state = None

    while True:
        current_gpio = GPIO.input(BUTTON_PIN)
        current_state = "pressed" if current_gpio == GPIO.LOW else "released"

        if current_state != prev_button_state:
            button_state = current_state
            mqtt_client.publish(MQTT_TOPIC, button_state)
            print(f"[BUTTON] {button_state}")
            prev_button_state = current_state

        # LED naj sveti, če je gumb pritisnjen ALI če spletni ukaz je "on"
        led_should_be_on = (button_state == "pressed") or (web_led_state == "on")
        print(f"[DEBUG] web_led_state={web_led_state}, button={button_state}, LED_should_be_on={led_should_be_on}")

        # Ker je LED aktivna na LOW (sveti, ko je GPIO nastavljen na LOW)
        if led_should_be_on != led_is_on:
            if led_should_be_on:
                GPIO.output(LED_PIN, GPIO.LOW)
                print("[LED] Turning ON (GPIO.LOW)")
            else:
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("[LED] Turning OFF (GPIO.HIGH)")
            led_is_on = led_should_be_on

        time.sleep(0.05)

# ======================[ Zazeni spremljanje gumba loceno ]===============
button_thread = threading.Thread(target=monitor_button, daemon=True)
button_thread.start()

# ======================[ JWT AVTENTIKACIJA ]=======================
USERS = {"admin": "password123"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        token = create_access_token(identity=username)
        return jsonify({"access_token": token})
    return jsonify({"msg": "Invalid username or password"}), 401

# ======================[ API poti ]=======================
@app.route('/')
def index():
    # Uporabi predlogo iz /templates/index.html, ki že ima industrijski izgled
    return render_template("index.html", status=("ON" if led_is_on else "OFF"))

@app.route('/led/on', methods=['POST'])
@jwt_required()
def led_on():
    global web_led_state
    web_led_state = "on"
    print("[WEB] LED set to ON, web_led_state now:", web_led_state)
    # Pošlji uporabnika nazaj na glavno stran
    return redirect(url_for("index"))

@app.route('/led/off', methods=['POST'])
@jwt_required()
def led_off():
    global web_led_state
    web_led_state = "off"
    print("[WEB] LED set to OFF, web_led_state now:", web_led_state)
    return redirect(url_for("index"))

@app.route('/led/status', methods=['GET'])
@jwt_required()
def led_status():
    # Ne zahtevamo JWT, da je to javno dostopno
    return jsonify({"status": "on" if led_is_on else "off"})

@app.route('/button/status', methods=['GET'])
#@jwt_required()
def button_status():
    return jsonify({"status": button_state})

# ======================[ Zagon aplikacije ]=======================
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
