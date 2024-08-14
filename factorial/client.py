import requests

number = input("Enter a number : ")
data = {'number': number}

response = requests.post(json=data, url='http://127.0.0.1:5000/factorial')
result_dict = response.json()


if response.status_code == 200:

    result = result_dict['factorial']
    print('Factorial : ', result)

else:

    result = result_dict['error']
    print(result)
