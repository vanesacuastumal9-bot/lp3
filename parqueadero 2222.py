# Modulo Ingreso y Salida - Calculo de cobro RF-003
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime

# ================== ENDPOINTS ================== #
ENDPOINTS = {
    "Cliente": "http://127.0.0.1:8000/api/cliente/",
    "Vehículo": "http://127.0.0.1:8000/api/vehiculo/",
    "Tipo Vehículo": "http://127.0.0.1:8000/api/tipovehiculo/",
    "Tarifa": "http://127.0.0.1:8000/api/tarifa/",
    "Empleado": "http://127.0.0.1:8000/api/empleado/",
    "Usuario": "http://127.0.0.1:8000/api/usuario/",
    "Ingreso/Salida": "http://127.0.0.1:8000/api/ingresosalida/",
}

RELATIONS = {
    "tipo_vehiculo": ENDPOINTS["Tipo Vehículo"],
    "empleado": ENDPOINTS["Empleado"],
    "cliente": ENDPOINTS["Cliente"],
    "vehiculo": ENDPOINTS["Vehículo"],
    "tarifa": ENDPOINTS["Tarifa"],
}

# ================== COLORES ================== #
BG_MAIN = "#050505"
BG_PANEL = "#0d0d0d"
BG_INPUT = "#1a1a1a"
GREEN = "#00cc66"
GREEN_HOVER = "#00e676"
TEXT = "white"

# ================== APP ================== #
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🚗 Sistema Parqueadero PRO")
        self.geometry("1300x720")
        self.configure(bg=BG_MAIN)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#111111",
            foreground="white",
            fieldbackground="#111111",
            rowheight=30,
            bordercolor=GREEN,
            borderwidth=1
        )

        style.configure(
            "Treeview.Heading",
            background=GREEN,
            foreground="black",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", GREEN)],
            foreground=[("selected", "black")]
        )

        # ===== SIDEBAR ===== #
        self.sidebar = tk.Frame(self, bg=BG_PANEL, width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="🚗 PARQUEADERO",
            bg=BG_PANEL,
            fg=GREEN,
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # ===== CONTENEDOR ===== #
        self.container = tk.Frame(self, bg=BG_MAIN)
        self.container.pack(side="right", fill="both", expand=True)

        self.buttons = []

        for name, url in ENDPOINTS.items():

            btn = tk.Button(
                self.sidebar,
                text=name,
                fg="white",
                bg="#1a1a1a",
                activebackground=GREEN,
                activeforeground="black",
                relief="flat",
                height=2,
                font=("Arial", 10, "bold"),
                cursor="hand2",
                command=lambda u=url, n=name: self.load_module(u, n)
            )

            btn.pack(fill="x", pady=4, padx=12)
            self.buttons.append(btn)

        self.load_module(ENDPOINTS["Cliente"], "Cliente")

    def highlight(self, name):

        for btn in self.buttons:

            btn.config(
                bg=GREEN if btn["text"] == name else "#1a1a1a",
                fg="black" if btn["text"] == name else "white"
            )

    def load_module(self, url, name):

        self.highlight(name)

        for widget in self.container.winfo_children():
            widget.destroy()

        ModuleFrame(self.container, url).pack(fill="both", expand=True)


# ================== MODULO ================== #
class ModuleFrame(tk.Frame):

    def __init__(self, parent, url):
        super().__init__(parent, bg=BG_MAIN)

        self.url = url
        self.data = []
        self.fields = []
        self.entries = {}
        self.relations_data = {}

        self.build_ui()
        self.fetch_all()

    def styled_button(self, parent, text, command, color=GREEN):

        return tk.Button(
            parent,
            text=text,
            bg=color,
            fg="black",
            activebackground=GREEN_HOVER,
            activeforeground="black",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=6,
            command=command
        )

    def build_ui(self):

        # ===== TABLA ===== #
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected)

        # ===== FORM ===== #
        container = tk.Frame(self, bg=BG_PANEL)
        container.pack(fill="both", padx=10, pady=10)

        canvas = tk.Canvas(
            container,
            bg=BG_PANEL,
            height=230,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        self.form = tk.Frame(canvas, bg=BG_PANEL)

        self.form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== BOTONES ABAJO ===== #
        bottom = tk.Frame(self, bg=BG_MAIN)
        bottom.pack(fill="x", pady=10)

        self.styled_button(
            bottom,
            "➕ Crear",
            self.create
        ).pack(side="left", padx=5)

        self.styled_button(
            bottom,
            "✏️ Editar",
            self.update
        ).pack(side="left", padx=5)

        self.styled_button(
            bottom,
            "❌ Eliminar",
            self.delete,
            "#ff4444"
        ).pack(side="left", padx=5)

        tk.Button(
            bottom,
            text="🧹 Limpiar",
            bg="#333333",
            fg="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.clear_form
        ).pack(side="left", padx=5)

        tk.Button(
            bottom,
            text="🧾 Recibo",
            bg="#00bcd4",
            fg="black",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.generar_recibo
        ).pack(side="left", padx=5)

    def fetch_all(self):

        try:

            res = requests.get(self.url)

            if res.status_code != 200:

                messagebox.showerror(
                    "Error",
                    f"Error API:\n{res.status_code}\n{res.text}"
                )

                return

            self.data = res.json()

            if isinstance(self.data, dict):
                self.data = self.data.get("results", [])

            if not self.data:
                self.fields = self.get_default_fields()
            else:
                self.fields = list(self.data[0].keys())

            if "ingresosalida" in self.url:
                if "tarifa" not in self.fields:
                    self.fields.append("tarifa")

            self.load_relations()
            self.build_table()
            self.build_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_default_fields(self):

        if "cliente" in self.url:
            return [
                "id","tipo_identificacion","identificacion",
                "nombre","apellido","direccion",
                "telefono","estado"
            ]

        elif "vehiculo" in self.url:
            return [
                "id","placa","marca",
                "color","estado","tipo_vehiculo"
            ]

        elif "tipovehiculo" in self.url:
            return [
                "id","nombre",
                "descripcion","estado"
            ]

        elif "tarifa" in self.url:
            return [
                "id","tiempo",
                "valor","estado","tipo_vehiculo"
            ]

        elif "empleado" in self.url:
            return [
                "id","identificacion","nombre",
                "apellido","telefono","rol","estado"
            ]

        elif "usuario" in self.url:
            return [
                "id","usuario",
                "contrasena","estado","empleado"
            ]

        elif "ingresosalida" in self.url:
            return [
                "id",
                "fecha_entrada",
                "fecha_salida",
                "tiempo_total",
                "numero_recibo",
                "total_pago",
                "forma_pago_descripcion",
                "estado",
                "vehiculo",
                "empleado",
                "cliente",
                "tarifa"
            ]

        return []

    def load_relations(self):

        for field, url in RELATIONS.items():

            try:

                r = requests.get(url)

                if r.status_code != 200:
                    self.relations_data[field] = []
                    continue

                data = r.json()

                if isinstance(data, dict):
                    data = data.get("results", [])

                self.relations_data[field] = data

            except:
                self.relations_data[field] = []

    def build_table(self):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = self.fields
        self.tree["show"] = "headings"

        for col in self.fields:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for row in self.data:

            values = []

            for field in self.fields:
                values.append(row.get(field, ""))

            self.tree.insert("", "end", values=values)

    def build_form(self):

        for widget in self.form.winfo_children():
            widget.destroy()

        self.entries = {}

        for i, field in enumerate(self.fields):

            if field == "id":
                continue

            frame = tk.Frame(self.form, bg=BG_PANEL)
            frame.grid(row=i//3, column=i%3, padx=15, pady=10)

            tk.Label(
                frame,
                text=field,
                fg=GREEN,
                bg=BG_PANEL,
                font=("Arial", 10, "bold")
            ).pack()

            # ===== RELACIONES ===== #
            if field in RELATIONS:

                combo = ttk.Combobox(
                    frame,
                    width=28,
                    state="readonly"
                )

                values = []

                for item in self.relations_data[field]:

                    texto = ""

                    if "nombre" in item:
                        texto = item["nombre"]

                    elif "placa" in item:
                        texto = item["placa"]

                    elif "usuario" in item:
                        texto = item["usuario"]

                    elif "valor" in item:
                        texto = item["valor"]

                    else:
                        texto = str(item["id"])

                    values.append(f"{item['id']} - {texto}")

                combo["values"] = values
                combo.pack(pady=3)

                self.entries[field] = combo

                if field == "vehiculo":
                    combo.bind("<<ComboboxSelected>>", self.auto_asignar_tarifa)
                elif field == "tarifa":
                    combo.bind("<<ComboboxSelected>>", self.calcular_totales)

            elif field == "estado":

                var = tk.BooleanVar()

                tk.Checkbutton(
                    frame,
                    text="Activo",
                    variable=var,
                    bg=BG_PANEL,
                    fg="white",
                    selectcolor="#111"
                ).pack()

                self.entries[field] = var

            elif "fecha" in field:

                entry = tk.Entry(
                    frame,
                    bg=BG_INPUT,
                    fg="white",
                    insertbackground="white",
                    width=30
                )

                entry.pack(pady=3)

                tk.Button(
                    frame,
                    text="Ahora",
                    bg=GREEN,
                    fg="black",
                    relief="flat",
                    command=lambda e=entry: [e.delete(0, tk.END), e.insert(0, datetime.now().isoformat()), self.calcular_totales()]
                ).pack(pady=2)

                self.entries[field] = entry

            elif field == "contrasena":

                entry = tk.Entry(
                    frame,
                    show="*",
                    bg=BG_INPUT,
                    fg="white",
                    insertbackground="white",
                    width=30
                )

                entry.pack(pady=3)
                self.entries[field] = entry

            else:

                entry = tk.Entry(
                    frame,
                    bg=BG_INPUT,
                    fg="white",
                    insertbackground="white",
                    width=30
                )

                entry.pack(pady=3)
                self.entries[field] = entry

    def get_form_data(self):

        data = {}

        for k, v in self.entries.items():

            if isinstance(v, ttk.Combobox):

                if v.get():
                    data[k] = int(v.get().split("-")[0])
                else:
                    data[k] = None

            elif isinstance(v, tk.BooleanVar):
                data[k] = v.get()

            else:
                data[k] = v.get()

        return data

    def load_selected(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]
        data = dict(zip(self.fields, values))

        for k, v in self.entries.items():

            if k in data:

                if isinstance(v, ttk.Combobox):

                    for item in v["values"]:

                        if item.startswith(str(data[k])):
                            v.set(item)

                elif isinstance(v, tk.BooleanVar):
                    v.set(bool(data[k]))

                else:
                    v.delete(0, tk.END)
                    v.insert(0, data[k])

    

    def auto_asignar_tarifa(self, event=None):
        if "ingresosalida" not in self.url:
            return
        try:
            vehiculo_combo = self.entries.get("vehiculo")
            tarifa_combo = self.entries.get("tarifa")
            
            if not vehiculo_combo or not tarifa_combo:
                return
                
            val_vehiculo = vehiculo_combo.get()
            if not val_vehiculo:
                return
                
            vehiculo_id = val_vehiculo.split("-")[0].strip()
            
            tipo_vehiculo_id = None
            for v in self.relations_data.get("vehiculo", []):
                if str(v.get("id")) == str(vehiculo_id):
                    tipo_vehiculo_id = str(v.get("tipo_vehiculo"))
                    break
                    
            if not tipo_vehiculo_id:
                return
                
            for t in self.relations_data.get("tarifa", []):
                t_tipo = str(t.get("tipo_vehiculo"))
                if t_tipo == tipo_vehiculo_id:
                    tarifa_id = str(t.get("id"))
                    for item in tarifa_combo["values"]:
                        if item.startswith(f"{tarifa_id} -") or item == str(tarifa_id):
                            tarifa_combo.set(item)
                            self.calcular_totales()
                            break
                    break
        except Exception as e:
            print("Error auto-asignando tarifa:", e)
        
       

    def calcular_totales(self, *args):
        if "ingresosalida" not in self.url:
            return
        try:
            f_entrada = self.entries.get("fecha_entrada")
            f_salida = self.entries.get("fecha_salida")
            tarifa_combo = self.entries.get("tarifa")
            total_entry = self.entries.get("total_pago")
            tiempo_entry = self.entries.get("tiempo_total")

            if f_entrada and f_salida and tarifa_combo:
                val_entrada = f_entrada.get()
                val_salida = f_salida.get()
            
                if val_entrada and val_salida:
                    dt_entrada = datetime.fromisoformat(val_entrada.replace("Z", ""))
                    dt_salida = datetime.fromisoformat(val_salida.replace("Z", ""))
                
                    diferencia = dt_salida - dt_entrada
                    horas = diferencia.total_seconds() / 3600
                    if horas < 0:
                        horas = 0
                
                    if tiempo_entry:
                        tiempo_entry.delete(0, tk.END)
                        tiempo_entry.insert(0, f"{round(horas, 2)}")

                    tarifa_val = tarifa_combo.get()
                    if tarifa_val:
                        tarifa_id = tarifa_val.split("-")[0].strip()
                        total = 0.0
                        for t in self.relations_data.get("tarifa", []):
                            if str(t.get("id")) == str(tarifa_id):
                                precio_unitario = float(t.get("valor", 0))
                                total = horas * precio_unitario
                                break
                            
                        if total_entry:
                                total_entry.delete(0, tk.END)
                                total_entry.insert(0, f"{round(total, 2)}")
        except Exception as e:
            print("Error en cálculo automático:", e)
    

    def clear_form(self):

        for v in self.entries.values():

            if isinstance(v, ttk.Combobox):
                v.set("")

            elif isinstance(v, tk.BooleanVar):
                v.set(False)

            else:
                v.delete(0, tk.END)

    def create(self):

        data = self.get_form_data()

        if all(v == "" or v is None for v in data.values()):

            messagebox.showwarning(
                "Aviso",
                "Debes llenar al menos un campo"
            )

            return

        try:

            response = requests.post(self.url, json=data)

            if response.status_code in [200, 201]:

                self.fetch_all()

                messagebox.showinfo(
                    "OK",
                    "Creado correctamente"
                )

            else:

                messagebox.showerror(
                    "Error API",
                    f"{response.status_code}\n\n{response.text}"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update(self):

        selected = self.tree.focus()

        if not selected:
            return

        row = self.tree.item(selected)["values"]
        id_ = row[0]

        try:

            response = requests.put(
                self.url + f"{id_}/",
                json=self.get_form_data()
            )

            if response.status_code in [200, 202]:

                self.fetch_all()

                messagebox.showinfo(
                    "OK",
                    "Actualizado"
                )

            else:

                messagebox.showerror(
                    "Error API",
                    f"{response.status_code}\n\n{response.text}"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete(self):

        selected = self.tree.focus()

        if not selected:
            return

        row = self.tree.item(selected)["values"]
        id_ = row[0]

        try:

            response = requests.delete(self.url + f"{id_}/")

            if response.status_code in [200, 204]:

                self.fetch_all()

                messagebox.showinfo(
                    "OK",
                    "Eliminado"
                )

            else:

                messagebox.showerror(
                    "Error API",
                    f"{response.status_code}\n\n{response.text}"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= RECIBO ================= #
    def generar_recibo(self):

        selected = self.tree.focus()

        if not selected:

            messagebox.showwarning(
                "Aviso",
                "Selecciona un registro"
            )

            return

        values = self.tree.item(selected)["values"]
        data = dict(zip(self.fields, values))

        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo TXT", "*.txt")]
        )

        if not archivo:
            return

        try:

            with open(archivo, "w", encoding="utf-8") as f:

                f.write("=====================================\n")
                f.write("         PARQUEADERO TICKET\n")
                f.write("=====================================\n")
                f.write(f"Fecha: {datetime.now()}\n")
                f.write("-------------------------------------\n")

                for campo, valor in data.items():
                    f.write(f"{campo.upper()}: {valor}\n")

                f.write("-------------------------------------\n")
                f.write("GRACIAS POR SU VISITA 🚗\n")
                f.write("=====================================\n")

            messagebox.showinfo(
                "OK",
                "Recibo generado correctamente"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

    # commit 2 listo.