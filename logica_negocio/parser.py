from bs4 import BeautifulSoup
import re

def extraer_calificaciones(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Extraer nombre y matrícula si existen en los h3 con etiquetas <strong>
    try:
        alumno_tag = soup.find(lambda tag: tag.name == "h3" and "Alumno" in tag.text)
        alumno = alumno_tag.find("strong").text.strip() if alumno_tag else "Desconocido"
        
        matricula_tag = soup.find(lambda tag: tag.name == "h3" and "Matricula" in tag.text)
        matricula = matricula_tag.find("strong").text.strip() if matricula_tag else "Sin matrícula"
    except:
        alumno = "Desconocido"
        matricula = "Sin matrícula"

    calificaciones = []

    # Buscar todas las filas de la tabla de historial
    filas = soup.find_all("tr")

    for fila in filas:
        columnas = fila.find_all("td")
        # Asumiendo que la tabla tiene Semestre(0), Clave(1), Materia(2), Calificacion(3), etc.
        if len(columnas) >= 4:
            semestre = re.sub(r"[\r\n\t]+", "", columnas[0].text.strip())
            materia = re.sub(r"[\r\n\t]+", "", columnas[2].text.strip())
            calificacion_texto = re.sub(r"[\r\n\t]+", "", columnas[3].text.strip())
            
            # Buscar el número en la columna de calificación
            calificacion_num = re.findall(r"\d+", calificacion_texto)
            
            # Evitar encabezados o filas vacías
            if calificacion_num and materia and materia.lower() != "materia":
                calificaciones.append({
                    "semestre": semestre,
                    "materia": materia,
                    "calificacion": int(calificacion_num[0])
                })
                
    # Retornar un diccionario estructurado
    return {
        "alumno": alumno,
        "matricula": matricula,
        "calificaciones": calificaciones
    }
