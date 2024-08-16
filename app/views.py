from flask import Blueprint, send_from_directory, render_template
from flask import jsonify, request
import numpy as np
from predictor import Classifier
from lib.descriptor_gen import DescriptorGen
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

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
    # Get the input data
    input_data = request.json
    smiles = input_data['smiles']

    if smiles == '':
        response = {
            'success': False,
        }
        return jsonify(response)

    # Generate the molecular descriptors
    desc_gen = DescriptorGen()
    desc = desc_gen.from_smiles(smiles)
    desc = np.stack(desc).reshape(1, -1)

    # Load the model
    model = Classifier()

    # Make prediction
    prediction = model.predict(desc)

    # Get the prediction class with the highest probability
    prediction_class = int(np.argmax(prediction))

    # Prepare the response
    label_map = {0: 'Activator', 1: 'Inactive', 2: 'Inhibitor'}
    response = {
        'success': True,
        'prediction_id': prediction_class,
        'prediction_class': label_map[prediction_class]
    }
    return jsonify(response)
