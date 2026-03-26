import pandas as pd

def guardar_excel(datos, ruta="calificaciones.xlsx"):
    # Lista para guardar los datos "aplanados"
    filas_planas = []
    
    # Recorremos cada alumno
    for estudiante in datos:
        nombre = estudiante.get("alumno", "Desconocido")
        matricula = estudiante.get("matricula", "Sin matrícula")
        
        # Recorremos cada calificación de ese alumno
        for calif in estudiante.get("calificaciones", []):
            # Creamos una fila individual por cada materia
            fila = {
                "Matrícula": matricula,
                "Alumno": nombre,
                "Semestre": calif.get("semestre", ""),
                "Materia": calif.get("materia", ""),
                "Calificación": calif.get("calificacion", "")
            }
            filas_planas.append(fila)
            
    # Si hay datos, creamos el Excel
    if filas_planas:
        df = pd.DataFrame(filas_planas)
        df.to_excel(ruta, index=False)
        print(f"Datos guardados correctamente en formato tabular en {ruta}")
    else:
        print("No hay datos detallados para guardar en Excel.")
