"""
This module provides a FastAPI application for predicting energy consumption.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import REG_MODEL_PATH
import joblib
import pandas as pd

app = FastAPI()


class PredictionRegInput(BaseModel):
    """
    Model for input data required for prediction.
    """
    etiquette_dpe: float
    type_batiment: float
    annee_construction: float
    classe_inertie_batiment: float
    hauteur_sous_plafond: float
    surface_habitable_logement: float
    type_energie_principale_chauffage: float
    isolation_toiture: float
    code_postal_ban: float


class PredictionRegOutput(BaseModel):
    """
    Model for output data of the prediction.
    """
    Conso_5_usages_e_finale: float

class PredictionClassifInput(BaseModel):
    """
    Model for input data required for prediction.
    """
    annee_construction: float
    surface_habitable_logement: float
    cout_total_5_usages: float
    cout_ecs: float
    cout_chauffage: float
    cout_eclairage: float
    cout_auxiliaires: float
    cout_refroidissement: float
    
class PredictionClassifOutput(BaseModel):
    """
    Model for output data of the prediction.
    """
    predict_label: str

def predict_from_df(df: pd.DataFrame):
    """
    Endpoint for predicting energy consumption from input dictionary.
    """
    from sklearn.base import BaseEstimator, TransformerMixin
    import category_encoders as ce

    # Load the model
    model = joblib.load(REG_MODEL_PATH)
    y_pred = model.predict(df)

    return y_pred[0]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict_label", response_model=PredictionClassifOutput)
def predict_label(input_dict: dict):
    try:
        if not input_dict:
            raise HTTPException(status_code=400, detail="Input dictionary is empty")

        # Convert input_dict to PredictionClassifInput model
        input_data = PredictionClassifInput(**input_dict)
        
        COLUMN_NAMES = [
            "annee_construction",
            "surface_habitable_logement",
            "cout_total_5_usages",
            "cout_ECS",
            "cout_chauffage",
            "cout_eclairage",
            "cout_auxiliaires",
            "cout_refroidissement"
        ]

        data = [
            input_data.annee_construction,
            input_data.surface_habitable_logement,
            input_data.cout_total_5_usages,
            input_data.cout_ecs,
            input_data.cout_chauffage,
            input_data.cout_eclairage,
            input_data.cout_auxiliaires,
            input_data.cout_refroidissement
        ]

        # # Prepare the input data for prediction
        input_df = pd.DataFrame([data], columns=COLUMN_NAMES)
        
        input_df = input_df.astype({
            "annee_construction": "float64",
            "surface_habitable_logement": "float64",
            "cout_total_5_usages": "float64",
            "cout_ECS": "float64",
            "cout_chauffage": "float64",
            "cout_eclairage": "float64",
            "cout_auxiliaires": "float64",
            "cout_refroidissement": "float64"
        })
        # return "hello"

        # # Reshape the data for prediction
        # data = input_df.values.reshape(1, -1)
        print(input_df.values)
        # # Load the model and encoder
        model, encoder = joblib.load('./models/pipeline_ml_classification.pkl')
        prediction = model.predict(input_df)
        prediction_decoded = encoder.inverse_transform(prediction)

        # return PredictionClassifOutput(predict_label=round(45.900, 2))
        return PredictionClassifOutput(predict_label=prediction_decoded[0])
        # return "Hello"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_consomation", response_model=PredictionRegOutput)
def predict_from_dict(input_dict: dict):
    try:
        if not input_dict:
            raise HTTPException(status_code=400, detail="Input dictionary is empty")

        # Convert input_dict to PredictionRegInput model
        input_data = PredictionRegInput(**input_dict)

        # Prepare the input data for prediction
        data = [
            input_data.etiquette_dpe,
            input_data.type_batiment,
            input_data.annee_construction,
            input_data.classe_inertie_batiment,
            input_data.hauteur_sous_plafond,
            input_data.surface_habitable_logement,
            input_data.type_energie_principale_chauffage,
            input_data.isolation_toiture,
            input_data.code_postal_ban
        ]

        # Convert the input data to a DataFrame
        input_df = pd.DataFrame([data], columns=[
            "Etiquette_DPE",
            "Type_bâtiment",
            "Année_construction",
            "Classe_inertie_bâtiment",
            "Hauteur_sous-plafond",
            "Surface_habitable_logement",
            "Type_énergie_principale_chauffage",
            "Isolation_toiture_(0/1)",
            "Code_postal_(BAN)"
        ])

        # Force change types
        input_df = input_df.astype({
            "Etiquette_DPE": "float64",
            "Type_bâtiment": "float64",
            "Année_construction": "float64",
            "Classe_inertie_bâtiment": "float64",
            "Hauteur_sous-plafond": "float64",
            "Surface_habitable_logement": "float64",
            "Type_énergie_principale_chauffage": "float64",
            "Isolation_toiture_(0/1)": "float64",
            "Code_postal_(BAN)": "float64"
        })

        prediction = predict_from_df(input_df)
        return PredictionRegOutput(Conso_5_usages_e_finale=round(prediction, 2))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
