
#ESTE SCRIPT ELIMINA LAS VARIABLES type_log Y lf_kotlin_log PORQUE TIENEN UNA BAJA VARIANZA Y VIF INFINITO

import pandas as pd

# Cargar el dataset
file_path = "data/dataset_limpio_transformado_estandarizado.csv"
df = pd.read_csv(file_path)

# Verificar la distribución de type_log y lf_kotlin_log (opcional, para registro)
print("Distribución de type_log:")
print(df['type_log'].value_counts())
print("\nDistribución de lf_kotlin_log:")
print(df['lf_kotlin_log'].value_counts())

# Eliminar explícitamente type_log y lf_kotlin_log debido a su baja varianza y VIF infinito
columns_to_drop = ['type_log', 'lf_kotlin_log']
for column in columns_to_drop:
    if column in df.columns:
        print(f"\nEliminando {column} por baja varianza y VIF infinito.")
        df = df.drop(columns=[column])

# Guardar el dataset actualizado
cleaned_file_path = "data/dataset_limpio_transformado_estandarizado_sin_constantes.csv"
df.to_csv(cleaned_file_path, index=False)
print(f"\nDataset actualizado guardado en: {cleaned_file_path}")

# Verificar las columnas del dataset actualizado
df_updated = pd.read_csv("data/dataset_limpio_transformado_estandarizado_sin_constantes.csv")
print(df_updated.columns)