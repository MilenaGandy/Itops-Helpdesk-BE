from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Se crea una instancia del Router
router = DefaultRouter()

# Se registran todas las vistas en el router
router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RolViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'prioridades', views.PrioridadViewSet)
router.register(r'estados-ticket', views.EstadoTicketViewSet)
router.register(r'medios-contacto', views.MedioContactoViewSet)
router.register(r'tipos-gestion', views.TipoGestionViewSet)
router.register(r'slas', views.SLAViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'contactos-cliente', views.ContactoClienteViewSet)
router.register(r'gestiones-ticket', views.GestionTicketViewSet)
router.register(r'satisfaccion-cliente', views.SatisfaccionClienteViewSet)
router.register(r'tickets', views.TicketViewSet)

# Se define el patrón de URL principal que incluirá todas las rutas generadas por el router.
urlpatterns = [
    # Esto creará todas las rutas bajo el prefijo /api/
    # ej: /api/tickets/, /api/clientes/, etc.
    path('api/', include(router.urls)),
]
