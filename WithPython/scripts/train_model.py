
# ESTE SCRIPT FUE UTILIZADO INICIALMENTE Y 
# ACTUALMENTE SOLO SE UTILIZA PARA FORMATEAR EL DATASET CAMBIANDO EL SEPARADOR DE PUNTOS POR COMAS

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
import time
import numpy as np

# Variables globales
seconds = 5

# Cargar dataset
df = pd.read_csv("data/dataset_11.csv", decimal=",")
print("Dataset cargado con éxito!")

# Guardar el dataset completo (sin eliminar outliers)
df.to_csv("data/dataset_11_formatted.csv", index=False, decimal=".")
print("Dataset completo guardado con éxito!")

# Separar variables independientes y dependientes
X = df[["type", "s_frontend", "s_backend", "lf_react", "lf_angular", "lf_javascript", "lf_kotlin",
        "lb_node", "lb_dotnet", "lb_java", "Complexity_value"]]
y = df[["t_design", "t_frontend", "t_backend", "t_qa"]]  # Múltiples variables dependientes

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Dataset dividido en entrenamiento y prueba con éxito!")

print("Entrenando modelos...")
time.sleep(seconds)

# Entrenar modelos
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

xgb_model = XGBRegressor(objective='reg:squarederror')
xgb_model.fit(X_train, y_train)

# Guardar los modelos entrenados
with open("models/linear_model.pkl", "wb") as f:
    pickle.dump(linear_model, f)

with open("models/xgb_model.pkl", "wb") as f:
    pickle.dump(xgb_model, f)

print("¡Modelos entrenados y guardados con éxito!")