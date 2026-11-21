import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8000/api/tipovehiculo/"
datos_invalidos = json.dumps({"nombre": "", "descripcion": ""}).encode("utf-8")

req = urllib.request.Request(
    URL,
    data=datos_invalidos,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
  with urllib.request.urlopen(req, timeout=10) as resp:
    print(f"ALERTA: El servidor acepto datos vacios con codigo {resp.status}")
except urllib.error.HTTPError as e:
  cuerpo_error = e.read().decode("utf-8", errors="replace")
  print(f"Codigo de respuesta ante entrada invalida: {e.code}")
  print(f"Detalle de validacion devuelto por la API: {cuerpo_error}")
  assert e.code == 400, f"Se esperaba 400 Bad Request y llego {e.code}"
  print("PRUEBA DE SEGURIDAD / VALIDACION EXITOSA")