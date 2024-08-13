from cryptography.fernet import Fernet
import io

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
    
    # Decrypt the file data
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(file_data)
    
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)

# Example usage
if __name__ == "__main__":
    
    img = input("Enter the name of the image : ")
    encryption_key = input("Enter a password/encryption key : ")    

    extract_file_from_image(img, 'extracted_file.dat', encryption_key)
