from flask import Flask, request, jsonify
from math import factorial

app = Flask(__name__)

@app.route('/factorial', methods=['POST'])
def calculate_factorial():

    try:
        
        data = request.get_json()
        number = int(data['number'])
        result = factorial(number)
        x = {'factorial':result}
        return x, 200

    except: 

        error_msg = "random error occured" 
        err = {'error' : error_msg}
        return jsonify(err), 400


app.run(debug=True)