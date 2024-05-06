from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from template import Template

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def result():
    print("here")
    print(request.form.to_dict())
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')

    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)