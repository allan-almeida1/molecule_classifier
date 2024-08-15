#!/usr/bin/env python

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import argparse
from lib.descriptor_gen import DescriptorGen
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from lightgbm import LGBMClassifier
import pickle
from tqdm.auto import tqdm
from rdkit import RDLogger
import os

tqdm.pandas()
RDLogger.DisableLog('rdApp.*')


class DataPreprocessor:
    """
    This class is used to preprocess the data.
    """

    def __init__(self):
        self.df = None

    def read_csv(self, path: str):
        """
        Read the csv file.

        Args:
            path (str): The path to the csv file.
        """
        try:
            self.df = pd.read_csv(
                path, skiprows=[1, 2, 3, 4, 5], low_memory=False)
        except Exception as e:
            raise ValueError(
                f"An error occurred while reading the csv file: {e}")

    def drop_na(self):
        """
        Drop the rows with missing values.
        """
        self.df.dropna(inplace=True, subset=["PUBCHEM_CID"])

    def encode_labels(self):
        """
        Encode the labels to integers and store them in a the `label` column.
        """
        labels = self.df['Phenotype-Replicate_1'].unique().tolist()
        le = LabelEncoder()
        le.fit(labels)
        self.df['label'] = le.transform(self.df['Phenotype-Replicate_1'])

    def get_data(self) -> pd.DataFrame:
        """
        Drop the columns that are not needed and return the preprocessed data.

        Returns:
            pd.DataFrame: The preprocessed data.
        """
        df = self.df[["PUBCHEM_CID", "PUBCHEM_EXT_DATASOURCE_SMILES",
                      "Phenotype-Replicate_1", "label"]]
        return df.copy()


def print_green(text: str):
    """
    Print the text in green color.

    Args:
        text (str): The text to print.
    """
    print("\033[32m" + text + "\033[0m")


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(
        description="A script to train a model to predict the \
            phenotype of a molecule.")
    parser.add_argument("--input", "-i", type=str,
                        help="The path to the input csv file.", required=True)
    parser.add_argument("--output", "-o", type=str,
                        help="The path to the output trained model.")

    # Parse the arguments
    args = parser.parse_args()
    if args.input is None:
        raise ValueError("Please provide the path to the input csv file.")
    if args.output is None:
        output_path = "model.pkl"
    else:
        exists = os.path.exists(args.output)
        if not exists:
            raise ValueError("The output path does not exist.")
        is_dir = os.path.isdir(args.output)
        if not is_dir:
            if args.output.endswith(".pkl"):
                output_path = args.output
            else:
                raise ValueError(
                    "The output path should end with .pkl extension.")
        else:
            output_path = os.path.join(args.output, "model.pkl")

    # Preprocess the data
    print_green("1. Preprocessing the data...\0")
    data_preprocessor = DataPreprocessor()
    data_preprocessor.read_csv(args.input)
    data_preprocessor.drop_na()
    data_preprocessor.encode_labels()
    df = data_preprocessor.get_data()

    # Generate the descriptors
    print_green("2. Generating the descriptors...")
    desc_gen = DescriptorGen()
    df.loc[:, 'desc'] = df['PUBCHEM_EXT_DATASOURCE_SMILES'].progress_apply(
        desc_gen.from_smiles)

    # Prepare the data for training
    print_green("3. Preparing the data for training...")
    train_X: np.ndarray = np.stack(df['desc'])
    train_y = df['label']
    print("Number of data points before oversampling: ", train_X.shape[0])
    oversampler = RandomOverSampler()
    train_X, train_y = oversampler.fit_resample(train_X, train_y)
    print("Number of data points after oversampling: ", train_X.shape[0])

    # Train the model
    print_green("4. Training the model...")
    model = LGBMClassifier()
    model.fit(train_X, train_y)

    # Export the model
    print_green("5. Exporting the model...")
    with open(output_path, "wb") as f:
        pickle.dump(model, f)

    print_green(f"Model saved at {output_path}")
