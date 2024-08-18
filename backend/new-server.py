from flask import Flask, request, send_file, render_template, jsonify
from functions import encrypt_and_embed_file, extract_and_decrypt_file
from io import BytesIO
import base64

app = Flask(__name__)


@app.route('/')
def encode_html():
    return render_template('encode.html')


@app.route('/decode')
def decode_html():
    return render_template('decode.html')


@app.route('/encodefile', methods=['POST'])
def encode():
        
    try :

        password = request.form['password']
        # file_name = request.form['file-name']

        img_file = request.files['img_file']
        zip_file = request.files['zip_file']
        file_name = zip_file.filename
        
        img_data = img_file.read()
        file_data = zip_file.read()
        
        new_image_data = encrypt_and_embed_file(img_data, file_name, file_data, password)
        
        new_image_io = BytesIO(new_image_data)
        new_image_io.seek(0)

        return send_file(new_image_io, mimetype='application/octet-stream', as_attachment=True, download_name='new-image.png')
        # return send_file(new_image_data, mimetype='application/octet-stream', as_attachment=True, download_name='new-image')

    except Exception as e:

        return jsonify({'error': str(e)}), 400


@app.route('/decodefile', methods=['POST'])
def decode_file():

    try :

        password = request.form['password']
        img_file = request.files['img_file']
        img_data = img_file.read()
        
        file_name, file_data = extract_and_decrypt_file(img_data, password)

        # file_io = BytesIO(file_data)
        # file_io.seek(0)

        encoded_file_data = base64.b64encode(file_data).decode('utf-8')

        return jsonify({'file_name': file_name, 'file_data': encoded_file_data})
        # return send_file(file_io, as_attachment=True, download_name=file_name, mimetype='application/octet-stream')
        # return send_file(file_data, as_attachment=True, download_name=file_name, mimetype='application/octet-stream')
        
    except Exception as e:

        return jsonify({'error': str(e)}), 400


app.run(debug=True)