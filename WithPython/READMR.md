proyecto/
│
├── data/                   # Carpeta para datasets
│   └── tu_dataset.csv      # Archivo CSV con tu dataset
│
├── models/                 # Carpeta para guardar modelos entrenados
│   ├── linear_model.pkl    # Archivo del modelo de regresión lineal
│   └── xgb_model.pkl       # Archivo del modelo XGBoost
│
├── scripts/                # Scripts Python para tareas específicas
│   ├── train_model.py      # Script para entrenar y guardar los modelos
│   └── analyze_data.py     # Opcional: análisis exploratorio de datos
│
├── app/                    # Carpeta para tu API con FastAPI
│   ├── main.py             # Archivo principal de FastAPI
│   └── requirements.txt    # Dependencias del proyecto
│
├── venv/                   # Entorno virtual (opcional)
│
└── README.md               # Instrucciones del proyecto


#PARA INICIAR:
C:\Users\Juan\Desktop\FACULTAD\Repos\TimeWizard\WithPython>
fastApi-env\Scripts\activate

pip install "fastapi[all]" uvicorn[standard] joblib pandas numpy scikit-learn matplotlib seaborn
uvicorn app.main:app --reload

uvicorn app.main:app --reload

http://127.0.0.1:8000/docs

#Para entrenar modelos
python scripts/xxxxxx.py
