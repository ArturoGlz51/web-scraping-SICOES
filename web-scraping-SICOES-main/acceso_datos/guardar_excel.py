import pandas as pd

def guardar_excel(datos, ruta="calificaciones.xlsx"):
    df = pd.DataFrame(datos)
    df.to_excel(ruta, index=False)
    print(f"Datos guardados en {ruta}")