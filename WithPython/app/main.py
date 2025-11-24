# ESTE ARCHIVO LEVANTA LA API CON REGRESIÓN LINEAL Y XGBOOST

from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:4200",  # La URL  aplicación Angular
    "http://127.0.0.1:4200",  # Otra variante de la URL app Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes desde estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Cargar los modelos de Regresión Lineal
linear_model = joblib.load("models/linear_model.joblib")

# Cargar los modelos individuales de Regresión Lineal
linear_models_individual = {}
for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
    linear_models_individual[target] = joblib.load(f"models/linear_model_{target}.joblib")

# Cargar los modelos de XGBoost
xgb_model = joblib.load("models/xgb_model.joblib")

# Cargar los modelos individuales de XGBoost
xgb_models_individual = {}
for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
    xgb_models_individual[target] = joblib.load(f"models/xgb_model_{target}.joblib")

# Parámetros de estandarización (valores reales del dataset después de aplicar np.log1p Transformación Logarítmica)
means = {
    "t_design_log": 0.5139683141448294,
    "t_frontend_log": 1.6632931954862227,
    "t_backend_log": 1.5972817986147338,
    "t_qa_log": 0.8876860096797844,
    "s_frontend_log": 1.0756553307100052,
    "s_backend_log": 1.1552521483046234,
    "lf_react_log": 0.3090965285092238,
    "lf_angular_log": 0.22985931219392622,
    "lf_javascript_log": 0.040689381351098744,
    "lb_node_log": 0.4290231261756201,
    "lb_dotnet_log": 0.13134817839652926,
    "lb_java_log": 0.07138487956333113,
    "Complexity_value_log": 1.534672696308243
}

stds = {
    "t_design_log": 0.8037391908356493,
    "t_frontend_log": 1.0505904783246762,
    "t_backend_log": 1.17712344056498,
    "t_qa_log": 0.7962915554678553,
    "s_frontend_log": 0.14172667092101315,
    "s_backend_log": 0.14157364887583546,
    "lf_react_log": 0.34463006522810696,
    "lf_angular_log": 0.3264136865603088,
    "lf_javascript_log": 0.16297785661563644,
    "lb_node_log": 0.3367101236673176,
    "lb_dotnet_log": 0.27171546275960395,
    "lb_java_log": 0.21073038166639868,
    "Complexity_value_log": 0.618764319244126
}

# Modelo de datos para validar la entrada del usuario (en horas o escala original)
class PredictionInput(BaseModel):
    s_frontend: float
    s_backend: float
    lf_react: float
    lf_angular: float
    lf_javascript: float
    lb_node: float
    lb_dotnet: float
    lb_java: float
    Complexity_value: float

# Función para transformar y estandarizar datos de entrada
def transform_input(data: dict):
    df = pd.DataFrame([data])
    # Renombrar columnas al formato esperado por el modelo
    df.columns = [
        "s_frontend", "s_backend", "lf_react", "lf_angular", "lf_javascript",
        "lb_node", "lb_dotnet", "lb_java", "Complexity_value"
    ]
    # Guardar las columnas originales antes de transformar
    original_cols = df.columns.tolist()
    # Aplicar transformación logarítmica (sumamos 1 para evitar log(0))
    for col in original_cols:
        df[f"{col}_log"] = np.log1p(df[col])
    # Estandarizar los valores transformados (solo las columnas originales)
    for col in original_cols:
        df[f"{col}_log"] = (df[f"{col}_log"] - means[f"{col}_log"]) / stds[f"{col}_log"]
    # Eliminar columnas no transformadas
    df = df[[col for col in df.columns if "_log" in col]]
    return df

# Función para revertir la transformación de las predicciones
def inverse_transform_prediction(prediction: float, target: str):
    # Asegurarse de que prediction es un float nativo de Python
    prediction = float(prediction)  # Convertir desde numpy.float32 o float64
    # Desestandarizar
    prediction_unscaled = (prediction * stds[target]) + means[target]
    # Revertir logaritmo
    prediction_hours = np.expm1(prediction_unscaled)  # exp(x) - 1
    # Asegurarse de que el valor no sea negativo (mínimo 0 horas)
    prediction_hours = max(prediction_hours, 0.0)
    return prediction_hours

@app.get("/")
def read_root():
    return {"message": "¡API con Regresión Lineal y XGBoost en funcionamiento!"}

# Endpoints para Regresión Lineal (originales)
@app.post("/predict-all/")
def predict_all(data: PredictionInput):
    # Transformar los datos de entrada
    input_df = transform_input(data.dict())
    
    # Predecir con el modelo general de Regresión Lineal
    predictions = {}
    for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
        pred = linear_model[target].predict(input_df)[0]
        # Revertir transformación para devolver en horas
        pred_hours = inverse_transform_prediction(pred, target)
        predictions[target.replace("_log", "")] = pred_hours
    
    return {"predictions": predictions}

@app.post("/predict-design/")
def predict_design(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = linear_models_individual["t_design_log"].predict(input_df)[0]
    pred_hours = inverse_transform_prediction(pred, "t_design_log")
    return {"prediction_t_design": pred_hours}

@app.post("/predict-frontend/")
def predict_frontend(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = linear_models_individual["t_frontend_log"].predict(input_df)[0]
    pred_hours = inverse_transform_prediction(pred, "t_frontend_log")
    return {"prediction_t_frontend": pred_hours}

@app.post("/predict-backend/")
def predict_backend(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = linear_models_individual["t_backend_log"].predict(input_df)[0]
    pred_hours = inverse_transform_prediction(pred, "t_backend_log")
    return {"prediction_t_backend": pred_hours}

@app.post("/predict-qa/")
def predict_qa(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = linear_models_individual["t_qa_log"].predict(input_df)[0]
    pred_hours = inverse_transform_prediction(pred, "t_qa_log")
    return {"prediction_t_qa": pred_hours}

# Endpoints para XGBoost (nuevos)
@app.post("/predict-all-xgb/")
def predict_all_xgb(data: PredictionInput):
    # Transformar los datos de entrada
    input_df = transform_input(data.dict())
    
    # Predecir con el modelo general de XGBoost
    predictions = {}
    for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
        pred = xgb_model[target].predict(input_df)[0]
        # Convertir explícitamente a float nativo de Python
        pred = float(pred)
        # Revertir transformación para devolver en horas
        pred_hours = inverse_transform_prediction(pred, target)
        predictions[target.replace("_log", "")] = pred_hours
    
    return {"predictions": predictions}

@app.post("/predict-design-xgb/")
def predict_design_xgb(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = xgb_models_individual["t_design_log"].predict(input_df)[0]
    # Convertir explícitamente a float nativo de Python
    pred = float(pred)
    pred_hours = inverse_transform_prediction(pred, "t_design_log")
    return {"prediction_t_design": pred_hours}

@app.post("/predict-frontend-xgb/")
def predict_frontend_xgb(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = xgb_models_individual["t_frontend_log"].predict(input_df)[0]
    # Convertir explícitamente a float nativo de Python
    pred = float(pred)
    pred_hours = inverse_transform_prediction(pred, "t_frontend_log")
    return {"prediction_t_frontend": pred_hours}

@app.post("/predict-backend-xgb/")
def predict_backend_xgb(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = xgb_models_individual["t_backend_log"].predict(input_df)[0]
    # Convertir explícitamente a float nativo de Python
    pred = float(pred)
    pred_hours = inverse_transform_prediction(pred, "t_backend_log")
    return {"prediction_t_backend": pred_hours}

@app.post("/predict-qa-xgb/")
def predict_qa_xgb(data: PredictionInput):
    input_df = transform_input(data.dict())
    pred = xgb_models_individual["t_qa_log"].predict(input_df)[0]
    # Convertir explícitamente a float nativo de Python
    pred = float(pred)
    pred_hours = inverse_transform_prediction(pred, "t_qa_log")
    return {"prediction_t_qa": pred_hours}


# NEW ENDPOINT FOR PREDICTING A LIST OF INPUTS

# Modelo de datos para validar una sola entrada (ya lo tienes)
class PredictionInput(BaseModel):
    s_frontend: float
    s_backend: float
    lf_react: float
    lf_angular: float
    lf_javascript: float
    lb_node: float
    lb_dotnet: float
    lb_java: float
    Complexity_value: float

# Nuevo modelo para validar un listado de entradas
class PredictionInputList(BaseModel):
    inputs: List[PredictionInput]


# Endpoint para Regresión Lineal (procesar un listado)
@app.post("/predict-all-batch/")
def predict_all_batch(data: PredictionInputList):
    # Lista para almacenar las predicciones de todas las entradas
    all_predictions = []
    
    # Procesar cada entrada en el listado
    for input_data in data.inputs:
        # Transformar los datos de entrada
        input_df = transform_input(input_data.dict())
        
        # Predecir con el modelo general de Regresión Lineal
        predictions = {}
        for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
            pred = linear_model[target].predict(input_df)[0]
            # Revertir transformación para devolver en horas
            pred_hours = inverse_transform_prediction(pred, target)
            predictions[target.replace("_log", "")] = pred_hours
        
        # Añadir las predicciones al listado de resultados
        all_predictions.append({
            "input": input_data.dict(),  # Incluir la entrada original
            "predictions": predictions
        })
    
    return {"batch_predictions": all_predictions}


# Endpoint para XGBoost (procesar un listado)
@app.post("/predict-all-batch-xgb/")
def predict_all_batch_xgb(data: PredictionInputList):
    # Lista para almacenar las predicciones de todas las entradas
    all_predictions = []
    
    # Procesar cada entrada en el listado
    for input_data in data.inputs:
        # Transformar los datos de entrada
        input_df = transform_input(input_data.dict())
        
        # Predecir con el modelo general de XGBoost
        predictions = {}
        for target in ["t_design_log", "t_frontend_log", "t_backend_log", "t_qa_log"]:
            pred = xgb_model[target].predict(input_df)[0]
            # Convertir explícitamente a float nativo de Python
            pred = float(pred)
            # Revertir transformación para devolver en horas
            pred_hours = inverse_transform_prediction(pred, target)
            predictions[target.replace("_log", "")] = pred_hours
        
        # Añadir las predicciones al listado de resultados
        all_predictions.append({
            "input": input_data.dict(),  # Incluir la entrada original
            "predictions": predictions
        })
    
    return {"batch_predictions": all_predictions}


#Para mejorar la usabilidad de la API y permitir al frontend enviar múltiples entradas simultáneamente, se implementaron dos nuevos endpoints: /predict-all-batch/ para Regresión Lineal y /predict-all-batch-xgb/ para XGBoost. Estos endpoints reciben un listado de entradas en el formato definido por el modelo PredictionInput, procesan cada entrada de manera independiente utilizando las funciones existentes de transformación y predicción, y devuelven un listado de resultados que incluye las entradas originales y las predicciones correspondientes. Esta funcionalidad permite realizar predicciones masivas de manera eficiente, lo que es útil para escenarios donde se necesitan estimaciones para múltiples proyectos o configuraciones al mismo tiempo.