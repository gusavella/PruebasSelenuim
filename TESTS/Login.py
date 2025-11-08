from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json
import os
import unittest

ruta_archivo = 'Config.json'
# Obtener la ruta del archivo JSON en la misma carpeta
ruta_json = os.path.join(os.path.dirname(__file__), ruta_archivo)

options = Options()
options.use_cromium = True

print("ruta:", ruta_json)

with open(ruta_json, 'r', encoding='utf-8') as archivo:
    configuracion = json.load(archivo)

class ExampleDetComTest (unittest.TestCase):
    def setUp(self):
        self.driver =webdriver.Edge(options=options)

    def test_page_tittle(self):
        driver= self.driver
        driver.get(configuracion['pre']['url'])
        self.assertEqual(driver.title,'Andina Core','Titulo no corresponde')

        # 1. Login usando Selenium
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Inserte usuario']"))
        )
        password_field = driver.find_element(By.XPATH, "//input[@aria-label='Inserte clave']")

        username_field.send_keys(configuracion['pre']['user'])
        password_field.send_keys(configuracion['pre']['password'])

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ingresar')]"))
        )
        login_button.click()

        # 2. Esperar a que el navegador envíe la petición de OTP y obtener su respuesta
        otp_url = configuracion['pre']['url_otp']
        payload = {
            'key': configuracion['pre']['key']
        }

        # Encabezados opcionales
        headers = {
            'Content-Type': 'application/json'
        }

        # Enviar la solicitud POST
        response = requests.post(otp_url, json=payload, headers=headers)

        # Verificar la respuesta
        if response.status_code == 200:
            print("Respuesta exitosa:", response.json())
        else:
            print(f"Error {response.status_code}: {response.text}")

        print("otp:",response.json()['otp'])
        otp_code = response.json()['otp']

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

if __name__ == "__main__":
    unittest.main()