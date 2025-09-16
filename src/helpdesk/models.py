from django.db import models
from django.contrib.auth.models import User # Recomendado para manejar usuarios

# --- MODELOS DE CATÁLOGOS Y CONFIGURACIÓN ---

class Rol(models.Model):
    """Corresponde a la tabla 'roles'."""
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre del rol (ej: Agente, Supervisor)")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de las responsabilidades del rol")

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    """Corresponde a la tabla 'categorias'."""
    nombre = models.CharField(max_length=150, unique=True, help_text="Nombre de la categoría del ticket (ej: Problemas de Hardware)")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Prioridad(models.Model):
    """Corresponde a la tabla 'prioridades'."""
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre de la prioridad (ej: Alta, Media, Baja)")
    descripcion = models.TextField(blank=True, null=True)
    nivel = models.IntegerField(unique=True, help_text="Nivel numérico de la prioridad (ej: 1 para Alta)")

    def __str__(self):
        return self.nombre

class EstadoTicket(models.Model):
    """Corresponde a la tabla 'estados_ticket'."""
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del estado (ej: Abierto, En Progreso, Cerrado)")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class MedioContacto(models.Model):
    """Corresponde a la tabla 'medios_contacto'."""
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del medio (ej: Llamada Telefónica, Email)")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class TipoGestion(models.Model):
    """Corresponde a la tabla 'tipos_gestion'."""
    nombre = models.CharField(max_length=100, help_text="Nombre del tipo de gestión (ej: Nota Interna, Respuesta al Cliente)")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class SLA(models.Model):
    """Corresponde a la tabla 'slas' (Acuerdos de Nivel de Servicio)."""
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    tiempo_respuesta_horas = models.DecimalField(max_digits=5, decimal_places=2)
    tiempo_resolucion_horas = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre


# --- MODELOS PRINCIPALES ---

class Cliente(models.Model):
    """Corresponde a la tabla 'clientes'."""
    nombre_empresa = models.CharField(max_length=200, unique=True)
    nit_empresa = models.CharField(max_length=50, blank=True, null=True)
    direccion_empresa = models.CharField(max_length=255, blank=True, null=True)
    telefono_empresa = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_empresa

class ContactoCliente(models.Model):
    """Corresponde a la tabla 'contactos_cliente'."""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="contactos")
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.cliente.nombre_empresa})"

class Ticket(models.Model):
    """Corresponde a la tabla central 'tickets'."""
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)
    fecha_hora_ultima_actualizacion = models.DateTimeField(auto_now=True)
    fecha_hora_cierre = models.DateTimeField(null=True, blank=True)

    # --- Relaciones ForeignKey ---
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contacto_solicitante = models.ForeignKey(ContactoCliente, on_delete=models.SET_NULL, null=True, blank=True)
    medio_contacto = models.ForeignKey(MedioContacto, on_delete=models.PROTECT)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoTicket, on_delete=models.PROTECT)
    agente_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_asignados")

    def __str__(self):
        return f"Ticket #{self.id} - {self.asunto}"

class GestionTicket(models.Model):
    """Corresponde a la tabla 'gestiones_ticket', son las acciones o notas de un ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="gestiones")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_gestion = models.ForeignKey(TipoGestion, on_delete=models.PROTECT)
    descripcion = models.TextField()
    fecha_hora_gestion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gestión en Ticket #{self.ticket.id} por {self.usuario.username}"

class SatisfaccionCliente(models.Model):
    """Corresponde a la tabla 'satisfaccion_cliente'. Se usa OneToOneField porque un ticket solo tiene una encuesta."""
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta del Ticket #{self.ticket.id} - Puntuación: {self.puntuacion}"


class Usuario(models.Model):
    # Corresponde a la tabla 'usuarios'
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=250, unique=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    activo = models.BooleanField(default=True)
    roles = models.ManyToManyField(Rol) # Django crea la tabla 'usuario_roles' automáticamente

    def __str__(self):
        return self.nombre_usuario
