from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from .models import (
    Rol, Categoria, Prioridad, EstadoTicket, MedioContacto, TipoGestion, SLA,
    Cliente, ContactoCliente, Ticket, GestionTicket, SatisfaccionCliente
)
from .serializers import (
    UserSerializer, RolSerializer, CategoriaSerializer, PrioridadSerializer,
    EstadoTicketSerializer, MedioContactoSerializer, TipoGestionSerializer, SLASerializer,
    ClienteSerializer, ContactoClienteSerializer, TicketCreateUpdateSerializer,
    TicketListDetailSerializer, GestionTicketSerializer, SatisfaccionClienteSerializer,
    RegisterSerializer
)

# --- Vistas para los modelos de "Catálogo" y Principales ---

class UserViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de usuario."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RolViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de rol."""
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de categoría."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PrioridadViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de prioridad."""
    queryset = Prioridad.objects.all()
    serializer_class = PrioridadSerializer

class EstadoTicketViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de estado del ticket."""
    queryset = EstadoTicket.objects.all()
    serializer_class = EstadoTicketSerializer

class MedioContactoViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de medio de contacto."""
    queryset = MedioContacto.objects.all()
    serializer_class = MedioContactoSerializer

class TipoGestionViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de tipo de gestión."""
    queryset = TipoGestion.objects.all()
    serializer_class = TipoGestionSerializer

class SLAViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de SLA."""
    queryset = SLA.objects.all()
    serializer_class = SLASerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de cliente."""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ContactoClienteViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de contacto del cliente."""
    queryset = ContactoCliente.objects.all()
    serializer_class = ContactoClienteSerializer

class GestionTicketViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de gestión del ticket."""
    queryset = GestionTicket.objects.all()
    serializer_class = GestionTicketSerializer

class SatisfaccionClienteViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de satisfacción del cliente."""
    queryset = SatisfaccionCliente.objects.all()
    serializer_class = SatisfaccionClienteSerializer


# --- Vista avanzada para Tickets ---

class TicketViewSet(viewsets.ModelViewSet):
    """Vista para el modelo de ticket con serializers diferenciados para lectura y escritura."""
    queryset = Ticket.objects.all().order_by('-fecha_hora_creacion')

    def get_serializer_class(self):
        """
        Determina qué serializer usar.
        - Para leer (list, retrieve), usa el serializer detallado.
        - Para escribir (create, update), usa el serializer simple.
        """
        if self.action in ['list', 'retrieve']:
            return TicketListDetailSerializer
        return TicketCreateUpdateSerializer


# --- Vista para el Registro de Usuarios ---
class RegisterView(generics.CreateAPIView):
    """
    Vista para crear un nuevo usuario.
    Solo permite peticiones POST.
    """
    queryset = User.objects.all()
    # Permite que cualquier usuario (incluso no autenticado) pueda acceder a esta vista
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer