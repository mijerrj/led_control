from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import RPi.GPIO as GPIO

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per second"])

# GPIO konfiguracija
LED_PIN = 17
BUTTON_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up upor

# Status LED
led_status = {"state": "off"}

@app.route('/')
@limiter.limit("5 per second")  # Omeji zahtev na 5/s za to pot
def index():
    return render_template('index.html', led_status=led_status["state"])

@app.route('/led/on', methods=['POST'])
@limiter.limit("3 per second")  # Omeji zahtev na 3/s za LED
def led_on():
    global led_status
    GPIO.output(LED_PIN, GPIO.HIGH)
    led_status["state"] = "on"
    return jsonify({"status": "LED prižgana"})

@app.route('/led/off', methods=['POST'])
@limiter.limit("3 per second")
def led_off():
    global led_status
    GPIO.output(LED_PIN, GPIO.LOW)
    led_status["state"] = "off"
    return jsonify({"status": "LED ugasnjena"})

@app.route('/button/status', methods=['GET'])
def button_status():
    # Preveri stanje stikala
    button_state = GPIO.input(BUTTON_PIN)
    return jsonify({"status": "pressed" if button_state == GPIO.LOW else "released"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()

