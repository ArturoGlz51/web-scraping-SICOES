import getpass
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logica_negocio.login_selenium import login_y_navegar_trayectoria
from logica_negocio.parser import extraer_calificaciones
from acceso_datos.guardar_json import guardar_json
from acceso_datos.guardar_excel import guardar_excel

def main():
    print("=== Extractor de Calificaciones SICOES ===")
    email = input("Correo: ")
    # getpass oculta la contraseña mientras la escribes en la consola
    password = getpass.getpass("Contraseña: ")

    # 1. Iniciar sesión y llegar a la página de tutorados
    driver = login_y_navegar_trayectoria(email, password)

    if not driver:
        print("No se pudo iniciar sesión o acceder a la trayectoria.")
        return

    todos_los_tutorados = []

    try:
        # 2. Identificar cuántos alumnos hay buscando los botones de Historial
        xpath_botones = "//button[@title='Historial académico' or contains(@formaction, 'Historial')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_botones)))
        botones = driver.find_elements(By.XPATH, xpath_botones)
        total_alumnos = len(botones)
        
        print(f"\nSe encontraron {total_alumnos} tutorados. Iniciando extracción...")

        # 3. Iterar sobre cada alumno
        for i in range(total_alumnos):
            # Debemos volver a buscar los botones en cada iteración porque al cambiar de página se pierde la referencia
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_botones)))
            botones = driver.find_elements(By.XPATH, xpath_botones)
            
            # Clic en el botón del alumno actual
            botones[i].click()
            
            # Esperar a que cargue el historial académico (buscamos la tabla o el título)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Historial')]|//table")))
            time.sleep(1) # Pequeña pausa para asegurar la carga del DOM
            
            # 4. Extraer el HTML de la página actual y enviarlo al parser
            html = driver.page_source
            datos_alumno = extraer_calificaciones(html)
            
            if datos_alumno:
                todos_los_tutorados.append(datos_alumno)
                print(f"  [+] Extraído: {datos_alumno['alumno']} ({len(datos_alumno['calificaciones'])} materias)")
            
            # 5. Regresar a la lista de tutorados
            driver.back()

    except Exception as e:
        print(f"Ocurrió un error procesando a los alumnos: {e}")

    # 6. Guardar la información usando tus módulos de acceso a datos
    if todos_los_tutorados:
        print("\nExtracción finalizada. Guardando archivos...")
        guardar_json(todos_los_tutorados)
        guardar_excel(todos_los_tutorados)
        print("¡Archivos guardados con éxito!")
    else:
        print("\nNo se encontraron calificaciones para guardar.")

    # Cerrar el navegador al terminar
    driver.quit()

if __name__ == "__main__":
    main()