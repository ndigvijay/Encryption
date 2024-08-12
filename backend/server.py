from flask import Flask, request, jsonify
import gridfs
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

# import os

app = Flask(__name__)

CORS(app)  #  Adjust the origin as needed

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

client = MongoClient("mongodb://localhost:27017/")
db = client.mydatabase
fs = gridfs.GridFS(db)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_ZIP_EXTENSIONS = {'zip'}


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/encode", methods=['POST'])
# @cross_origin()
def encode():
    zip_file = request.files.get('zip_file')
    image_file = request.files.get('image_file')

    if 'zip_file' not in request.files or 'image_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    if not allowed_file(zip_file.filename, ALLOWED_ZIP_EXTENSIONS):
        return jsonify({'error': 'Invalid ZIP file type'}), 400
    if not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': 'Invalid image file type'}), 400

    # Read the file content and store it in MongoDB using GridFS
    zip_id = fs.put(zip_file.read(), filename=zip_file.filename, content_type=zip_file.content_type)
    image_id = fs.put(image_file.read(), filename=image_file.filename, content_type=image_file.content_type)

    db.file_metadata.insert_one({
        'zip_file_id': zip_id,
        'image_file_id': image_id,
        'zip_filename': zip_file,
        'image_filename': image_file
    })

    return jsonify({'zip_id': str(zip_id), 'image_id': str(image_id)}), 200


@app.route("/decode")
def decode():
    return jsonify({"message": "this is decode page"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
