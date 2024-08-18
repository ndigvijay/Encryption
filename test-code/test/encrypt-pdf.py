from cryptography.fernet import Fernet

def encrypt_file(input_file_path, encryption_key, output_file_path):
    """Encrypts the input file and saves it to output file path."""
    fernet = Fernet(encryption_key)
    with open(input_file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(output_file_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"Encrypted file size: {len(encrypted_data)} bytes")

def embed_file(image_path, file_path, output_image_path, marker=b'FILESTART'):
    """Embeds the encrypted file into the image with a marker."""
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Embed marker and file data into the image data
    output_data = image_data + marker + file_data
    with open(output_image_path, 'wb') as output_file:
        output_file.write(output_data)
    print(f"Embedded image size: {len(output_data)} bytes")

def extract_file_from_image(image_path, output_file_path, key, marker=b'FILESTART'):
    """Extracts and decrypts the file from the image."""
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    # Locate the marker
    start_index = image_data.find(marker)
    if start_index == -1:
        raise ValueError("No file found in the image")

    # Extract the file data
    file_data = image_data[start_index + len(marker):]
    print(f"Extracted file data size: {len(file_data)} bytes")
    
    # Decrypt the file data
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(file_data)
        with open(output_file_path, 'wb') as file:
            file.write(decrypted_data)
        print(f"Decrypted file size: {len(decrypted_data)} bytes")
    except Exception as e:
        print(f"Decryption failed: {e}")

def generate_key():
    """Generates a new encryption key."""
    return Fernet.generate_key()

# Example usage
if __name__ == "__main__":
    # Generate a key for encryption
    encryption_key = generate_key()
    print(f"Encryption key (keep this safe): {encryption_key.decode()}")

    file = input("Enter the name of the file to encrypt: ")
    img = input("Enter the name of the image to embed into: ")

    # Encrypt the file
    encrypt_file(file, encryption_key, 'document_encrypted.dat')
    
    # Embed the encrypted file into the image
    embed_file(img, 'document_encrypted.dat', f'enc-{img}')
    
    # Extract the file from the image
    output_file = input("Enter the name for the extracted file: ")
    try:
        extract_file_from_image(f'enc-{img}', output_file, encryption_key)
        print(f"File extracted successfully to {output_file}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")