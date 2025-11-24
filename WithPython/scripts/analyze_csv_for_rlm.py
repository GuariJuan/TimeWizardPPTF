import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ✅ Regresión Lineal Múltiple, verifica:
# ✔️ Linealidad
# ✔️ Multicolinealidad baja (VIF < 5)
# ✔️ Normalidad de residuos
# ✔️ Homocedasticidad

# Ruta del archivo transformado
file_path = "data/dataset_limpio_transformado_estandarizado.csv"

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Archivo cargado con éxito")

    # Definir las variables dependientes e independientes
    y_columns = ['t_design_log']
    X_columns = ['type_log', 's_frontend_log', 's_backend_log', 'lf_react_log', 'lf_angular_log', 
                'lf_javascript_log', 'lf_kotlin_log', 'lb_node_log', 'lb_dotnet_log', 'lb_java_log', 
                'Complexity_value_log']

    X = df[X_columns]
    
    # Verificación de Linealidad, Multicolinealidad, Normalidad de los residuos y Homocedasticidad para cada variable dependiente
    for y_column in y_columns:
        print(f"\n\nVerificando para la variable dependiente: {y_column}")
        
        # 1. Verificación de Linealidad: Gráfico de dispersión
        print("\nVerificación de Linealidad:")
        y = df[y_column]
        plt.figure(figsize=(12, 8))
        for i, col in enumerate(X.columns, 1):
            plt.subplot(1, len(X.columns), i)
            sns.scatterplot(x=X[col], y=y)
            plt.title(f'{col} vs {y_column}')
        plt.tight_layout()
        plt.show()

        # 2. Verificación de Multicolinealidad: Cálculo del VIF (Variance Inflation Factor)
        print("\nVerificación de Multicolinealidad (VIF):")
        X_sm = sm.add_constant(X)  # Añadir constante a las variables independientes
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X_sm.columns
        vif_data["VIF"] = [variance_inflation_factor(X_sm.values, i) for i in range(X_sm.shape[1])]
        print(vif_data)

        # 3. Comprobación de Normalidad de los Residuos
        print("\nComprobación de normalidad de los residuos:")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        residuals = y_train - model.predict(X_train)

        # Q-Q plot para los residuos
        stats.probplot(residuals, dist="norm", plot=plt)
        plt.title(f"Gráfico Q-Q de los residuos para {y_column}")
        plt.show()

        # 4. Verificación de Homocedasticidad: Gráfico de residuos vs valores ajustados
        print("\nVerificación de Homocedasticidad:")
        plt.figure(figsize=(8, 6))
        plt.scatter(model.predict(X_train), residuals)
        plt.axhline(0, color='red', linestyle='--')
        plt.title(f"Residuos vs Valores Ajustados para {y_column}")
        plt.xlabel("Valores Ajustados")
        plt.ylabel("Residuos")
        plt.show()

else:
    print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")
