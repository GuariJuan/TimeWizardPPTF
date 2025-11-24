# SCRIPT PARA PROBAR REGRESIÓN RIDGE

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Cargar el dataset
try:
    df_updated = pd.read_csv("data/dataset_limpio_transformado_estandarizado_sin_constantes.csv")
except FileNotFoundError:
    print("Error: El archivo CSV no se encontró.")
    exit()

# Separar variables independientes (X) y dependientes (y)
target_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log']
X = df_updated.drop(columns=target_cols)
y = df_updated[target_cols]

# Dividir en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar Ridge con validación cruzada para encontrar el mejor alpha
ridge_model = {}
alphas = [0.01, 0.1, 1.0, 10.0, 100.0]  # Posibles valores de alpha cubren un rango amplio de regularización (desde casi sin penalización hasta una penalización fuerte).
for target in target_cols:
    model = RidgeCV(alphas=alphas, cv=5)  # Se usa validación cruzada (cv=5) para elegir el mejor alpha y evitar seleccionar un valor arbitrario.
    model.fit(X_train, y_train[target])
    ridge_model[target] = model
    print(f"Modelo Ridge para {target} entrenado. Mejor alpha: {model.alpha_}")

# Evaluar el modelo en el conjunto de prueba
for target in target_cols:
    y_pred = ridge_model[target].predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))
    mae = mean_absolute_error(y_test[target], y_pred)
    scores = cross_val_score(ridge_model[target], X, y[target], cv=5, scoring='neg_mean_squared_error')
    rmse_cv = np.sqrt(-scores.mean())
    r2 = r2_score(y_test[target], y_pred)  # Calcular R² en el conjunto de prueba
    r2_cv = cross_val_score(ridge_model[target], X, y[target], cv=5, scoring='r2').mean()  # R² con validación cruzada
    
    # Imprimir las métricas
    print(f"\nMétricas para {target}:")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE promedio (CV) para {target}: {rmse_cv:.4f}")
    print(f"Coeficiente de Determinación (R²) en prueba: {r2:.4f}")
    print(f"Coeficiente de Determinación promedio (CV, R²): {r2_cv:.4f}")
    
    # Visualización
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test[target], y_pred, color="royalblue", alpha=0.7, label="Valores Predichos")
    plt.plot([min(y_test[target]), max(y_test[target])], [min(y_test[target]), max(y_test[target])], 
            color="red", linestyle="dashed", linewidth=2, label="Referencia: Predicción Exacta")

    plt.xlabel(f"Valores Reales ({target})")
    plt.ylabel(f"Valores Predichos ({target})")
    plt.title(f"Comparación: Valores Reales vs Predichos ({target})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
    
    # Reporte de coeficientes
    print(f"\n=== Coeficientes para {target} ===")
    coef_df = pd.DataFrame({
        "Variable": X.columns,
        "Coeficiente": ridge_model[target].coef_
    })
    print(coef_df.to_string(index=False))
    print(f"Intercepto: {ridge_model[target].intercept_:.4f}")

# Guardar los modelos individuales
for target in target_cols:
    joblib.dump(ridge_model[target], f"models/ridge_model_{target}.joblib")

print("\nModelos Ridge guardados exitosamente en la carpeta 'models'.")