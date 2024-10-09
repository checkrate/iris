from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from joblib import load

model = load('./model.joblib')
scaler = load('./scaler.joblib')
app = FastAPI()

# Определяем модель данных для входных параметров
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Определяем модель данных для выходных параметров
class PredictionResult(BaseModel):
    predicted_species: int

@app.post("/predict", response_model=PredictionResult)
@app.get("/predict")
async def predict_species(sepal_length: float = None, sepal_width: float = None, petal_length: float = None, petal_width: float = None):
    try:
        if None in (sepal_length, sepal_width, petal_length, petal_width):
            raise HTTPException(status_code=400, detail="All input parameters are required")

        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        input_data_scaled = scaler.transform(input_data)
        prediction = model.predict(input_data_scaled)
        species = prediction[0]

        return {"predicted_species": int(species)}

    except Exception as e:
        # Возвращаем ошибку HTTP 500 в случае любой непредвиденной ошибки
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {e}")
