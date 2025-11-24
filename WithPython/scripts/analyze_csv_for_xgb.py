import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math


# ✅ XGBoost, verifica:
# ✔️ Outliers extremos (pueden afectar el modelo)
# ✔️ Importancia de características
# ✔️ Distribución de la variable objetivo

# Ruta del archivo transformado
file_path = "data/dataset_limpio_transformado_estandarizado.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Archivo cargado con éxito")

    # Identificar columnas numéricas
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    # 1️⃣ Análisis de Outliers
    print("\n🔍 Análisis de outliers:")
    num_cols = len(numeric_cols)
    num_rows = math.ceil(num_cols / 3)  # Ajusta el número de filas dinámicamente

    plt.figure(figsize=(12, 4 * num_rows))
    for i, col in enumerate(numeric_cols, 1):
        plt.subplot(num_rows, 3, i)  # Ajusta el layout para evitar errores
        sns.boxplot(y=df[col], color='red')
        plt.title(f'Boxplot de {col}')
    plt.tight_layout()
    plt.show()

    # 2️⃣ Matriz de Correlación
    print("\n📊 Matriz de correlación:")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Matriz de Correlación de las Características")
    plt.show()

    # 3️⃣ Distribución de la Variable Objetivo
    objetivo_columna = 't_design_log'  # Ajusta según la variable que quieras analizar
    if objetivo_columna in df.columns:
        print(f"\n📈 Distribución de la variable objetivo ({objetivo_columna}):")
        sns.histplot(df[objetivo_columna], kde=True, bins=30)
        plt.title(f"Distribución de {objetivo_columna}")
        plt.show()
    else:
        print(f"⚠️ La columna '{objetivo_columna}' no se encuentra en el dataset.")

else:
    print(f"❌ Error: El archivo '{file_path}' no existe.")
