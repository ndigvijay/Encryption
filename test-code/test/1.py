from cryptography.fernet import Fernet
import io

def encrypt_file(input_file_path, encryption_key):
    """Encrypts the input file and saves it to output file path."""
    fernet = Fernet(encryption_key)
    with open(input_file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(input_file_path, 'wb') as file:
        file.write(encrypted_data)

def embed_file(image_path, file_path, marker=b'FILESTART'):
    """Embeds the encrypted file into the image with a marker."""
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Embed marker and file data into the image data
    output_data = image_data + marker + file_data
    with open(image_path, 'wb') as output_file:
        output_file.write(output_data)

def generate_key():
    """Generates a new encryption key."""
    return Fernet.generate_key()

# Example usage
if __name__ == "__main__":
    
    # Generate a key for encryption
    encryption_key = generate_key()
    print(f"Encryption key (keep this safe): {encryption_key.decode()}")

    img = input("Enter the name of the image : ")
    # encryption_key = input("Enter a password/encryption key : ")    

    encrypt_file('file.txt', encryption_key)
    embed_file(img, 'file.txt')
