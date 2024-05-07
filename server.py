from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from template import Template

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def result():
    req = request.form.to_dict()
    print(req)

    template = Template(
        hardware = req['hardware'],
        num_leds = req['n_of_led'],
        button_colors = req['color_of_buttons'],
        num_buttons = req['n_of_buttons'],
        sensor_boundary = req['ultrasonic_boundary'],
        sensor_color1 = req['ultrasonic_color1'],
        sensor_color2 = req['ultrasonic_color2'],
        no_hardware_color = req['no_hardware_color']
    )

    code = template.synthesize_program()

    response = jsonify({'code': code})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')

    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)