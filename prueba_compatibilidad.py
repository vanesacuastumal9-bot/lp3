from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

opciones = Options()
opciones.add_argument("--log-level=3")

TAMANOS = [(1366, 768), (768, 900)]
driver = webdriver.Chrome(options=opciones)
wait = WebDriverWait(driver, 10)

try:
  for ancho, alto in TAMANOS:
    driver.set_window_size(ancho, alto)
    driver.get("http://127.0.0.1:8000/api/tipovehiculo/")

    cuerpo = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    campo_nombre = wait.until(
        EC.presence_of_element_located((By.NAME, "nombre"))
    )
    boton_post = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(normalize-space(.), 'POST')]")
        )
    )

    assert len(cuerpo.text.strip()) > 0, f"Sin contenido en {ancho}x{alto}"
    assert campo_nombre is not None and boton_post is not None
    print(
        f"Resolucion {ancho}x{alto}: vista y formulario cargados correctamente",
        flush=True,
    )

  print("PRUEBA DE COMPATIBILIDAD EXITOSA", flush=True)

finally:
  driver.quit()