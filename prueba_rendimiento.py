import statistics
import time
import urllib.request

URL = "http://127.0.0.1:8000/api/tipovehiculo/"
TIEMPOS_MS = []
CODIGOS_HTTP = []

for i in range(10):
  inicio = time.perf_counter()
  with urllib.request.urlopen(URL, timeout=10) as respuesta:
    respuesta.read()
    CODIGOS_HTTP.append(respuesta.status)
  fin = time.perf_counter()
  TIEMPOS_MS.append((fin - inicio) * 1000)

promedio = statistics.mean(TIEMPOS_MS)
maximo = max(TIEMPOS_MS)
minimo = min(TIEMPOS_MS)

print(f"Peticiones exitosas: {len(CODIGOS_HTTP)}/10 | Codigos: {set(CODIGOS_HTTP)}")
print(
    f"Tiempo promedio: {promedio:.2f} ms | Min: {minimo:.2f} ms | Max:"
    f" {maximo:.2f} ms"
)
assert all(code == 200 for code in CODIGOS_HTTP)
assert promedio < 2000
print("PRUEBA DE RENDIMIENTO EXITOSA")