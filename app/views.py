from flask import Blueprint, send_from_directory, render_template, jsonify

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


ketcher = Blueprint('ketcher', __name__)


@ketcher.route('/', methods=['GET'])
def serve_ketcher():
    return send_from_directory('static/ketcher', 'index.html')


@ketcher.route('/static/<path:filename>', methods=['GET'])
def serve_ketcher_static(filename):
    return send_from_directory('static/ketcher/static', filename)


api = Blueprint('api', __name__)


@api.route('/molecule-classifier/predict', methods=['POST'])
def predict():
    response = {
        'success': True,
        'prediction_id': 1,
        'prediction_class': 'Inactive'
    }
    return jsonify(response)
