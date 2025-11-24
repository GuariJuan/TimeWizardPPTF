
#ESTE SCRIPT TRANSFORMA Y ESTANDARIZA EL DATASET

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler
import numpy as np

# Ruta del archivo
file_path = "data/dataset_11_formatted.csv"

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Archivo cargado con éxito")
    
    # Columnas a transformar (ajusta según tu dataset)
    dependent_vars = ['t_design', 't_frontend', 't_backend', 't_qa']
    independent_vars = ['type', 's_frontend', 's_backend', 'lf_react', 'lf_angular', 
                        'lf_javascript', 'lf_kotlin', 'lb_node', 'lb_dotnet', 'lb_java', 'Complexity_value']
    columns_to_log_transform = dependent_vars + independent_vars

    # Aplicar transformación logarítmica
    transformed_columns = []
    for col in columns_to_log_transform:
        if df[col].min() > 0:  # Asegurarse de que todos los valores sean positivos
            df[col + '_log'] = np.log(df[col])
        else:
            print(f"\nAdvertencia: La columna '{col}' tiene valores <= 0. Usando log1p.")
            df[col + '_log'] = np.log1p(df[col])
        transformed_columns.append(col + '_log')
    
    # Estandarización de las columnas transformadas
    print("\nEstandarización de variables transformadas...")
    scaler = StandardScaler()
    df[transformed_columns] = scaler.fit_transform(df[transformed_columns])
    print("\nDataset después de la estandarización:")
    print(df[transformed_columns].describe())
    
    # Guardar solo las columnas transformadas y estandarizadas
    clean_file_path = "data/dataset_limpio_transformado_estandarizado.csv"
    df[transformed_columns].to_csv(clean_file_path, index=False)
    print(f"\nDataset limpio, transformado y estandarizado guardado en: {clean_file_path}")
else:
    print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")
