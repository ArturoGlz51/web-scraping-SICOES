import requests

def login_requests(email, password):
    url_login = "http://acceso.unisierra.edu.mx/sicoes/"
    session = requests.Session()
    payload = {
        "Email": email,
        "Password": password
    }
    response = session.post(url_login, data=payload)
    if "Listas y Calificaciones" in response.text:
        print("Inicio de sesión exitoso (requests).")
        return response.text
    else:
        print("Error al iniciar sesión con requests.")
        return None