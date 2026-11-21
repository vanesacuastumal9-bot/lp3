from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
  driver.set_window_size(1280, 800)
  driver.get("http://127.0.0.1:8000/api/tipovehiculo/")

  campo_nombre = wait.until(
      EC.visibility_of_element_located((By.NAME, "nombre"))
  )
  campo_desc = wait.until(
      EC.visibility_of_element_located((By.NAME, "descripcion"))
  )
  checkbox_estado = wait.until(
      EC.presence_of_element_located((By.NAME, "estado"))
  )
  boton_post = wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "form button[type='submit']"))
  )

  assert (
      campo_nombre.is_displayed() and campo_nombre.is_enabled()
  ), "Campo nombre no disponible"
  assert (
      campo_desc.is_displayed() and campo_desc.is_enabled()
  ), "Campo descripcion no disponible"
  assert checkbox_estado.is_enabled(), "Checkbox estado no disponible"
  assert (
      boton_post.is_displayed() and boton_post.is_enabled()
  ), "Boton POST no disponible"

  print("Titulo de la pagina:", driver.title)
  print(
      "Campos visibles y habilitados: nombre, descripcion, estado y boton POST"
  )
  print("PRUEBA DE USABILIDAD EXITOSA")
finally:
  driver.quit()