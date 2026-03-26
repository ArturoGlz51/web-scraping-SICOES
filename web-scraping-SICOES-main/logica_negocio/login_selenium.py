from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_y_navegar_trayectoria(email, password):
    # Inicializar Chrome
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get("http://acceso.unisierra.edu.mx/sicoes/")
    driver.maximize_window()

    try:
        # --- 1. LOGIN ---
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Email"))
        )
        driver.find_element(By.NAME, "Email").send_keys(email)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Iniciando sesión...")

        # --- 2. DESPLEGAR MENÚ “Tutorías” ---
        tutorias_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Tutorías')]"))
        )
        ActionChains(driver).move_to_element(tutorias_menu).perform()
        tutorias_menu.click()

        # --- 3. CLIC EN “Trayectoria Escolar por Tutorado” ---
        trayectoria_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'TrayectoriaTutorado')]"))
        )
        trayectoria_link.click()
        print("Navegando a la lista de tutorados...")
        
        # Esperamos a que la página de trayectoria cargue confirmando que hay una tabla o título
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Tutorados')]|//table"))
        )

        # Retornamos el driver posicionado en la lista de alumnos
        return driver

    except Exception as e:
        print("Error durante el login o navegación:", e)
        driver.quit()
        return None