import requests


url = 'http://localhost:5000/decode'

image_path = input('enter image name : ')
encryption_key = input('enter encryption key : ')


files = {'img_file': open(image_path, 'rb')}
data = {'encryption_key': encryption_key}


response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open('decoded_file', 'wb') as f:
        f.write(response.content)
    print("File decoded and saved as 'decoded_file'.")
else:
    print(f"Error: {response.json().get('error', 'Unknown error')}")
