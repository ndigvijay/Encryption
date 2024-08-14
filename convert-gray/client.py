import requests

server_url = 'http://127.0.0.1:5000/upload'

image_path = input("enter image name : ")

with open(image_path, 'rb') as img_file:
    response = requests.post(server_url, files={'file': img_file})
    
with open('received_grayscale.png', 'wb') as out_file:
    out_file.write(response.content)

print('Grayscale image received and saved as received_grayscale.png')
