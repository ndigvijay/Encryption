from cryptography.fernet import Fernet
import os

# def extract_file_from_image(image_path, output_file_path, key):
#     delimiter = b'END_OF_IMAGE_DATA'
#     with open(image_path, 'rb') as image_file:
#         image_data = image_file.read()
#     start_index = image_data.find(delimiter)
#     if start_index == -1:
#         raise ValueError("No file data found in the image")
#     file_data = image_data[start_index + len(delimiter):]
#     fernet = Fernet(key)
#     decrypted_data = fernet.decrypt(file_data)
#     with open(output_file_path, 'wb') as file:
#         file.write(decrypted_data)

def delete_file(file_path):
    os.remove(file_path)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    decrypted_data = fernet.decrypt(file_data)
    with open(file_path, 'wb') as output_file:
        output_file.write(decrypted_data)

def extract_file(image_path):
    delimiter1 = b'END_OF_IMAGE_DATA'
    delimiter2 = b'END_OF_FILE_PATH'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    pos1 = image_data.find(delimiter1)
    if pos1 == -1:
        raise ValueError("Delimiter 1 not found in image data")
    pos2 = image_data.find(delimiter2, pos1 + len(delimiter1))
    if pos2 == -1:
        raise ValueError("Delimiter 2 not found in image data")
    file_path_bytes = image_data[pos1 + len(delimiter1):pos2]
    file_path = file_path_bytes.decode('utf-8').rstrip('\0')
    file_data = image_data[pos2 + len(delimiter2):]
    with open(file_path, 'wb') as output_file:
        output_file.write(file_data)
    return file_path

def extract_and_decrypt_file_from_image(image_path):
    file_path = extract_file(image_path)
    delete_file(image_path)
    encryption_key =  input("Enter the encryption key : ")
    decrypt_file(file_path, encryption_key)

if __name__ == "__main__":
    img = input("Enter image name : ")
    extract_and_decrypt_file_from_image(img)
