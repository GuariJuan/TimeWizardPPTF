
#ESTE SCRIPT ANALIZA EL DATASET FORMATEADO (COMAS EN VEZ DE PUNTOS)

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ruta del archivo
file_path = "data/dataset_corregido.csv"

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
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Matriz de Correlación")
    plt.show()

    # 5. Análisis de outliers
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df.select_dtypes(include=['float64', 'int64']))
    plt.title("Análisis de Outliers (Boxplot)")
    plt.xticks(rotation=45)
    plt.show()

    # 6. Análisis de multicolinealidad con VIF
    def calculate_vif(df, features):
        vif_data = pd.DataFrame()
        vif_data["Variable"] = features
        vif_data["VIF"] = [
            variance_inflation_factor(df[features].values, i) for i in range(len(features))
        ]
        return vif_data

    # Variables independientes
    independent_vars = ['type', 's_frontend', 's_backend', 'lf_react', 'lf_angular', 
                        'lf_javascript', 'lf_kotlin', 'lb_node', 'lb_dotnet', 'lb_java', 'Complexity_value']
    
    vif = calculate_vif(df, independent_vars)
    print("\nVariance Inflation Factor (VIF):")
    print(vif)

    # 7. Relación entre variables independientes y dependientes
    dependent_vars = ['t_design', 't_frontend', 't_backend', 't_qa']
    
    for dep_var in dependent_vars:
        for ind_var in independent_vars:
            sns.scatterplot(x=df[ind_var], y=df[dep_var])
            plt.title(f'Relación entre {ind_var} y {dep_var}')
            plt.xlabel(ind_var)
            plt.ylabel(dep_var)
            plt.show()

    # 8. Normalidad de las variables dependientes
    for dep_var in dependent_vars:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[dep_var], kde=True, bins=20)
        plt.title(f"Distribución de {dep_var}")
        plt.xlabel(dep_var)
        plt.show()

    # 9. Distribución de frecuencias para columnas clave
    columns_to_plot = dependent_vars + independent_vars

    # Histogramas de distribución
    plt.figure(figsize=(12, 8))
    for i, col in enumerate(columns_to_plot, 1):
        plt.subplot(4, 4, i)
        sns.histplot(df[col], bins=20, kde=False, color='blue')
        plt.title(f'Distribución de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()

    # Gráficos de densidad (KDE)
    plt.figure(figsize=(12, 8))
    for col in columns_to_plot:
        sns.kdeplot(df[col], fill=True, label=col)

    plt.title("Distribución de Densidad")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.show()

else:
    print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")



# # ANALISIS DE OUTLIERS (BOXPLOT SEPARADO)

# import os
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Ruta del archivo
# file_path = "data/dataset_corregido.csv"

# # Verificar si el archivo existe antes de cargarlo
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito")

#     # Variables dependientes e independientes
#     dependent_vars = ['t_design', 't_frontend', 't_backend', 't_qa']
#     independent_vars = ['type', 's_frontend', 's_backend', 'lf_react', 'lf_angular',
#                         'lf_javascript', 'lf_kotlin', 'lb_node', 'lb_dotnet', 'lb_java', 'Complexity_value']

#     # --- BOXPLOT 1: Variables dependientes ---
#     plt.figure(figsize=(8, 6))
#     sns.boxplot(data=df[dependent_vars])
#     plt.title("Análisis de Outliers - Variables Dependientes")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

#     # --- BOXPLOT 2: Variables independientes ---
#     plt.figure(figsize=(12, 6))
#     sns.boxplot(data=df[independent_vars])
#     plt.title("Análisis de Outliers - Variables Independientes")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")




# # ANALISIS DE OUTLIERS (BOXPLOT SOLO VARIABLES DEPENDIENTES + COMPLEXITY_VALUE)

# import os
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Ruta del archivo
# file_path = "data/dataset_11_formatted.csv"
# # file_path = "data/dataset_corregido.csv" #para dataset estandarizado y aplicado logaritmo

# # Verificar si el archivo existe antes de cargarlo
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito")

#     # Variables a mostrar en el gráfico
#     selected_vars = ['t_design', 't_frontend', 't_backend', 't_qa', 'Complexity_value']

#     # Verificar que todas las columnas existan en el dataset
#     missing_cols = [col for col in selected_vars if col not in df.columns]
#     if missing_cols:
#         print(f"Advertencia: No se encontraron las columnas: {missing_cols}")
#     else:
#         # --- BOXPLOT combinado ---
#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=df[selected_vars])
#         plt.title("Análisis de Outliers - Variables dependientes + Complexity_value")
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")



# # ANALISIS DE DENSIDAD (KDE) - VARIABLES DEPENDIENTES + COMPLEXITY_VALUE

# import os
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Ruta del archivo
# file_path = "data/dataset_limpio_transformado_estandarizado.csv" # para dataset estandarizado y aplicado logaritmo
# # file_path = "data/dataset_corregido.csv" 

# # Verificar si el archivo existe antes de cargarlo
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito")

#     # Variables a mostrar en el gráfico
#     selected_vars = ['t_design_log', 't_frontend_log', 't_backend_log', 't_qa_log', 'Complexity_value_log']

#     # Verificar que todas las columnas existan en el dataset
#     missing_cols = [col for col in selected_vars if col not in df.columns]
#     if missing_cols:
#         print(f"Advertencia: No se encontraron las columnas: {missing_cols}")
#     else:
#         # --- Gráfico de densidad (KDE) combinado ---
#         plt.figure(figsize=(10, 6))
#         for col in selected_vars:
#             sns.kdeplot(df[col], fill=True, label=col, alpha=0.5)
        
#         plt.title("Distribución de Densidad - Variables dependientes + Complexity_value")
#         plt.xlabel("Valor")
#         plt.ylabel("Densidad")
#         plt.legend(title="Variables")
#         plt.tight_layout()
#         plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")



#     # ANALISIS DE DENSIDAD (KDE) - TODAS LAS VARIABLES NUMÉRICAS

# import os
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Ruta del archivo
# #file_path = "data/dataset_11_formatted.csv"
# file_path = "data/dataset_limpio_transformado_estandarizado.csv"

# # Verificar si el archivo existe antes de cargarlo
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito")

#     # Filtrar solo las columnas numéricas
#     numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

#     if not numeric_cols:
#         print("No se encontraron columnas numéricas en el dataset.")
#     else:
#         # --- Gráfico de densidad (KDE) combinado ---
#         plt.figure(figsize=(12, 7))
#         for col in numeric_cols:
#             sns.kdeplot(df[col], fill=True, label=col, alpha=0.5)

#         plt.title("Distribución de Densidad - Todas las variables numéricas")
#         plt.xlabel("Valor")
#         plt.ylabel("Densidad")
#         plt.legend(title="Variables", bbox_to_anchor=(1.05, 1), loc='upper left')
#         plt.tight_layout()
#         plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")




# # ANALISIS DE DENSIDAD (KDE) - ILUSTRACIÓN DE FALTA DE VARIANZA

# import os
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Ruta del archivo
# file_path = "data/dataset_limpio_transformado_estandarizado.csv"

# # Verificar si el archivo existe antes de cargarlo
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito")

#     # Filtrar solo las columnas numéricas
#     numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

#     if not numeric_cols:
#         print("No se encontraron columnas numéricas en el dataset.")
#     else:
#         # Calcular varianza de cada variable numérica
#         variances = df[numeric_cols].var().sort_values()

#         print("\nVarianza de cada variable (de menor a mayor):")
#         print(variances)

#         # Crear subplots según cantidad de variables
#         n_cols = 3
#         n_rows = int(len(numeric_cols) / n_cols) + 1
#         fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 3))
#         axes = axes.flatten()

#         # Graficar cada variable con su KDE y mostrar varianza
#         for i, col in enumerate(variances.index):
#             sns.kdeplot(df[col], fill=True, color='steelblue', alpha=0.6, ax=axes[i])
#             axes[i].set_title(f"{col}\nVarianza: {variances[col]:.6f}")
#             axes[i].set_xlabel("")
#             axes[i].set_ylabel("Densidad")

#         # Eliminar subplots vacíos
#         for j in range(i+1, len(axes)):
#             fig.delaxes(axes[j])

#         plt.suptitle("Distribución de Densidad (KDE) - Ilustración de falta de varianza", fontsize=14)
#         plt.tight_layout(rect=[0, 0, 1, 0.96])
#         plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe. Verifica la ruta y el nombre del archivo.")


# ANALISIS DE VARIANZA Y DISTRIBUCION - VARIABLES CON BAJA DISPERSION

# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Ruta del archivo
# file_path = "data/dataset_limpio_transformado_estandarizado.csv"

# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print("Archivo cargado con éxito\n")

#     # Variables a analizar
#     cols_to_check = ["type_log", "lf_kotlin_log"]

#     # 1️⃣ Estadísticas descriptivas
#     stats = df[cols_to_check].describe().T
#     stats["varianza"] = df[cols_to_check].var()
#     stats["% valor más frecuente"] = [
#         df[c].value_counts(normalize=True).iloc[0] * 100 for c in cols_to_check
#     ]
#     print("📊 Estadísticas descriptivas:\n")
#     print(stats[["mean", "std", "min", "max", "varianza", "% valor más frecuente"]])

#     # 2️⃣ Conteo de valores únicos
#     print("\n🔢 Frecuencias absolutas:\n")
#     for c in cols_to_check:
#         print(f"\n--- {c} ---")
#         print(df[c].value_counts().head())

#     # 3️⃣ Gráficos de distribución (KDE o histograma)
#     plt.figure(figsize=(10, 5))
#     for col in cols_to_check:
#         sns.kdeplot(df[col], fill=True, label=col, alpha=0.5)

#     plt.title("Distribución de variables con baja varianza")
#     plt.xlabel("Valor")
#     plt.ylabel("Densidad")
#     plt.legend()
#     plt.tight_layout()
#     plt.show()

# else:
#     print(f"Error: El archivo '{file_path}' no existe.")
