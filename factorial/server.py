from flask import Flask, request, jsonify, render_template
from math import factorial

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/factorial', methods=['POST'])
def calculate_factorial():

    try:
        
        data = request.get_json()
        number = int(data['number'])
        result = factorial(number)
        x = {'factorial':result}
        return x, 200

    except Exception as e: 

        error_msg = str(e)
        err = {'error' : error_msg}
        return jsonify(err), 400


app.run(debug=True)