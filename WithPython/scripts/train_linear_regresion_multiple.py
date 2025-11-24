
# # ESTE SCRIPT ENTRENA EL MODELO DE REGRESIÓN LINEAL MULTIPLE 

# import pandas as pd
# import numpy as np
# from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, mean_absolute_error
# import joblib
# import matplotlib.pyplot as plt
# from sklearn.metrics import r2_score

# # Cargar el dataset
# try:
#     df_updated = pd.read_csv("data/dataset_limpio_transformado_estandarizado_sin_constantes.csv")
# except FileNotFoundError:
#     print("Error: El archivo CSV no se encontró.")
#     exit()
    
# # Separar variables independientes (X) y dependientes (y)
# target_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log']
# X = df_updated.drop(columns=target_cols)
# y = df_updated[target_cols]

# # Dividir en entrenamiento (80%) y prueba (20%)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Entrenar el modelo de Regresión Lineal Múltiple para todas las variables objetivo
# linear_model = {}
# for target in target_cols:
#     model = LinearRegression()
#     model.fit(X_train, y_train[target])
#     linear_model[target] = model
#     print(f"Modelo de Regresión Lineal para {target} entrenado.")

# # Evaluar el modelo en el conjunto de prueba
# for target in target_cols:
#     y_pred = linear_model[target].predict(X_test)
#     rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))
#     mae = mean_absolute_error(y_test[target], y_pred)
#     scores = cross_val_score(linear_model[target], X, y[target], cv=5, scoring='neg_mean_squared_error')
#     rmse_cv = np.sqrt(-scores.mean())
#     r2 = r2_score(y_test[target], y_pred)  # Calcular R² en el conjunto de prueba
#     r2_cv = cross_val_score(linear_model[target], X, y[target], cv=5, scoring='r2').mean()  # R² con validación cruzada
    
#     #Imprimir las métricas
#     print(f"\nMétricas para {target}:")
#     print(f"RMSE: {rmse:.4f}")
#     print(f"MAE: {mae:.4f}")
#     print(f"RMSE promedio (CV) para {target}: {np.sqrt(-scores.mean()):.4f}")
#     print(f"Coeficiente de Determinación (R²) en prueba: {r2:.4f}")
#     print(f"Coeficiente de Determinación promedio (CV, R²): {r2_cv:.4f}")
    
#     #Visualización predicciones vs reales
#     plt.figure(figsize=(7, 5))
#     plt.scatter(y_test[target], y_pred, color="royalblue", alpha=0.7, label="Valores Predichos")
#     plt.plot([min(y_test[target]), max(y_test[target])], [min(y_test[target]), max(y_test[target])], 
#             color="red", linestyle="dashed", linewidth=2, label="Referencia: Predicción Exacta")

#     plt.xlabel(f"Valores Reales ({target})")
#     plt.ylabel(f"Valores Predichos ({target})")
#     plt.title(f"Comparación: Valores Reales vs Predichos ({target})")
#     plt.legend()
#     plt.grid(True, linestyle="--", alpha=0.6)
#     plt.show()
    
#     #Reporte de coeficientes: ¿Qué variables son las más influyentes?
#     print(f"\n=== Coeficientes para {target} ===")
#     coef_df = pd.DataFrame({
#         "Variable": X.columns,
#         "Coeficiente": linear_model[target].coef_
#     })
#     print(coef_df.to_string(index=False))
#     print(f"Intercepto: {linear_model[target].intercept_:.4f}")

# # Guardar los modelos entrenados en un solo archivo .joblib
# joblib.dump(linear_model, "models/linear_model.joblib")

# # Guardar los modelos individuales en archivos separados
# for target in target_cols:
#     joblib.dump(linear_model[target], f"models/linear_model_{target}.joblib")

# print("\nModelo de Regresión Lineal Múltiple guardado exitosamente en models/linear_model.joblib.")

# ESTE SCRIPT ENTRENA EL MODELO DE REGRESIÓN LINEAL MÚLTIPLE CON GRID SEARCH (usando Ridge)

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.linear_model import Ridge  # Usamos Ridge en lugar de LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt

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

# Definir los hiperparámetros para Grid Search (para Ridge)
param_grid = {
    'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]  # Valores de regularización
}

# Entrenar el modelo de Regresión Lineal Múltiple (Ridge) para todas las variables objetivo con Grid Search
linear_model = {}
for target in target_cols:
    print(f"\nEntrenando modelo de Regresión Lineal (Ridge) para {target} con Grid Search...")
    
    # Definir el modelo base (Ridge)
    model = Ridge()
    
    # Configurar GridSearchCV
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='neg_mean_squared_error',
        cv=5,  # 5-fold cross-validation
        verbose=1,
        n_jobs=-1  # Usar todos los núcleos disponibles
    )
    
    # Ajustar GridSearchCV al conjunto de entrenamiento
    grid_search.fit(X_train, y_train[target])
    
    # Obtener el mejor modelo
    best_model = grid_search.best_estimator_
    linear_model[target] = best_model
    
    # Imprimir los mejores hiperparámetros
    print(f"Mejores hiperparámetros para {target}: {grid_search.best_params_}")
    print(f"Mejor RMSE (CV): {np.sqrt(-grid_search.best_score_):.4f}")
    
    # Evaluar el mejor modelo en el conjunto de prueba
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))
    mae = mean_absolute_error(y_test[target], y_pred)
    r2 = r2_score(y_test[target], y_pred)
    
    # Validación cruzada para R² y RMSE
    scores = cross_val_score(best_model, X, y[target], cv=5, scoring='neg_mean_squared_error')
    rmse_cv = np.sqrt(-scores.mean())
    r2_cv = cross_val_score(best_model, X, y[target], cv=5, scoring='r2').mean()
    
    # Imprimir las métricas
    print(f"\nMétricas para {target}:")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE promedio (CV): {rmse_cv:.4f}")
    print(f"Coeficiente de Determinación (R²) en prueba: {r2:.4f}")
    print(f"Coeficiente de Determinación promedio (CV, R²): {r2_cv:.4f}")
    
    # Visualización predicciones vs reales
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test[target], y_pred, color="royalblue", alpha=0.7, label="Valores Predichos")
    plt.plot([min(y_test[target]), max(y_test[target])], [min(y_test[target]), max(y_test[target])], 
            color="red", linestyle="dashed", linewidth=2, label="Referencia: Predicción Exacta")
    plt.xlabel(f"Valores Reales ({target})")
    plt.ylabel(f"Valores Predichos ({target})")
    plt.title(f"Comparación: Valores Reales vs Predichos ({target}) - Regresión Lineal (Ridge)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
    
    # Reporte de coeficientes: ¿Qué variables son las más influyentes?
    print(f"\n=== Coeficientes para {target} ===")
    coef_df = pd.DataFrame({
        "Variable": X.columns,
        "Coeficiente": best_model.coef_
    })
    print(coef_df.to_string(index=False))
    print(f"Intercepto: {best_model.intercept_:.4f}")

# Guardar los modelos entrenados en un solo archivo .joblib
joblib.dump(linear_model, "models/linear_model.joblib")

# Guardar los modelos individuales en archivos separados
for target in target_cols:
    joblib.dump(linear_model[target], f"models/linear_model_{target}.joblib")

print("\nModelo de Regresión Lineal Múltiple (Ridge) guardado exitosamente en models/linear_model.joblib.")


from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

# Definir el modelo base
model = Ridge(random_state=42)

# Definir los valores de alpha para Grid Search
param_grid = {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]}

# Configurar GridSearchCV
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5,
    verbose=1,
    n_jobs=-1
)

# Ajustar GridSearchCV al conjunto de entrenamiento
grid_search.fit(X_train, y_train[target])
best_model = grid_search.best_estimator_