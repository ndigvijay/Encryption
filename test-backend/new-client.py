import requests


server_url = 'http://127.0.0.1:5000/encode'

# img_path = input("Enter image name : ")
# file_path = input("Enter file name : ")

img_path = 'img.png'
file_path = 'kaggle.json'

    
files = {'img': open(img_path, 'rb'), 'file': open(file_path, 'rb')}
response = requests.post(server_url, files=files)


if response.status_code == 200:

    response_json = response.json()
    encryption_key = response_json.get('encryption_key')
    download_link = response_json.get('download_link')
    
    image_response = requests.get(f'http://127.0.0.1:5000{download_link}')


    if image_response.status_code == 200:

        with open('embedded_image.png', 'wb') as out_file:
            out_file.write(image_response.content)
        
        print('Image received and saved')
        print(f'Encryption Key: {encryption_key}')
    
    else:

        print("the download error is : \n", image_response.json()['error'])

else:

    print('the encode error is : \n', response.json()['error'])
