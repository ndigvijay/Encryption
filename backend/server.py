from flask import Flask, request, jsonify

app=Flask(__name__)

@app.route("/")
def hello_world():
    return jsonify({"message":"home page"}),200

if __name__=="__main__":
    app.run(debug=True)