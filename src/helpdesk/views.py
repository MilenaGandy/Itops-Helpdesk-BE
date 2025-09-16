from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import (
    Rol, Categoria, Prioridad, EstadoTicket, MedioContacto, TipoGestion, SLA,
    Cliente, ContactoCliente, Ticket, GestionTicket, SatisfaccionCliente
)
from .serializers import (
    UserSerializer, RolSerializer, CategoriaSerializer, PrioridadSerializer,
    EstadoTicketSerializer, MedioContactoSerializer, TipoGestionSerializer, SLASerializer,
    ClienteSerializer, ContactoClienteSerializer, TicketCreateUpdateSerializer,
    TicketListDetailSerializer, GestionTicketSerializer, SatisfaccionClienteSerializer
)

# --- Vistas para los modelos de "Catálogo" y Principales ---

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PrioridadViewSet(viewsets.ModelViewSet):
    queryset = Prioridad.objects.all()
    serializer_class = PrioridadSerializer

class EstadoTicketViewSet(viewsets.ModelViewSet):
    queryset = EstadoTicket.objects.all()
    serializer_class = EstadoTicketSerializer

class MedioContactoViewSet(viewsets.ModelViewSet):
    queryset = MedioContacto.objects.all()
    serializer_class = MedioContactoSerializer

class TipoGestionViewSet(viewsets.ModelViewSet):
    queryset = TipoGestion.objects.all()
    serializer_class = TipoGestionSerializer

class SLAViewSet(viewsets.ModelViewSet):
    queryset = SLA.objects.all()
    serializer_class = SLASerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ContactoClienteViewSet(viewsets.ModelViewSet):
    queryset = ContactoCliente.objects.all()
    serializer_class = ContactoClienteSerializer

class GestionTicketViewSet(viewsets.ModelViewSet):
    queryset = GestionTicket.objects.all()
    serializer_class = GestionTicketSerializer

class SatisfaccionClienteViewSet(viewsets.ModelViewSet):
    queryset = SatisfaccionCliente.objects.all()
    serializer_class = SatisfaccionClienteSerializer


# --- Vista avanzada para Tickets ---

class TicketViewSet(viewsets.ModelViewSet):
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
