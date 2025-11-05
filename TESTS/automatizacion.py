import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def login_and_get_driver():
    """
    Realiza el proceso de login y devuelve el objeto driver.
    """
    # Define la ruta a tu chromedriver.exe
    chrome_driver_path = "C:\\Users\\Usuario1\\Documents\\LinkTic\\QA\\7- ANDINA\\chromedriver-win64\\chromedriver.exe"

    # Crea un objeto Service
    service = Service(executable_path=chrome_driver_path)

    # Importante: el driver ahora viene de selenium-wire
    driver = webdriver.Chrome(service=service)

    #Maximizamos el navegador
    driver.maximize_window()

    # Navega a la URL
    driver.get("https://andinavidasegurosqa.linktic.com")

    #zoom en 67%
    driver.execute_script("document.body.style.zoom='67%'")

    try:
        # 1. Login usando Selenium
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Inserte usuario']"))
        )
        password_field = driver.find_element(By.XPATH, "//input[@aria-label='Inserte clave']")

        username_field.send_keys("Kevin.Guerrero")
        password_field.send_keys("KevGue2025*")

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ingresar')]"))
        )
        login_button.click()

        # 2. Esperar a que el navegador envíe la petición de OTP y obtener su respuesta
        otp_url = "https://andinavidasegurosqabackend.linktic.com/identityserver/api/v1/otp/send-otp"
        driver.wait_for_request(otp_url, timeout=20)
        
        # 3. Encontrar la petición y extraer el código del cuerpo de la respuesta
        otp_code = None
        for request in driver.requests:
            if request.url == otp_url and request.response:
                try:
                    response_body = request.response.body
                    response_json = json.loads(response_body.decode('utf-8'))
                    otp_code = response_json.get('otp')
                    print(f"Token obtenido: {otp_code}")
                    # Limpia las peticiones para la siguiente corrida si es necesario
                    del driver.requests
                    break
                except Exception as e:
                    print(f"Error al procesar la respuesta: {e}")
        
        if not otp_code:
            raise Exception("No se pudo obtener el código OTP de la respuesta de red.")

        # 4. Esperar a que la ventana emergente aparezca completamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'otp-inputs-container')]//input"))
        )

        # 5. Encontrar los campos del token e ingresar el código
        otp_fields = driver.find_elements(By.XPATH, "//div[contains(@class, 'otp-inputs-container')]//input")
        for i in range(len(otp_code)):
            otp_fields[i].send_keys(otp_code[i])

        # 6. Esperar a que el botón 'Validar' sea clicable y hacer clic
        validate_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Validar')]"))
        )
        validate_button.click()

        # Espera adicional para que la página cargue completamente después del login
        time.sleep(5)

        # Devuelve el objeto driver para usarlo en otro archivo
        return driver

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        driver.quit()
        return None

if __name__ == "__main__":
    # Esta parte se ejecuta solo si corres el archivo directamente
    driver = login_and_get_driver()
    if driver:
        print("Login completado exitosamente.")
        # Aquí puedes agregar una pausa o más código de prueba
        time.sleep(10)
        driver.quit()