import zipfile
from cryptography.fernet import Fernet
import base64
import io

def encrypt_file(input_file_path, encryption_key, output_file_path):
    fernet = Fernet(encryption_key)
    with open(input_file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(output_file_path, 'wb') as file:
        file.write(encrypted_data)

def embed_file(image_path, file_path, output_image_path):
    delimiter = b'END_OF_IMAGE_DATA'
    
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Append delimiter and file data to image data
    output_data = image_data + delimiter + file_data
    
    with open(output_image_path, 'wb') as output_file:
        output_file.write(output_data)


def extract_file_from_image(image_path, output_file_path, key):
    delimiter = b'END_OF_IMAGE_DATA'
    
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    # Find the start of the file data
    start_index = image_data.find(delimiter)
    
    if start_index == -1:
        raise ValueError("No file data delimiter found in the image")
    
    # Extract the file data
    file_data = image_data[start_index + len(delimiter):]
    
    # Debug: Print the beginning of the file data in hexadecimal
    print(f"Extracted file data starts with: {file_data[:20].hex()}")
    print(f"Extracted file data length: {len(file_data)}")
    
    # Compare the length of the extracted data to the original encrypted data length
    with open('file_encrypted.zip', 'rb') as encrypted_file:
        original_encrypted_data = encrypted_file.read()
    
    print(f"Original encrypted data length: {len(original_encrypted_data)}")
    
    # Ensure that the length of the extracted data matches the expected length
    if len(file_data) != len(original_encrypted_data):
        raise ValueError("Length of extracted data does not match the original encrypted data length")
    
    # Decrypt the file data
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(file_data)
        print("Decryption successful")
    except Exception as e:
        print(f"Decryption failed: {e}")
        return
    
    # Write the decrypted data to the output file
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)
    
    print(f"Decrypted file saved as {output_file_path}")


def generate_key():
    return Fernet.generate_key()

# Example usage:
if __name__ == "__main__":
    encryption_key = generate_key()
    print(f"Encryption key (keep this safe): {encryption_key.decode()}")

    # Encrypt the ZIP file
    encrypt_file('file.zip', encryption_key, 'file_encrypted.zip')

    # Embed the encrypted ZIP file into the PNG image
    embed_file('img.png', 'file_encrypted.zip', 'output.png')

    # Extract and decrypt
    extract_file_from_image('output.png', 'extracted_file.zip', encryption_key)