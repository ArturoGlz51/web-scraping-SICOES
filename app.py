from logica_negocio.login_request import login_requests
from logica_negocio.login_selenium import login_Selenium
from logica_negocio.parser import extraer_calificaciones
from acceso_datos.guardar_json import guardar_json
from acceso_datos.guardar_excel import guardar_excel

def main():
    metodo = input("¿Deseas usar 'requests' o 'selenium'? ")
    email = input("Correo: ")
    password = input("Contraseña: ")

    if metodo.lower() == "requests":
        html = login_requests(email, password)
    else:
        driver, html = login_Selenium(email, password)

    if not html:
        print("No se pudo iniciar sesión.")
        return

    calificaciones = extraer_calificaciones(html)

    if calificaciones:
        guardar_json(calificaciones)
        guardar_excel(calificaciones)
    else:
        print("No se encontraron calificaciones.")

    if metodo.lower() == "selenium":
        driver.quit()

if __name__ == "__main__":
    main()