from flask import Flask, request, send_file, render_template, jsonify
from io import BytesIO
import os
from functions import *

app = Flask(__name__)

TEMP_FILE_PATH = 'temp-file.png'



@app.route('/encode', methods=['POST'])
def encode():
        
    try :

        img_file = request.files['img_file']
        emb_file = request.files['emb_file']
        img_data = img_file.read()
        file_data = emb_file.read()
        embedded_image_data, encryption_key = encrypt_and_embed_file(img_data, file_data)
        with open(TEMP_FILE_PATH, 'wb') as f:
            f.write(embedded_image_data)
            return jsonify({'download_link': '/download_image', 'encryption_key': encryption_key.decode()}), 200

    except:

        # return jsonify({'error': 'this error'}), 409

        if not img_file or not emb_file:
            return jsonify({'error': 'No file part'}), 401
        else:
            return jsonify({'error': 'some random error'}), 402



@app.route('/download_image')
def download_image():

    try:

        return send_file(TEMP_FILE_PATH, as_attachment=True, download_name=TEMP_FILE_PATH, mimetype='image/png')

    except:

        return jsonify({'error': 'File not found'}), 406



@app.route('/decode', methods=['POST'])
def decode_file():

    if 'img_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    img_file = request.files['img_file']
    encryption_key = request.form.get('encryption_key')
    
    if not img_file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    if not encryption_key:
        return jsonify({'error': 'No encryption key provided'}), 400

    try:
        img_data = img_file.read()
        file_name, file_data = extract_and_decrypt_file_from_image(img_data, encryption_key.encode())
        return send_file(BytesIO(file_data), as_attachment=True, download_name=file_name, mimetype='application/octet-stream')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


app.run(debug=True)