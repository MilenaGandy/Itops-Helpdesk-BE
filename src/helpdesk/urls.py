from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserViewSet, RolViewSet, CategoriaViewSet, PrioridadViewSet,
    EstadoTicketViewSet, MedioContactoViewSet, TipoGestionViewSet, SLAViewSet,
    ClienteViewSet, ContactoClienteViewSet, TicketViewSet,
    GestionTicketViewSet, SatisfaccionClienteViewSet, RegisterView, CustomTokenObtainPairView
)

# Se crea una instancia del Router
router = DefaultRouter()

# Se registran todas las vistas en el router
router.register(r'users', UserViewSet)
router.register(r'roles', RolViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'prioridades', PrioridadViewSet)
router.register(r'estados-ticket', EstadoTicketViewSet)
router.register(r'medios-contacto', MedioContactoViewSet)
router.register(r'tipos-gestion', TipoGestionViewSet)
router.register(r'slas', SLAViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'contactos-cliente', ContactoClienteViewSet)
router.register(r'gestiones-ticket', GestionTicketViewSet)
router.register(r'satisfaccion-cliente', SatisfaccionClienteViewSet)
router.register(r'tickets', TicketViewSet)

# Se define el patrón de URL principal que incluirá todas las rutas generadas por el router.
urlpatterns = [
    # Esto creará todas las rutas bajo el prefijo /api/
    # ej: /api/tickets/, /api/clientes/, etc.
    path('api/', include(router.urls)),

    # --- Rutas para el Servicio de Autenticación ---

    # 1. Endpoint para el Registro de Usuarios
    path('api/register/', RegisterView.as_view(), name='auth_register'),

    # 2. Endpoint para el Inicio de Sesión (Login)
    # Recibe 'username' y 'password', devuelve 'access' y 'refresh' tokens.
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 3. Endpoint para refrescar el token de acceso
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
