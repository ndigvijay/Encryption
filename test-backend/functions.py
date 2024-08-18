from cryptography.fernet import Fernet


def embed_file(image_data, file_data):
    delimiter1 = b'END_OF_IMAGE_DATA'
    delimiter2 = b'END_OF_FILE_PATH'
    file_path_bytes = b'embedded_file' + b'\0'
    output_data = image_data + delimiter1 + file_path_bytes + delimiter2 + file_data
    return output_data

def encrypt_data(data, encryption_key):
    fernet = Fernet(encryption_key)
    return fernet.encrypt(data)

def generate_key():
    return Fernet.generate_key()

def encrypt_and_embed_file(img_data, file_data):
    encryption_key = generate_key()
    encrypted_file_data = encrypt_data(file_data, encryption_key)
    embedded_image_data = embed_file(img_data, encrypted_file_data)
    return embedded_image_data, encryption_key


def decrypt_file(file_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(file_data)
    return decrypted_data

def extract_file(image_data):
    delimiter1 = b'END_OF_IMAGE_DATA'
    delimiter2 = b'END_OF_FILE_PATH'
    pos1 = image_data.find(delimiter1)
    if pos1 == -1:
        raise ValueError("Delimiter 1 not found in image data")
    pos2 = image_data.find(delimiter2, pos1 + len(delimiter1))
    if pos2 == -1:
        raise ValueError("Delimiter 2 not found in image data")
    file_path_bytes = image_data[pos1 + len(delimiter1):pos2]
    file_path = file_path_bytes.decode('utf-8').rstrip('\0')
    file_data = image_data[pos2 + len(delimiter2):]
    return file_path, file_data

def extract_and_decrypt_file_from_image(image_data, encryption_key):
    file_name, encrypted_file_data = extract_file(image_data)
    file_data = decrypt_file(encrypted_file_data, encryption_key)
    return file_name, file_data