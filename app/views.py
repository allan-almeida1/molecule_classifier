from flask import Blueprint, send_from_directory, render_template
from flask import jsonify, request
import numpy as np
from predictor import Classifier
from lib.descriptor_gen import DescriptorGen
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

"""
Main views

- Home page
- About page
"""

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    """Render the home page."""

    return render_template('index.html')


@main.route('/about', methods=['GET'])
def about():
    """Render the about page."""

    return render_template('about.html')


"""
Ketcher views

- Serve the Ketcher web app
- Serve the Ketcher static files
"""


ketcher = Blueprint('ketcher', __name__)


@ketcher.route('/', methods=['GET'])
def serve_ketcher():
    """Serve the Ketcher web app."""

    return send_from_directory('static/ketcher', 'index.html')


@ketcher.route('/static/<path:filename>', methods=['GET'])
def serve_ketcher_static(filename):
    """Serve the Ketcher static files."""

    return send_from_directory('static/ketcher/static', filename)


"""
API views

- Predict endpoint
"""

api = Blueprint('api', __name__)


@api.route('/molecule-classifier/predict', methods=['POST'])
def predict():
    """Predict the class of a molecule given its SMILES string."""

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
