import pandas as pd
import numpy as np

# Cargar el dataset original (antes de estandarizar)
df = pd.read_csv("data/dataset_11_formatted.csv") 

# Variables a transformar
columns = [
    "t_design", "t_frontend", "t_backend", "t_qa",
    "s_frontend", "s_backend",
    "lf_react", "lf_angular", "lf_javascript",
    "lb_node", "lb_dotnet", "lb_java",
    "Complexity_value"
]

# Aplicar transformación logarítmica
for col in columns:
    df[f"{col}_log"] = np.log1p(df[col])

# Calcular medias y desviaciones estándar
log_columns = [f"{col}_log" for col in columns]
means = df[log_columns].mean().to_dict()
stds = df[log_columns].std().to_dict()

# Imprimir los valores
print("Means:", means)
print("Stds:", stds)