from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)#Charfield texto corto
    descripcion = models.TextField(blank=True)#texto largo
    is_created = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)#el date es para fecha y el time es para hora

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title




class TipoVehiculo(models.Model):
    
    nombre = models.CharField(max_length=100) 
    descripcion = models.TextField(blank=True)#texto largo
    estado =  models.BooleanField(default=True)

   

    def __str__(self):
        return f"{self.nombre}- {self.descripcion}- {self.estado}"

class Tarifa(models.Model):
    tipo_vehiculo=models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    
    tiempo = models.IntegerField()#minutos o horas y sirve para numeros enteros el integer
    valor = models.DecimalField(max_digits=10, decimal_places=2)#valores deicimales
    estado =  models.BooleanField(default=True)#boolean falso verdadero o activo o inactivo


    def __str__(self):
        return f"{self.tipo_vehiculo}- {self.valor}"

class Vehiculo(models.Model):
    
    placa = models.CharField(max_length=10) 
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50) 
    color = models.CharField(max_length=50) 
    estado =  models.BooleanField(default=True)

    

    def __str__(self):
        return self.placa
class Cliente(models.Model):
    
    tipo_identificacion = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100) 
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20) 
    estado =  models.BooleanField(default=True)
    
    

    def __str__(self):
        return f"{self.nombre}- {self.apellido}- {self.identificacion}"

class Empleado(models.Model):
    
    identificacion = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100) 
    telefono = models.CharField(max_length=20) 
    rol = models.CharField(max_length=50)
    estado =  models.BooleanField(default=True)
    

    

    def __str__(self):
        return f"{self.nombre}- {self.apellido}"

class Usuario(models.Model):
    
    usuario = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=128) 
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    estado =  models.BooleanField(default=True)

    

    def __str__(self):
        return self.usuario

class IngresoSalida(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    tiempo_total = models.IntegerField()#en minutos
    numero_recibo = models.CharField(max_length=50)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2) 
    forma_pago_descripcion = models.CharField(max_length=100) 
    estado =  models.BooleanField(default=True)
    

   

    def __str__(self):
        return f"Registro{self.vehiculo}- {self.empleado}-{self.cliente}-{self.tarifa}"