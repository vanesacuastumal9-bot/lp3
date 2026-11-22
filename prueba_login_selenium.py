from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
nombre_prueba = f"Moto QA {int(time.time())}"

try:
    # 1. Abrir la vista de Tipo de Vehiculo
    driver.get("http://127.0.0.1:8000/api/tipovehiculo/")
    time.sleep(2)

    # 2. Bajar hasta el formulario POST
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # 3. Llenar Nombre y Descripcion
    campo_nombre = wait.until(EC.presence_of_element_located((By.NAME, "nombre")))
    campo_nombre.clear()
    campo_nombre.send_keys(nombre_prueba)

    campo_desc = wait.until(EC.presence_of_element_located((By.NAME, "descripcion")))
    campo_desc.clear()
    campo_desc.send_keys("Registro automatizado desde Selenium para pruebas QA")

    # 4. Marcar Estado si no esta marcado
    checkbox_estado = driver.find_element(By.NAME, "estado")
    if not checkbox_estado.is_selected():
        checkbox_estado.click()
    time.sleep(1)

    # 5. Hacer clic en el boton POST
    boton_post = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()=\"POST\"]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_post)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", boton_post)
    time.sleep(3)

    # 6. Leer el resultado en pantalla y confirmar creacion
    cuerpo = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    texto_pagina = cuerpo.text

    if nombre_prueba in texto_pagina or "201 Created" in texto_pagina:
        print(f"PRUEBA EXITOSA: Se creo '{nombre_prueba}' mediante Selenium en /api/tipovehiculo/")
    else:
        print("Resultado obtenido:", texto_pagina[:200])

finally:
    driver.quit()