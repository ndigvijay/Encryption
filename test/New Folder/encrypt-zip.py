from cryptography.fernet import Fernet
import os

# def encrypt_file(input_file_path, encryption_key):
#     fernet = Fernet(encryption_key)
#     with open(input_file_path, 'rb') as file:
#         file_data = file.read()
#     encrypted_data = fernet.encrypt(file_data)
#     with open(input_file_path, 'wb') as file:
#         file.write(encrypted_data)

# def embed_file(image_path, file_path):
#     delimiter = b'END_OF_IMAGE_DATA'
#     with open(image_path, 'rb') as image_file:
#         image_data = image_file.read()
#     with open(file_path, 'rb') as file:
#         file_data = file.read()
#     output_data = image_data + delimiter + file_data
#     with open(image_path, 'wb') as output_file:
#         output_file.write(output_data)

def delete_file(file_path):
    os.remove(file_path)

def embed_file(image_path, file_path):
    delimiter1 = b'END_OF_IMAGE_DATA'
    delimiter2 = b'END_OF_FILE_PATH'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    with open(file_path, 'rb') as file:
        file_data = file.read()
    file_path_bytes = file_path.encode('utf-8') + b'\0'
    output_data = image_data + delimiter1 + file_path_bytes + delimiter2 + file_data 
    with open(image_path, 'wb') as output_file:
        output_file.write(output_data)

def encrypt_file(file_path, encryption_key):
    fernet = Fernet(encryption_key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def generate_key():
    return Fernet.generate_key()

def encrypt_and_embed_file(image_path, file_path):
    encryption_key = generate_key()
    encrypt_file(file_path, encryption_key)
    embed_file(image_path, file_path)
    delete_file(file_path)
    print("Encryption key (keep this safe) : ",encryption_key.decode())

if __name__ == "__main__":
    img = input("Enter image name : ")
    file = input("Enter file name : ")
    encrypt_and_embed_file(img, file)
