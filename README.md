# Molecule Classifier

<div align="center">
<img src="app/static/icon/android-chrome-512x512.png" width="300"/>
</div>

## Overview

This is a web application that uses a machine learning model (LGBM) to classify molecules as Activator, Inhibitor, or Inactive. Draw a molecule in the Ketcher app and click the `SEND` button to classify it. The model was trained on a dataset from the NCATS CYP3A4 assay, which contains 5,239 molecules.

The model was trained using the `LightGBM` library, which is a gradient boosting framework that uses tree-based learning algorithms.

This web application was developed using Flask, a micro web framework for Python. It uses the [EPAM Ketcher](https://lifescience.opensource.epam.com/ketcher/) app to draw molecules and the RDKit library to convert the molecule SMILES string to a descriptor vector.

## Testing Environments

This application was tested in the following operating systems:

- Ubuntu 20.04
- Windows 11

<div style="display: inline_block">
<img align="center" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ubuntu/ubuntu-original-wordmark.svg"  width="150"/>
<img align="center" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/windows11/windows11-original-wordmark.svg" width="150"/>
</div>

The following web browsers were tested:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge

<div style="display: inline_block">
<img align="center" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/chrome/chrome-original.svg" width="80" height="80"/>
<img align="center" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/firefox/firefox-original.svg" width="80" height="80"/>
<img align="center" src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Microsoft_Edge_logo_%282019%29.png" width="80" height="80"/>
          
</div>

## Dependencies

### Python

This project requires Python 3.8 or higher. You can download Python from the [official website](https://www.python.org/downloads/).

### PIP

PIP is a package manager for Python. You can install it by running the following command:

```bash
python -m ensurepip --upgrade
```

### Python Libraries

It is recommended to create a virtual environment to manage the dependencies for this project. You can create a virtual environment by running the following command:

```bash
python -m venv venv
```

Activate the virtual environment by running the following command:

```bash
source venv/bin/activate
```

Once the virtual environment is activated, you can install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

Make sure you have activated the virtual environment before running the application. You can run the application by executing the following command:

```bash
python run.py
# or for hot reloading (development)
flask --app run.py --debug run
```

The application will be running on `http://localhost:5000/`.

Open the URL in a web browser and you should see the home page of the application, just like the screenshot below:

![Home Page](screenshot/home.png)

## Usage

1. Draw a molecule in the Ketcher app. You can use the tools on the left side to draw the molecule or you can paste a SMILES string in the input box. To paste a SMILES string press `Ctrl + O` on your keyboard or select the folder icon on the top left corner of the Ketcher app.

2. Click the `SEND` button to classify the molecule.

3. The classification result will be displayed on the screen.

![Classification Result](screenshot/result.png)
