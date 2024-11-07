"""
This module provides a FastAPI application for predicting energy consumption.
"""
from config import app

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

class PredictionInput(BaseModel):
    """
    Model for input data required for prediction.
    """
    type_batiment: str
    hauteur_plafond: float
    etiquette_dpe: str
    annee_construction: int
    code_insee: int
    surface_habitable: float
    type_energie: str
    isolation_toiture: int
    classe_inertie_batiment: str
    
class PredictionOutput(BaseModel):
    """
    Model for output data of the prediction.
    """
    Conso_5_usages_e_finale: float

def predict_from_df(df: pd.DataFrame):
    """
    Endpoint for predicting energy consumption from input dictionary.
    """
    from sklearn.base import BaseEstimator, TransformerMixin
    import category_encoders as ce
    import joblib

    # Transformateur personnalisé pour convertir la colonne isolation toiture en type `str`
    class ConvertToStrTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self  # Rien à ajuster
        
        def transform(self, X):
            # Conversion de la colonne en type `str`
            return X.astype(str)
        
    class TargetEncodingTransformer(BaseEstimator, TransformerMixin):
        def __init__(self, cols=None):
            self.cols = cols
            self.encoder = ce.TargetEncoder(cols=self.cols)
        
        def fit(self, X, y):
            self.encoder.fit(X, y)
            return self
        
        def transform(self, X):
            return self.encoder.transform(X)

    # Load the model
    model = joblib.load("./models/scripts/pipeline_ml_regression.pkl")
    print(model)
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
            input_data.type_batiment,
            input_data.hauteur_plafond,
            input_data.etiquette_dpe,
            input_data.annee_construction,
            input_data.code_insee,
            input_data.surface_habitable,
            input_data.type_energie,
            input_data.isolation_toiture,
            input_data.classe_inertie_batiment
        ]
        # Convert the input data to a DataFrame
        input_df = pd.DataFrame([data], columns=[
            "type_batiment",
            "hauteur_plafond",
            "etiquette_dpe",
            "annee_construction",
            "code_insee",
            "surface_habitable",
            "type_energie",
            "isolation_toiture",
            "classe_inertie_batiment"
        ])

        # Force change types
        input_df = input_df.astype({
            "type_batiment": "object",
            "hauteur_plafond": "float64",
            "etiquette_dpe": "object",
            "annee_construction": "int64",
            "code_insee": "int64",
            "surface_habitable": "float64",
            "type_energie": "object",
            "isolation_toiture": "int64",
            "classe_inertie_batiment": "object"
        })
        
        prediction = predict_from_df(input_df)
        # print(input_df)
        return PredictionOutput(Conso_5_usages_e_finale=0.0)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
