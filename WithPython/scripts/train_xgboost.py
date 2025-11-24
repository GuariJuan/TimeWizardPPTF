# # ESTE SCRIPT ENTRENA EL MODELO XGBOOST 

# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split, KFold
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# from xgboost import XGBRegressor, plot_tree
# import joblib
# import matplotlib.pyplot as plt

# # Cargar el dataset
# df_updated = pd.read_csv("data/dataset_limpio_transformado_estandarizado_sin_constantes.csv")

# # Separar variables independientes (X) y dependientes (y)
# target_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log']
# X = df_updated.drop(columns=target_cols)
# y = df_updated[target_cols]

# # Dividir en entrenamiento (80%) y prueba (20%)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Entrenar el modelo XGBoost para todas las variables objetivo
# xgb_model = {}
# for target in target_cols:
#     model = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
#     model.fit(X_train, y_train[target])
#     xgb_model[target] = model
#     print(f"Modelo XGBoost para {target} entrenado.")

# # Evaluar el modelo en el conjunto de prueba y generar gráficos
# for target in target_cols:
#     y_pred = xgb_model[target].predict(X_test)
#     rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))
#     mae = mean_absolute_error(y_test[target], y_pred)
#     r2 = r2_score(y_test[target], y_pred)

#     # Validación cruzada manual con KFold (5 folds), se hace manual por compatibilidad entre  scikit-learn y xgboost
#     cv = KFold(n_splits=5, shuffle=True, random_state=42)
#     rmse_scores = []
#     r2_scores = []
#     for train_idx, val_idx in cv.split(X):
#         X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
#         y_train_cv, y_val_cv = y[target].iloc[train_idx], y[target].iloc[val_idx]
#         model_cv = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
#         model_cv.fit(X_train_cv, y_train_cv)
#         y_pred_cv = model_cv.predict(X_val_cv)
#         rmse_scores.append(np.sqrt(mean_squared_error(y_val_cv, y_pred_cv)))
#         r2_scores.append(r2_score(y_val_cv, y_pred_cv))
    
#     rmse_cv = np.mean(rmse_scores)
#     r2_cv = np.mean(r2_scores)
    
#     print(f"\nMétricas para {target} con XGBoost:")
#     print(f"RMSE: {rmse:.4f}")
#     print(f"MAE: {mae:.4f}")
#     print(f"RMSE promedio (CV): {rmse_cv:.4f}")
#     print(f"Coeficiente de Determinación (R²) en prueba: {r2:.4f}")
#     print(f"Coeficiente de Determinación promedio (CV, R²): {r2_cv:.4f}")

#     # Gráfico de valores reales vs predichos
#     plt.figure(figsize=(7, 5))
#     plt.scatter(y_test[target], y_pred, color="royalblue", alpha=0.7, label="Valores Predichos")
#     plt.plot([min(y_test[target]), max(y_test[target])], [min(y_test[target]), max(y_test[target])], 
#             color="red", linestyle="dashed", linewidth=2, label="Referencia: Predicción Exacta")
#     plt.xlabel(f"Valores Reales ({target})")
#     plt.ylabel(f"Valores Predichos ({target})")
#     plt.title(f"Comparación: Valores Reales vs Predichos ({target}) - XGBoost")
#     plt.legend()
#     plt.grid(True, linestyle="--", alpha=0.6)
#     plt.show()

#     # Gráfico de un árbol de decisión (primer árbol del modelo)
#     plt.figure(figsize=(15, 10))
#     plot_tree(xgb_model[target], num_trees=0, rankdir='LR')  # num_trees=0 para el primer árbol
#     plt.title(f"Árbol de Decisión (Primer Árbol) para {target} - XGBoost")
#     plt.show()

# # Guardar los modelos entrenados en un solo archivo .joblib
# joblib.dump(xgb_model, "models/xgb_model.joblib")

# # Guardar los modelos individuales en archivos separados (como en Regresión Lineal)
# for target in target_cols:
#     joblib.dump(xgb_model[target], f"models/xgb_model_{target}.joblib")

# print("\nModelo XGBoost guardado exitosamente en models/xgb_model.joblib y modelos individuales.")



# from xgboost import XGBRegressor
# model = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
# model.fit(X_train, y_train[target])

# ESTE SCRIPT ENTRENA EL MODELO XGBOOST CON GRID SEARCH

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor, plot_tree
import joblib
import matplotlib.pyplot as plt

# Cargar el dataset
df_updated = pd.read_csv("data/dataset_limpio_transformado_estandarizado_sin_constantes.csv")

# Separar variables independientes (X) y dependientes (y)
target_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log']
X = df_updated.drop(columns=target_cols)
y = df_updated[target_cols]

# Dividir en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir los hiperparámetros para Grid Search
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.7, 0.8, 1.0],
    'colsample_bytree': [0.7, 0.8, 1.0]
}

# Entrenar el modelo XGBoost para todas las variables objetivo con Grid Search
xgb_model = {}
for target in target_cols:
    print(f"\nEntrenando modelo XGBoost para {target} con Grid Search...")
    
    # Definir el modelo base
    model = XGBRegressor(random_state=42)
    
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
    xgb_model[target] = best_model
    
    # Imprimir los mejores hiperparámetros
    print(f"Mejores hiperparámetros para {target}: {grid_search.best_params_}")
    print(f"Mejor RMSE (CV): {np.sqrt(-grid_search.best_score_):.4f}")
    
    # Evaluar el mejor modelo en el conjunto de prueba
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test[target], y_pred))
    mae = mean_absolute_error(y_test[target], y_pred)
    r2 = r2_score(y_test[target], y_pred)

    # Validación cruzada manual con KFold (5 folds) para confirmar
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    rmse_scores = []
    r2_scores = []
    for train_idx, val_idx in cv.split(X):
        X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
        y_train_cv, y_val_cv = y[target].iloc[train_idx], y[target].iloc[val_idx]
        model_cv = XGBRegressor(**grid_search.best_params_, random_state=42)
        model_cv.fit(X_train_cv, y_train_cv)
        y_pred_cv = model_cv.predict(X_val_cv)
        rmse_scores.append(np.sqrt(mean_squared_error(y_val_cv, y_pred_cv)))
        r2_scores.append(r2_score(y_val_cv, y_pred_cv))
    
    rmse_cv = np.mean(rmse_scores)
    r2_cv = np.mean(r2_scores)
    
    print(f"\nMétricas para {target} con XGBoost (mejor modelo):")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE promedio (CV): {rmse_cv:.4f}")
    print(f"Coeficiente de Determinación (R²) en prueba: {r2:.4f}")
    print(f"Coeficiente de Determinación promedio (CV, R²): {r2_cv:.4f}")

    # Gráfico de valores reales vs predichos
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test[target], y_pred, color="royalblue", alpha=0.7, label="Valores Predichos")
    plt.plot([min(y_test[target]), max(y_test[target])], [min(y_test[target]), max(y_test[target])], 
            color="red", linestyle="dashed", linewidth=2, label="Referencia: Predicción Exacta")
    plt.xlabel(f"Valores Reales ({target})")
    plt.ylabel(f"Valores Predichos ({target})")
    plt.title(f"Comparación: Valores Reales vs Predichos ({target}) - XGBoost")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

    # Gráfico de un árbol de decisión (primer árbol del modelo)
    plt.figure(figsize=(15, 10))
    plot_tree(best_model, num_trees=0, rankdir='LR')  # num_trees=0 para el primer árbol
    plt.title(f"Árbol de Decisión (Primer Árbol) para {target} - XGBoost")
    plt.show()

# Guardar los modelos entrenados en un solo archivo .joblib
joblib.dump(xgb_model, "models/xgb_model.joblib")

# Guardar los modelos individuales en archivos separados
for target in target_cols:
    joblib.dump(xgb_model[target], f"models/xgb_model_{target}.joblib")

print("\nModelo XGBoost guardado exitosamente en models/xgb_model.joblib y modelos individuales.")
