from django.contrib import admin
from.models import TipoVehiculo,Tarifa,Vehiculo,Cliente,Empleado,Usuario,IngresoSalida

@admin.register(TipoVehiculo)
class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display=['nombre','descripcion','estado']

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin): 
    list_display=['tipo_vehiculo', 'tiempo', 'valor', 'estado']

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'marca', 'color','estado']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['identificacion', 'nombre', 'apellido', 'telefono', 'estado']


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['identificacion', 'nombre', 'apellido', 'rol', 'estado']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empleado', 'estado']


@admin.register(IngresoSalida)
class IngresoSalidaAdmin(admin.ModelAdmin):
    list_display = [
        'vehiculo',
        'cliente',
        'empleado',
        'tarifa',
        'fecha_entrada',
        'fecha_salida',
        'total_pago',
        'estado'
    ]
