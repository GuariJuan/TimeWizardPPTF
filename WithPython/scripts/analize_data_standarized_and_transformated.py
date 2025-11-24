
#ESTE SCRIPT ANALIZA EL DATASET ESTANDARIZADO Y TRANSFORMADO 

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ruta del archivo transformado
file_path = "data/dataset_limpio_transformado_estandarizado.csv"

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Archivo cargado con éxito")
    
    # 1. Información general del dataset
    print("\nResumen del dataset:")
    print(df.info())
    print("\nPrimeras filas del dataset:")
    print(df.head())

    # 2. Estadísticas descriptivas
    print("\nEstadísticas descriptivas:")
    pd.set_option('display.max_columns', None)
    print(df.describe())
    print(df.dtypes)

    # 3. Verificar valores faltantes
    print("\nValores faltantes por columna:")
    print(df.isnull().sum())
    
    # Visualización de valores nulos
    plt.figure(figsize=(8, 5))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
    plt.title("Mapa de valores nulos")
    plt.show()
    
    # 4. Correlación entre variables
    print("\nMatriz de correlación (Pearson):")
    correlation_matrix = df.corr()
    print(correlation_matrix)

    # Visualizar matriz de correlación con un heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Matriz de Correlación")
    plt.show()

    # 4.1 Cálculo del VIF para detectar multicolinealidad (solo variables independientes)
    print("\nCálculo del VIF para todas las variables independientes (dataset original con 15 variables):")
    expected_independents = ['type_log', 's_frontend_log', 's_backend_log', 'lf_react_log', 'lf_angular_log', 
                            'lf_javascript_log', 'lf_kotlin_log', 'lb_node_log', 'lb_dotnet_log', 
                            'lb_java_log', 'Complexity_value_log']
    X = df[[col for col in df.columns if col in expected_independents]] 
    print("\nVariables independientes encontradas en el dataset:", X.columns.tolist())
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print(vif_data)
    print("\nNota: VIF > 10 puede indicar multicolinealidad significativa.")

    # 5. Análisis de distribución de las variables
    num_columns = len(df.columns)
    rows = (num_columns // 4) + (num_columns % 4 > 0) 
    
    plt.figure(figsize=(12, rows * 3))
    for i, col in enumerate(df.columns, 1):
        plt.subplot(rows, 4, i)
        sns.histplot(df[col], bins=20, kde=True, color='blue')
        plt.title(f'Distribución de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')
    
    plt.tight_layout()
    plt.show()
    
    # 6. Análisis de outliers con boxplots
    plt.figure(figsize=(12, rows * 3))
    for i, col in enumerate(df.columns, 1):
        plt.subplot(rows, 4, i)
        sns.boxplot(y=df[col], color='red')
        plt.title(f'Boxplot de {col}')
    
    plt.tight_layout()
    plt.show()
    
    # 7. Relación entre variables con pairplot
    print("\nGenerando dos pairplots con las variables más relevantes...")
    
    # Pairplot 1: Variables objetivo y algunas independientes clave (8 variables)
    objective_and_key_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log', 
                            'Complexity_value_log', 'lf_react_log', 'lf_javascript_log', 'lf_angular_log']
    plt.figure(figsize=(12, 10))  # Tamaño ajustado para 8 variables
    sns.pairplot(df[objective_and_key_cols], diag_kind='kde')
    plt.show()

    # Pairplot 2: Otras variables independientes y su relación con las variables objetivo
    other_cols = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log', 
                'type_log', 's_frontend_log', 's_backend_log', 'lf_kotlin_log', 
                'lb_node_log', 'lb_dotnet_log', 'lb_java_log']
    sns.pairplot(df[other_cols], diag_kind='kde')
    plt.show()
    
else:
    print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")