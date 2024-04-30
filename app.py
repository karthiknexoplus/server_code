from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
incoming_data = []

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.output(24, GPIO.LOW)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

@app.route('/', methods=['GET', 'POST'])
def index():
    global incoming_data
    if request.method == 'POST':
        incoming_data.append(request.json.get('data'))
        print("Incoming data:", incoming_data[-1])  # Print incoming data in terminal
        return jsonify({'message': 'Data received successfully'}), 200
    return render_template('index.html', incoming_data=incoming_data)

@app.route('/generate_qr_code', methods=['GET'])
def get_qr_code():
    global incoming_data
    if incoming_data:
        data = "upi://pay?pa=karthik.devarajiit-2@oksbi@pn=Karthik%20Devaraj&aid=uGICAgMDc1s6pGw"
        data_to_encode = data
        img_io = generate_qr_code(data_to_encode)
        # Turn on GPIO 18 for 5 seconds
        GPIO.output(18, GPIO.HIGH)
        print("GPIO 18 is ON")  # Print message in terminal
        time.sleep(5)
        GPIO.output(18, GPIO.LOW)
        print("GPIO 18 is OFF")  # Print message in terminal
        # Wait for 5 seconds before turning on servo
        time.sleep(5)
        # Turn on GPIO 24 for 5 seconds (servo motor)
        GPIO.output(24, GPIO.HIGH)
        print("GPIO 24 is ON")  # Print message in terminal
        time.sleep(5)
        GPIO.output(24, GPIO.LOW)
        print("GPIO 24 is OFF")  # Print message in terminal
        return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    return 'No data to generate QR code.', 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)  # Bind to all network interfaces
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
