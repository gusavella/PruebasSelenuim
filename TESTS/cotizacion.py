import time
import random
from datetime import date
import string
from dateutil.relativedelta import relativedelta
# Importamos la función de login desde el otro archivo
from automatizacion import login_and_get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta

# ==============================================================================
# <<<<<<< SECCIÓN DE FUNCIONES DE AYUDA (ACTUALIZADA) >>>>>>>
# ==============================================================================

def generar_fecha_nacimiento_aleatoria(edad_min=18, edad_max=80):
    """
    Genera una fecha de nacimiento aleatoria para una persona que tiene entre
    una edad mínima y máxima a día de hoy.
    """
    hoy = date.today()
    # La fecha más tardía posible (para cumplir 18 años justo hoy)
    fecha_limite_superior = hoy - relativedelta(years=edad_min)
    # La fecha más temprana que aceptamos (para tener 80 años)
    fecha_limite_inferior = hoy - relativedelta(years=edad_max)
    
    # Calculamos el total de días en ese rango
    total_dias_rango = (fecha_limite_superior - fecha_limite_inferior).days
    
    # Elegimos un número aleatorio de días para sumar a la fecha más temprana
    dias_aleatorios = random.randint(0, total_dias_rango)
    
    fecha_nacimiento_aleatoria = fecha_limite_inferior + timedelta(days=dias_aleatorios)
    return fecha_nacimiento_aleatoria

def asignar_fecha_causacion_aleatoria(fecha_nacimiento_str):
    """
    Valida si una persona es mayor de 18 años y devuelve una FECHA ALEATORIA válida.
    """
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y/%m/%d').date()
        fecha_actual = date.today()
        fecha_mayoria_edad = fecha_nacimiento + relativedelta(years=18)

        if fecha_actual >= fecha_mayoria_edad:
            delta_dias = (fecha_actual - fecha_mayoria_edad).days
            dias_aleatorios = random.randint(0, delta_dias)
            fecha_causacion_aleatoria = fecha_mayoria_edad + timedelta(days=dias_aleatorios)
            return fecha_causacion_aleatoria
        else:
            return None # Esto no debería pasar con la nueva lógica, pero es una buena práctica.
    except ValueError:
        return None
    
def generar_datos_personales(sexo):
    nombres_masculinos = ["Juan", "Carlos", "Luis", "Javier", "David", "Miguel", "José", "Daniel", "Alejandro", "Fernando", "Sergio", "Andrés", "Santiago", "Mateo"]
    nombres_femeninos = ["María", "Ana", "Laura", "Sofía", "Carmen", "Isabel", "Marta", "Lucía", "Elena", "Paula", "Valentina", "Camila", "Daniela", "Gabriela"]
    apellidos = ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Jiménez", "Ruiz", "Díaz", "Moreno", "Muñoz"]
    nombre_elegido = ""
    if sexo == 'MASCULINO': nombre_elegido = random.choice(nombres_masculinos)
    elif sexo == 'FEMENINO': nombre_elegido = random.choice(nombres_femeninos)
    else: nombre_elegido = random.choice(nombres_masculinos + nombres_femeninos)
    apellido_elegido = random.choice(apellidos)
    print(f"Datos personales generados: {nombre_elegido} {apellido_elegido} (Sexo: {sexo})")
    return {"nombre": nombre_elegido, "apellido": apellido_elegido}

    
def generar_numero_identificacion(tipo_documento):
    print(f"Generando # de identificación para el tipo: '{tipo_documento}'")
    if tipo_documento == 'CÉDULA CIUDADANIA': return str(random.randint(100000000, 1200000000))
    elif tipo_documento == 'TARJETA IDENTIDAD': return str(random.randint(1000000000, 1300000000))
    elif tipo_documento == 'REGISTRO CIVIL': return str(random.randint(1000000000, 9999999999))
    elif tipo_documento == 'CÉDULA EXTRANJERÍA': return str(random.randint(100000, 9999999))
    elif tipo_documento == 'NIT': return str(random.randint(100000000, 999999999))
    elif tipo_documento == 'PASAPORTE':
        letras = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        numeros = str(random.randint(100000, 999999))
        return letras + numeros
    elif tipo_documento in ['PERMISO PERMANENCIA', 'PERMISO TEMPORAL']: return str(random.randint(1000000, 9999999))
    else:
        print(f"ADVERTENCIA: Tipo de documento '{tipo_documento}' no reconocido. Se generará un ID genérico.")
        return str(random.randint(10000000, 99999999))

def seleccionar_opcion_aleatoria(driver, dropdown_locator, options_locator):
    # ... (código sin cambios)
    try:
        print("Abriendo el dropdown...")
        dropdown_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(dropdown_locator))
        driver.execute_script("arguments[0].click();", dropdown_element)
        print("Esperando que las opciones se carguen...")
        elementos_presentes = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(options_locator))
        opciones_disponibles = [opt for opt in elementos_presentes if opt.is_displayed()]
        if not opciones_disponibles:
            print("ERROR: No se encontraron opciones VISIBLES en el dropdown.")
            return None
        opcion_elegida = random.choice(opciones_disponibles)
        texto_opcion = opcion_elegida.get_attribute("textContent").strip()
        print(f"Opciones visibles encontradas: {len(opciones_disponibles)}. Opción elegida aleatoriamente: '{texto_opcion}'")
        elemento_a_desaparecer = opcion_elegida
        driver.execute_script("arguments[0].click();", opcion_elegida)
        WebDriverWait(driver, 5).until(EC.staleness_of(elemento_a_desaparecer))
        print(f"Opción aleatoria '{texto_opcion}' seleccionada y dropdown cerrado.")
        return texto_opcion
    except Exception as e:
        print(f"ERROR al seleccionar opción aleatoria: {e}")
        return None

def navegar_y_seleccionar_fecha(driver, fecha_objetivo):
    """
    Función reutilizable que abre y navega un calendario para seleccionar una fecha específica.
    """
    print(f"Navegando en calendario para seleccionar la fecha: {fecha_objetivo.strftime('%d/%m/%Y')}...")
    
    meses_a_numero = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    year_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[2]")
    month_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[1]")
    prev_year_btn_locator = (By.XPATH, "//button[@aria-label='Año anterior']")
    next_year_btn_locator = (By.XPATH, "//button[@aria-label='Año siguiente']")
    prev_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes anterior']")
    next_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes siguiente']")
    
    while True:
        year_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(year_locator))
        month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(month_locator))
        current_year = int(year_element.text)
        current_month = meses_a_numero[month_element.text.lower()]
        
        if current_year == fecha_objetivo.year and current_month == fecha_objetivo.month:
            print(f"Mes y año correctos encontrados: {month_element.text} de {current_year}")
            break

        btn_locator_to_click, element_to_wait_for = (None, None)
        if current_year > fecha_objetivo.year:
            btn_locator_to_click, element_to_wait_for = prev_year_btn_locator, year_element
        elif current_year < fecha_objetivo.year:
            btn_locator_to_click, element_to_wait_for = next_year_btn_locator, year_element
        elif current_month > fecha_objetivo.month:
            btn_locator_to_click, element_to_wait_for = prev_month_btn_locator, month_element
        elif current_month < fecha_objetivo.month:
            btn_locator_to_click, element_to_wait_for = next_month_btn_locator, month_element
        
        if btn_locator_to_click and element_to_wait_for:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator_to_click)).click()
            WebDriverWait(driver, 10).until(EC.staleness_of(element_to_wait_for))
        else:
            print("Error de lógica, saliendo del bucle de navegación de fecha.")
            break
            
    print(f"Seleccionando el día {fecha_objetivo.day}...")
    day_locator = (By.XPATH, f"//div[contains(@class, 'q-date__calendar-days')]//button[.//span[text()='{fecha_objetivo.day}']]")
    day_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(day_locator))
    driver.execute_script("arguments[0].click();", day_element)
    print(f"Fecha completa seleccionada: {fecha_objetivo.strftime('%d de %B de %Y')}")

# ==============================================================================
# <<<<<<< INICIO DEL SCRIPT PRINCIPAL >>>>>>>
# ==============================================================================

driver = login_and_get_driver()

if driver:
    print("Login exitoso. Iniciando proceso de cotización...")
    try:
        # <<<<<<< NUEVO: LÓGICA DE PRE-CÁLCULO DE DATOS ALEATORIOS >>>>>>>
        # 1. Generamos la fecha de nacimiento aleatoria (siempre mayor de 18).
        fecha_nacimiento_objetivo = generar_fecha_nacimiento_aleatoria()
        fecha_nacimiento_str_para_validar = fecha_nacimiento_objetivo.strftime('%Y/%m/%d')
        print(f"--- PRE-CÁLCULO: Fecha de Nacimiento Aleatoria Generada: {fecha_nacimiento_objetivo.strftime('%d/%m/%Y')}")

        # 2. Con la fecha de nacimiento, generamos la fecha de causación aleatoria.
        fecha_causacion_aleatoria = asignar_fecha_causacion_aleatoria(fecha_nacimiento_str_para_validar)
        print(f"--- PRE-CÁLCULO: Fecha de Causación Aleatoria Generada: {fecha_causacion_aleatoria.strftime('%d/%m/%Y')}")

        # 3. Verificamos la condición de las mesadas.
        fecha_limite_mesadas = date(2011, 7, 31)
        mesadas_a_ingresar = "13" # Valor por defecto
        if fecha_causacion_aleatoria and fecha_causacion_aleatoria < fecha_limite_mesadas:
            mesadas_a_ingresar = "14"
            print(f"--- PRE-CÁLCULO: La fecha de causación es anterior a {fecha_limite_mesadas.strftime('%d/%m/%Y')}. Se asignarán 14 mesadas.")
        else:
            print(f"--- PRE-CÁLCULO: La fecha de causación NO es anterior a {fecha_limite_mesadas.strftime('%d/%m/%Y')}. Se asignarán 13 mesadas.")
        # <<<<<<< FIN DE LA LÓGICA DE PRE-CÁLCULO >>>>>>>


        #Paso 1: Navegación inicial
        suscripcion_cotizacion_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Suscripción y cotización')]"))
        )
        suscripcion_cotizacion_btn.click()
        print("Botón 'Suscripción y Cotización' ha dado clic")

        crear_cotización_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Crear Cotización')]"))
        )
        crear_cotización_link.click()
        print("Botón 'Crear Cotización'ha dado clic")


        # --- INICIO FORMULARIO PARTE 1 ---
        print("Esperando a que el formulario se cargue...")
        clic_entidad_solicitante = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Entidad solicitante')]/following-sibling::label"))
        )
        print("Formulario cargado.")
        driver.execute_script("document.body.style.zoom='67%'")
        print("Zoom re-aplicado a 67%.")

        clic_entidad_solicitante.click()
        colfondos_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='COLFONDOS']"))).click()
        print("Opción 'COLFONDOS' seleccionada.")

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Tipo solicitud de cotización *')]/following-sibling::label"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='COTIZACION CAMBIO MODALIDAD']"))).click()
        print("Opción 'COTIZACION CAMBIO MODALIDAD' seleccionada.")
        
        fecha_fin_vigencia = date.today() + relativedelta(years=2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fecha fin vigencia cotización *')]/following-sibling::label"))).click()
        navegar_y_seleccionar_fecha(driver, fecha_fin_vigencia)
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Observaciones']/following-sibling::label//textarea"))).send_keys("MENSAJE DE PRUEBA KRGG")
        print("Mensaje agregado en el campo de observaciones")

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Estado de documentación')]/following-sibling::label"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='EN REVISIÓN']"))).click()
        print("Opción 'EN REVISIÓN' seleccionada.")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Origen pensión *')]/following-sibling::label"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='INVALIDEZ']"))).click()
        print("Se seleccionó el valor INVALIDEZ")
        
        vr_capital_input = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Vr. capital *']/following-sibling::label//input")))
        vr_capital_input.clear()
        vr_capital_input.send_keys("130000000")
        print("Valor agregado en 'Vr. capital *'")

        vr_pension_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Vr. pensión *']/following-sibling::label//input")))
        vr_pension_input.clear()
        vr_pension_input.send_keys("1623500")
        print("Valor agregado en 'Vr. pensión *'")

        # <<<<<<< CAMBIO: Usamos la variable pre-calculada para las mesadas >>>>>>>
        mesadas_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='# mesadas *']/following-sibling::label//input")))
        mesadas_input.clear()
        mesadas_input.send_keys(mesadas_a_ingresar)
        print(f"Valor agregado en '# mesadas *': {mesadas_a_ingresar}")
        
        continuar_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continuar']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continuar_btn)
        time.sleep(0.5)
        continuar_btn.click()
        print("Botón 'Continuar' ha sido presionado.")

        #------------------------------------SEGUNDA SECCIÓN------------------------------------
        tipo_documento_locator = (By.XPATH, "//span[text()='Tipo identificación *']/following-sibling::label")
        print("Esperando a que cargue la segunda parte del formulario...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(tipo_documento_locator))
        print("Segunda parte del formulario cargada.")

        tipo_documento_element = driver.find_element(*tipo_documento_locator)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tipo_documento_element)
        time.sleep(0.5)
        tipo_documento_element.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='CÉDULA CIUDADANIA']"))).click()
        print("Se ha seleccionado CEDULA DE CIUDADANÍA")

        numero_id_input = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='# identificación *']/following-sibling::label//input")))
        numero_id_input.clear()
        numero_id_input.send_keys("123456789")
        print("Número de identificación ingresado.")

        fecha_exp_objetivo = date(2014, 11, 14)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Fecha expedición documento']/following-sibling::label"))).click()
        navegar_y_seleccionar_fecha(driver, fecha_exp_objetivo)

        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Primer nombre *']/following-sibling::label//input"))).send_keys("KEVIN")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located ((By.XPATH, "//span[text()='Segundo nombre']/following-sibling::label//input"))).send_keys("REINALDO")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located ((By.XPATH, "//span[text()='Primer apellido *']/following-sibling::label//input"))).send_keys("Guerrero")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located ((By.XPATH, "//span[text()='Segundo apellido']/following-sibling::label//input"))).send_keys("Garcia")
        print("Nombres y apellidos registrados.")

        # <<<<<<< CAMBIO: Usamos la fecha de nacimiento aleatoria pre-calculada >>>>>>>
        fecha_nacimiento_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Fecha de nacimiento *']/following-sibling::label")))
        fecha_nacimiento_input.click()
        navegar_y_seleccionar_fecha(driver, fecha_nacimiento_objetivo)
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sexo *']/following-sibling::label"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='MASCULINO']"))).click()
        print("Sexo 'MASCULINO' seleccionado.")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Estado civil *']/following-sibling::label"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and .//span[text()='SOLTERO(A)']]"))).click()
        print("Estado civil 'SOLTERO(A)' seleccionado.")
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Estado del causante *']/following-sibling::label"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and .//span[text()='INVALIDO']]"))).click()
        print("Estado del causante 'INVALIDO' seleccionado.")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='EPS']/following-sibling::label"))).click()
        opcion_compensar_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='option' and .//span[text()='COMPENSAR']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion_compensar_element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", opcion_compensar_element)
        print("Opción 'COMPENSAR' seleccionada.")
            
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Residente en el exterior']/following-sibling::label"))).click()
        lista_de_opciones = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option' and .//span[text()='SI' or text()='NO']]")))
        opcion_elegida = random.choice(lista_de_opciones)
        texto_opcion_elegida = opcion_elegida.find_element(By.XPATH, ".//span").text
        print(f"La opción de residencia elegida aleatoriamente es: '{texto_opcion_elegida}'")
        driver.execute_script("arguments[0].click();", opcion_elegida)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='% DE PCL CON LA QUE SE RECONOCIÓ DERECHO *']/following-sibling::label//input"))).send_keys("55.5")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located ((By.XPATH, "//span[text()='% DE PCL ACTUAL']/following-sibling::label//input"))).send_keys("10")
        print("Datos de PCL ingresados.")

        # <<<<<<< CAMBIO: Usamos la fecha de causación aleatoria pre-calculada >>>>>>>
        if fecha_causacion_aleatoria:
            try:
                campo_fecha_causacion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fecha de causación del derecho *')]/following-sibling::label")))
                campo_fecha_causacion.click()
                navegar_y_seleccionar_fecha(driver, fecha_causacion_aleatoria)
            except Exception as e:
                print(f"ERROR: No se pudo asignar la 'Fecha de causación'. Detalle: {e}")
        else:
            print("ERROR CRÍTICO: No se pudo generar una fecha de causación válida.")

        continuar_btn_form2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continuar']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continuar_btn_form2)
        time.sleep(0.5)
        continuar_btn_form2.click()
        print("Botón 'Continuar' del formulario 2 ha sido presionado.")
        #---------------HASTA ACÁ LLEGA EL FORMULARIO #2 ----------------------------


        #-----------FORMULARIO #3 (DATOS DEL BENEFICIARIO)-----------
        
        print("\nEsperando a que el Formulario 3 (Detalles de pensión) cargue...")
        locator_dropdown_tipo_id_pension = (By.XPATH, "//span[text()='Tipo de identificación *']/following-sibling::label")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_dropdown_tipo_id_pension))
        print("Formulario 3 cargado con éxito.")
        
        try:
            print("\n--- Rellenando detalles de pensión (Beneficiario) ---")
            
            print("Seleccionando el tipo de identificación...")
            locator_opciones_tipo_id_pension = (By.XPATH, "//div[@role='option']")
            
            tipo_id_seleccionado = seleccionar_opcion_aleatoria(driver, locator_dropdown_tipo_id_pension, locator_opciones_tipo_id_pension)

            if not tipo_id_seleccionado:
                raise Exception("No se pudo seleccionar un tipo de identificación.")

            print(f"Tipo de identificación seleccionado: '{tipo_id_seleccionado}'.")
            
            numero_id_generado = generar_numero_identificacion(tipo_id_seleccionado)
            
            locator_input_id = (By.XPATH, "//span[text()='# identificación *']/following-sibling::label//input")
            campo_id = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_input_id))
            campo_id.clear()
            campo_id.send_keys(numero_id_generado)
            print(f"Número de identificación generado e ingresado: {numero_id_generado}")
            #---------------Seleccionar sexo de manera aleatoria --------------------
            print("Seleccionando el sexo del beneficiario...")
            locator_dropdown_sexo_form3 = (By.XPATH, "//span[text()='Sexo *']/following-sibling::label")
            locator_opciones_sexo_form3 = (By.XPATH, "//div[@role='option']")
            
            sexo_elegido_form3 = seleccionar_opcion_aleatoria(driver, locator_dropdown_sexo_form3, locator_opciones_sexo_form3)

            if not sexo_elegido_form3:
                raise Exception("No se pudo seleccionar un sexo en el Formulario 3.")

            print(f"Sexo del beneficiario seleccionado: '{sexo_elegido_form3}'. Generando datos...")
            datos_persona_form3 = generar_datos_personales(sexo_elegido_form3)

            # -------------------- Seleccionar el nombre dependiendo el sexo elegio -------------------
            locator_input_nombre = (By.XPATH, "//span[text()='Primer nombre *']/following-sibling::label//input")
            campo_nombre = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_input_nombre))
            campo_nombre.clear()
            campo_nombre.send_keys(datos_persona_form3["nombre"])

            locator_input_apellido = (By.XPATH, "//span[text()='Primer apellido *']/following-sibling::label//input")
            campo_apellido = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_input_apellido))
            campo_apellido.clear()
            campo_apellido.send_keys(datos_persona_form3["apellido"])
            
            print(f"Nombre y apellido del beneficiario generados e ingresados: {datos_persona_form3['nombre']} {datos_persona_form3['apellido']}")

            # ---- fecha nacimiento beneficiario -----
            print("Generando y seleccionando una fecha de nacimiento aleatoria para el beneficiario...")
            
            fecha_nacimiento_beneficiario = generar_fecha_nacimiento_aleatoria(edad_min=18, edad_max=65)

            locator_campo_fecha_nacimiento = (By.XPATH, "//span[text()='Fecha de nacimiento *']/following-sibling::label")
            campo_fecha_nacimiento = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_campo_fecha_nacimiento))
            campo_fecha_nacimiento.click()
            
            navegar_y_seleccionar_fecha(driver, fecha_nacimiento_beneficiario)

            # -----Parentesco -------
            print("Se va a generar el parentesco RANDOM")

            parentesco_beneficiario = ((By.XPATH, "//span[text()='Parentesco *']/following-sibling::label"))
            parentesco_beneficiario_select = ((By.XPATH, "//div[@role='option']"))

            parentesco_elegido = seleccionar_opcion_aleatoria (driver, parentesco_beneficiario, parentesco_beneficiario_select)

            if not parentesco_elegido:
                raise Exception("No se puede seleccionar un parentesco en el formulario 3")
            print(f"Parentesco seleccionado '{parentesco_elegido}' ")

            # ------------------ ESTADO DEL BENEFICIARIO ----------------------
            print("Seleccionando el estado del beneficiario...")
            estado_beneficiario = (By.XPATH, "//span[text()='Estado del beneficiario *']/following-sibling::label")
            estado_beneficiario_select = (By.XPATH, "//div[@role='option']")
            
            estado_beneficiario_elegido = seleccionar_opcion_aleatoria(driver,estado_beneficiario, estado_beneficiario_select)

            if not estado_beneficiario_select:
                raise Exception("No se pudo seleccionar un estado del beneficiario en el Formulario 3.")

            print(f"Sexo del beneficiario seleccionado: '{estado_beneficiario_select}'. Generando datos...")
            datos_persona_form3 = generar_datos_personales(estado_beneficiario_select)

            # ----------------TEMPORALIDAD -------------------
            print("Seleccionando la temporalidad del beneficiario")
            temporalidad_beneficiario = (By.XPATH, "//span[text()='Temporalidad *']/following-sibling::label")
            temporalidad_beneifciario_select = (By.XPATH, "//div[@role='option']")

            temporalidad_beneficiario_elegido = seleccionar_opcion_aleatoria(driver, temporalidad_beneficiario, temporalidad_beneifciario_select)

            if not temporalidad_beneifciario_select:
                raise Exception("No se pudo seleccionar una temporalidad en el formulario 3.")

            print(f"Temporalidad '{temporalidad_beneifciario_select}'")
            datos_persona_form3 = generar_datos_personales(estado_beneficiario_select)

        except Exception as e:
            print(f"ERROR al rellenar los detalles de la pensión: {e}")


            # -----Parentesco -------
            print("Se va a generar el parentesco RANDOM")

            parentesco_beneficiario = ((By.XPATH, "//span[text()='Parentesco *']/following-sibling::label"))
            parentesco_beneficiario_select = ((By.XPATH, "//div[@role='option']"))

            parentesco_elegido = seleccionar_opcion_aleatoria (driver, parentesco_beneficiario, parentesco_beneficiario_select)

            if not parentesco_elegido:
                raise Exception("No se puede seleccionar un parentesco en el formulario 3")
            print(f"Parentesco seleccionado '{parentesco_elegido}' ")

            # ------------------ ESTADO DEL BENEFICIARIO ----------------------
            print("Seleccionando el estado del beneficiario...")
            estado_beneficiario = (By.XPATH, "//span[text()='Estado del beneficiario *']/following-sibling::label")
            estado_beneficiario_select = (By.XPATH, "//div[@role='option']")
            
            estado_beneficiario_elegido = seleccionar_opcion_aleatoria(driver,estado_beneficiario, estado_beneficiario_select)

            if not estado_beneficiario_select:
                raise Exception("No se pudo seleccionar un estado del beneficiario en el Formulario 3.")

            print(f"Sexo del beneficiario seleccionado: '{estado_beneficiario_select}'. Generando datos...")
            datos_persona_form3 = generar_datos_personales(estado_beneficiario_select)

            # ----------------TEMPORALIDAD -------------------
            print("Seleccionando la temporalidad del beneficiario")
            temporalidad_beneficiario = (By.XPATH, "//span[text()='Temporalidad *']/following-sibling::label")
            temporalidad_beneifciario_select = (By.XPATH, "//div[@role='option']")

            temporalidad_beneficiario_elegido = seleccionar_opcion_aleatoria(driver, temporalidad_beneficiario, temporalidad_beneifciario_select)

            if not temporalidad_beneifciario_select:
                raise Exception("No se pudo seleccionar una temporalidad en el formulario 3.")

            print(f"Temporalidad '{temporalidad_beneifciario_select}'")
            datos_persona_form3 = generar_datos_personales(estado_beneficiario_select)


            #-------------GUARDAR -----------------
            guardar_btn_form3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Guardar']]")))
            
            time.sleep(0.5)
            guardar_btn_form3.click()
            print("Botón 'Guardar' del formulario 3 ha sido presionado. SE GUARDO SATISFACTORIAMENTE")
            

        # input("El script ha terminado. Presiona Enter en esta consola para cerrar el navegador...")
        print("Proceso de cotización finalizado.")

    except TimeoutException:
        print("Se agotó el tiempo de espera. El elemento no se encontró o no era clickeable.")
    except Exception as e:
        print(f"Ocurrió un error en el proceso de cotización: {e}")

    finally:
        driver.quit()
else:
    print("No se pudo completar el login. Saliendo del script.")