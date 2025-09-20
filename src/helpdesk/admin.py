from django.contrib import admin
from django.db import models

from helpdesk.models import Rol
from helpdesk.models import Categoria
from helpdesk.models import Prioridad
from helpdesk.models import EstadoTicket
from helpdesk.models import MedioContacto
from helpdesk.models import TipoGestion
from helpdesk.models import SLA
from helpdesk.models import Cliente
from helpdesk.models import ContactoCliente
from helpdesk.models import Ticket
from helpdesk.models import GestionTicket
from helpdesk.models import SatisfaccionCliente
from helpdesk.models import Usuario


class RolModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class CategoriaModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class PrioridadModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nivel',)

class EstadoTicketModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class MedioContactoModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class TipoGestionModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class SLAModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tiempo_respuesta_horas', 'tiempo_resolucion_horas')
    search_fields = ('nombre',)

class ClienteModelAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'nit_empresa', 'telefono_empresa', 'activo')
    search_fields = ('nombre_empresa', 'nit_empresa')
    list_filter = ('activo',)

class ContactoClienteModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'cliente', 'email', 'telefono', 'activo')
    search_fields = ('nombre', 'apellidos', 'email', 'cliente__nombre_empresa')
    list_filter = ('activo', 'cliente')

class TicketModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'asunto', 'cliente', 'contacto_solicitante', 'prioridad',
        'estado', 'agente_asignado', 'fecha_hora_creacion', 'fecha_hora_cierre'
    )
    search_fields = ('asunto', 'descripcion', 'cliente__nombre_empresa', 'agente_asignado__username')
    list_filter = ('prioridad', 'estado', 'categoria', 'medio_contacto', 'fecha_hora_creacion')
    raw_id_fields = ('cliente', 'contacto_solicitante', 'agente_asignado')
    date_hierarchy = 'fecha_hora_creacion'
    ordering = ('-fecha_hora_creacion',)
    readonly_fields = ('fecha_hora_creacion', 'fecha_hora_ultima_actualizacion')
    fieldsets = (
        ('Información Básica', {
            'fields': ('asunto', 'descripcion', 'cliente', 'contacto_solicitante', 'medio_contacto', 'prioridad', 'categoria', 'estado', 'agente_asignado')
        }),
        ('Fechas y Hora', {
            'fields': ('fecha_hora_creacion', 'fecha_hora_ultima_actualizacion', 'fecha_hora_cierre')
        }),
    )
    actions = ['cerrar_tickets']

    def cerrar_tickets(self, request, queryset):
        queryset.update(estado=EstadoTicket.objects.get(nombre='Cerrado'))
    cerrar_tickets.short_description = "Cerrar tickets seleccionados"

admin.site.register(Rol, RolModelAdmin)
admin.site.register(Categoria, CategoriaModelAdmin)
admin.site.register(Prioridad, PrioridadModelAdmin)
admin.site.register(EstadoTicket, EstadoTicketModelAdmin)
admin.site.register(MedioContacto, MedioContactoModelAdmin)
admin.site.register(TipoGestion, TipoGestionModelAdmin)
admin.site.register(SLA, SLAModelAdmin)
admin.site.register(Cliente, ClienteModelAdmin)
admin.site.register(ContactoCliente, ContactoClienteModelAdmin)
admin.site.register(Ticket, TicketModelAdmin)
admin.site.register(GestionTicket)
admin.site.register(SatisfaccionCliente)
admin.site.register(Usuario)
