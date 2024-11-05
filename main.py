"""
This module provides a FastAPI application for predicting energy consumption.
"""
from config import app

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
# import joblib  # or pickle, depending on how you saved your model

app = FastAPI()

class PredictionInput(BaseModel):
    """
    Model for input data required for prediction.
    """
    Type_batiment: str
    Annee_construction: float
    Classe_inertie_batiment: str
    Hauteur_sous_plafond: float
    Surface_habitable_logement: float
    Isolation_toiture: float
    Code_INSEE: str
    Type_energie_principale_chauffage: str
    
class PredictionOutput(BaseModel):
    """
    Model for output data of the prediction.
    """
    Conso_5_usages_e_finale: float

def read_root():
    """
    Root endpoint returning a simple greeting.
    """
def predict_from_df(df: pd.DataFrame):
    """
    Endpoint for predicting energy consumption from input dictionary.
    """
    # Load the model
    model = joblib.load("models/pipeline_ml_regression.pkl")

    # Make predictions on the test set
    
    y_pred = model.predict(df)

    return y_pred.flatten()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict_etiquets", response_model=PredictionOutput)
def predict_from_dict(input_dict: dict):
    try:
        if not input_dict:
            raise HTTPException(status_code=400, detail="Input dictionary is empty")
        
        # Convert input_dict to PredictionInput model
        input_data = PredictionInput(**input_dict)
        
        # Prepare the input data for prediction
        data = [
            input_data.Type_batiment,
            input_data.Annee_construction,
            input_data.Classe_inertie_batiment,
            input_data.Hauteur_sous_plafond,
            input_data.Surface_habitable_logement,
            input_data.Isolation_toiture,
            input_data.Code_INSEE,
            input_data.Type_energie_principale_chauffage
        ]
        
        print(data)
        # Convert the input data to a DataFrame
        input_df = pd.DataFrame([data], columns=[
            "Type_batiment",
            "Annee_construction",
            "Classe_inertie_batiment",
            "Hauteur_sous_plafond",
            "Surface_habitable_logement",
            "Isolation_toiture",
            "Code_INSEE",
            "Type_energie_principale_chauffage"
        ])

        # Force change types
        input_df = input_df.astype({
            "Type_batiment": "object",
            "Annee_construction": "float64",
            "Classe_inertie_batiment": "object",
            "Hauteur_sous_plafond": "float64",
            "Surface_habitable_logement": "float64",
            "Isolation_toiture": "float64",
            "Code_INSEE": "object",
            "Type_energie_principale_chauffage": "object"
        })
        
        return PredictionOutput(Conso_5_usages_e_finale=0.0)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
