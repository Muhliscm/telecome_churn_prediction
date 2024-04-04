import pandas as pd
import pickle
import numpy as np


def load_data():
    try:
        df = pd.read_csv('for_prediction.csv')
        df.drop(columns="Churn", inplace=True)
    except Exception as ex:
        print(f"Exception ex:{ex} occurred in loading data")
        raise (ex)
    return df


def load_model():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    except Exception as ex:
        print(f"Exception ex:{ex} occurred in loading model")
        raise (ex)
    return model


def predict(data):
    model = load_model()
    prediction = model.predict(data)
    probability = model.predict_proba(data)
    probability = np.ravel(probability)
    return prediction, probability
