from django.contrib import admin
from .models import Usuario,Categoria,Categoria_tecnico,SLA,Estado_Ticket,Ticket,Mensaje,Foto_Ticket,Tipo_Sancion,Sancion,Reporte,Auditoria,Email,Log_Email,Derivacion
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Categoria_tecnico)
admin.site.register(SLA)
admin.site.register(Estado_Ticket)
admin.site.register(Ticket)
admin.site.register(Mensaje)
admin.site.register(Foto_Ticket)
admin.site.register(Tipo_Sancion)
admin.site.register(Sancion)
admin.site.register(Reporte)
admin.site.register(Auditoria)
admin.site.register(Email)
admin.site.register(Log_Email)
admin.site.register(Derivacion)
