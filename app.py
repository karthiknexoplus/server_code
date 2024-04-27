from flask import Flask, render_template, request
import json
import qrcode
from io import BytesIO

app = Flask(__name__)

incoming_data = []

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
        incoming_data.append(json.loads(request.form['data']))
    return render_template('index.html', incoming_data=incoming_data)

@app.route('/generate_qr_code', methods=['GET'])
def get_qr_code():
    global incoming_data
    if incoming_data:
        data_to_encode = json.dumps(incoming_data[-1])
        img_io = generate_qr_code(data_to_encode)
        return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    return 'No data to generate QR code.', 400

if __name__ == '__main__':
    app.run(debug=True)
