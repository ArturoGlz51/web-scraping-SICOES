import json

def guardar_json(datos, ruta="calificaciones.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print(f"Datos guardados en {ruta}")