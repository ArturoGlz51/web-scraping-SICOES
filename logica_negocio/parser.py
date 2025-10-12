from bs4 import BeautifulSoup
import re

def extraer_calificaciones(html):
    soup = BeautifulSoup(html, "html.parser")

    # Buscar filas de calificaciones
    filas = soup.find_all("tr")
    datos = []

    for fila in filas:
        columnas = fila.find_all("td")
        if len(columnas) >= 3:
            materia = re.sub(r"[\r\n\t]+", "", columnas[0].text.strip())
            calificacion = re.findall(r"\d+", columnas[1].text)
            if calificacion:
                datos.append({
                    "materia": materia,
                    "calificacion": int(calificacion[0])
                })
    return datos