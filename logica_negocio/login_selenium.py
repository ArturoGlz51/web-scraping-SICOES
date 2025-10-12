from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_Selenium(email, password):
    # Inicializar Chrome
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get("http://acceso.unisierra.edu.mx/sicoes/")
    driver.maximize_window()

    try:
        # --- 1. LOGIN ---
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        driver.find_element(By.ID, "Email").send_keys(email)
        driver.find_element(By.ID, "Password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Intentando iniciar sesión...")

        # Esperar que cargue la barra de navegación
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Tutorías"))
        )
        print("Inicio de sesión exitoso.")

        # --- 2. DESPLEGAR MENÚ “Tutorías” ---
        tutorias_menu = driver.find_element(By.LINK_TEXT, "Tutorías")
        ActionChains(driver).move_to_element(tutorias_menu).perform()
        print("Menú 'Tutorías' desplegado.")

        # --- 3. CLIC EN “Trayectoria Escolar por Tutorado” ---
        trayectoria_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Trayectoria Escolar por Tutorado"))
        )
        trayectoria_link.click()
        print("Entrando a 'Trayectoria Escolar por Tutorado'...")
        time.sleep(3)

        # --- 4. CLIC EN BOTÓN “Historial académico” ---
        historial_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Historial académico']"))
        )
        historial_btn.click()
        print("Abriendo 'Historial académico'...")
        time.sleep(3)

        # --- 5. OBTENER HTML FINAL ---
        html = driver.page_source
        print("Página del historial académico obtenida correctamente.")

        return driver, html

    except Exception as e:
        print("Error durante la navegación:", e)
        return None, None

    finally:

        pass