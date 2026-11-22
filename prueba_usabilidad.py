from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

opciones = Options()
opciones.add_argument("--log-level=3")

driver = webdriver.Chrome(options=opciones)
wait = WebDriverWait(driver, 10)

try:
  driver.set_window_size(1280, 800)
  driver.get("http://127.0.0.1:8000/api/tipovehiculo/")

  campo_nombre = wait.until(
      EC.presence_of_element_located((By.NAME, "nombre"))
  )
  campo_desc = wait.until(
      EC.presence_of_element_located((By.NAME, "descripcion"))
  )
  checkbox_estado = wait.until(
      EC.presence_of_element_located((By.NAME, "estado"))
  )
  boton_post = wait.until(
      EC.presence_of_element_located(
          (By.XPATH, "//button[contains(normalize-space(.), 'POST')]")
      )
  )

  driver.execute_script(
      "arguments[0].scrollIntoView({block: 'center'});", campo_nombre
  )

  assert campo_nombre.is_enabled(), "Campo nombre no habilitado"
  assert campo_desc.is_enabled(), "Campo descripcion no habilitado"
  assert checkbox_estado.is_enabled(), "Checkbox estado no habilitado"
  assert boton_post.is_enabled(), "Boton POST no habilitado"

  print("Titulo de la pagina:", driver.title, flush=True)
  print(
      "Controles verificados: nombre, descripcion, estado y boton POST",
      flush=True,
  )
  print("PRUEBA DE USABILIDAD EXITOSA", flush=True)

finally:
  driver.quit()