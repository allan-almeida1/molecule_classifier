#!/usr/bin/env python

import pickle
import numpy as np
from lightgbm import LGBMClassifier


class Classifier:
    """
    This class uses a trained LightGBM model to make predictions on
    molecules.
    """

    def __init__(self):
        self.model: LGBMClassifier = None
        self.load_model()

    def load_model(self):
        """
        Load the trained model.
        """
        try:
            self.model = pickle.load(open("data/model.pkl", "rb"))
        except Exception as e:
            raise ValueError(f"An error occurred while loading the model: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make prediction on the input data.

        Args:
            X (np.ndarray): The input data.

        Returns:
            np.ndarray: The prediction.
        """
        return self.model.predict_proba(X)
