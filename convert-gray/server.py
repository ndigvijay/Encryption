from flask import Flask, request, send_file, render_template, jsonify
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    
    try :

        file = request.files['file']

        file_data = file.read()
        in_memory_file = np.frombuffer(file_data, np.uint8)
        image = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, img_encoded = cv2.imencode('.png', gray_image)
        img_io = BytesIO(img_encoded.tobytes())
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='grayscale.png')
    
    except :

        if 'file' not in request.files:
            return jsonify({'error':'No file part'}), 400
        
        if file.filename == '':
            return jsonify({'error':'No selected file'}), 400
        
        if image is None:
            return jsonify({'error':'Invalid image'}), 400


app.run(debug=True)
