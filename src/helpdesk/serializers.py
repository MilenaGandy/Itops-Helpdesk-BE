from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Rol, Categoria, Prioridad, EstadoTicket, MedioContacto, TipoGestion, SLA,
    Cliente, ContactoCliente, Ticket, GestionTicket, SatisfaccionCliente
)

# --- Serializers para el sistema de autenticación de Django ---
class UserSerializer(serializers.ModelSerializer):
    """Serializer para mostrar información básica del usuario."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# --- Serializers para los modelos de "Catálogo" ---

class RolSerializer(serializers.ModelSerializer):
    """Serializer para el rol del usuario."""
    class Meta:
        model = Rol
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para la categoría del ticket."""
    class Meta:
        model = Categoria
        fields = '__all__'

class PrioridadSerializer(serializers.ModelSerializer):
    """Serializer para la prioridad del ticket."""
    class Meta:
        model = Prioridad
        fields = '__all__'

class EstadoTicketSerializer(serializers.ModelSerializer):
    """Serializer para el estado del ticket."""
    class Meta:
        model = EstadoTicket
        fields = '__all__'

class MedioContactoSerializer(serializers.ModelSerializer):
    """Serializer para el medio de contacto."""
    class Meta:
        model = MedioContacto
        fields = '__all__'

class TipoGestionSerializer(serializers.ModelSerializer):
    """Serializer para el tipo de gestión."""
    class Meta:
        model = TipoGestion
        fields = '__all__'

class SLASerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = '__all__'


# --- Serializers para los modelos principales ---

class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el cliente."""
    class Meta:
        model = Cliente
        fields = '__all__'

class ContactoClienteSerializer(serializers.ModelSerializer):
    """Serializer para el contacto del cliente."""
    class Meta:
        model = ContactoCliente
        fields = '__all__'

class GestionTicketSerializer(serializers.ModelSerializer):
    """Serializer para la gestión del ticket."""
    class Meta:
        model = GestionTicket
        fields = '__all__'

class SatisfaccionClienteSerializer(serializers.ModelSerializer):
    """Serializer para la satisfacción del cliente."""
    class Meta:
        model = SatisfaccionCliente
        fields = '__all__'


# --- Serializers avanzados para el modelo Ticket ---

class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear y actualizar tickets.
    Acepta los IDs de los modelos relacionados para la escritura.
    """
    class Meta:
        model = Ticket
        fields = [
            'asunto', 'descripcion', 'cliente', 'contacto_solicitante',
            'medio_contacto', 'prioridad', 'categoria', 'estado', 'agente_asignado'
        ]

class TicketListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para leer (listar y ver detalle de) tickets.
    Muestra los objetos completos de los modelos relacionados (nested serialization),
    lo que es mucho más útil para el frontend.
    """
    cliente = ClienteSerializer(read_only=True)
    contacto_solicitante = ContactoClienteSerializer(read_only=True)
    medio_contacto = MedioContactoSerializer(read_only=True)
    prioridad = PrioridadSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    estado = EstadoTicketSerializer(read_only=True)
    agente_asignado = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'asunto', 'descripcion', 'fecha_hora_creacion',
            'fecha_hora_ultima_actualizacion', 'fecha_hora_cierre', 'cliente',
            'contacto_solicitante', 'medio_contacto', 'prioridad',
            'categoria', 'estado', 'agente_asignado'
        ]


# --- Serializer para el Registro de Usuarios ---
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios.
    Incluye validación para asegurar que las dos contraseñas coincidan.
    """
    # Campo para la confirmación de la contraseña (no se guarda en la BD)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User # Utiliza el modelo de Usuario por defecto de Django
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True} # La contraseña no debe ser retornada en la respuesta
        }

    def validate(self, data):
        """
        Verifica que las dos contraseñas ingresadas sean iguales.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        """
        Crea y guarda un nuevo usuario en la base de datos,
        asegurándose de hashear la contraseña correctamente.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
