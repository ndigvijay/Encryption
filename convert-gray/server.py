from flask import Flask, request, send_file
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure a file is present in the request
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Read the file as a PIL Image
    image = Image.open(file)
    # Convert PIL Image to OpenCV format
    image = np.array(image)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image back to PIL format
    gray_image_pil = Image.fromarray(gray_image)
    
    # Save the grayscale image to a BytesIO object
    img_io = BytesIO()
    gray_image_pil.save(img_io, format='PNG')
    img_io.seek(0)

    # Send the processed image back to the client
    # return send_file(img_io, mimetype='image/png', as_attachment=True, attachment_filename='grayscale.png')
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='grayscale.png')


if __name__ == '__main__':
    app.run(debug=True)
