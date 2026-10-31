from rest_framework import routers
from .api import TipoVehiculoViewSet
from .api import TarifaViewSet
from .api import VehiculoViewSet
from .api import ClienteViewSet
from .api import EmpleadoViewSet
from .api import UsuarioViewSet
from .api import IngresoSalidaViewSet        

router=  routers.DefaultRouter()

router.register('api/tipovehiculo', TipoVehiculoViewSet, 'TipoVehiculo')
router.register('api/tarifa', TarifaViewSet, 'Tarifa')
router.register('api/vehiculo', VehiculoViewSet, 'Vehiculo')
router.register('api/cliente', ClienteViewSet, 'Cliente')
router.register('api/empleado', EmpleadoViewSet, 'Empleado')
router.register('api/usuario', UsuarioViewSet, 'Usuario')
router.register('api/ingresosalida', IngresoSalidaViewSet, 'IngresoSalida')
urlpatterns = router.urls

