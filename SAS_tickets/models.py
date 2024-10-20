from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    is_techsupp = models.BooleanField(default=False)
    profilepic  = models.ImageField(upload_to='pfp/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='id_categoria', primary_key=True)
    nombre       = models.CharField(max_length=50, blank=False, null=False)
    descripcion  = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return str(self.nombre)
class Categoria_tecnico(models.Model):
    id_asignacion = models.AutoField(db_column='id_asignacion', primary_key=True)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignacion_categoria') 
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asignacion_categoria')
    id_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='id_categoria')
    
    def __str__(self):
         return f"{self.user.username} - {self.id_categoria.nombre}"



class SLA(models.Model):
    id_prioridad         = models.AutoField(db_column='id_prioridad', primary_key=True)
    nombre_SLA           = models.CharField(max_length=50, blank=False, null=False)
    respuesta_minutos    = models.IntegerField(blank=False, null=False)
    solucion_minutos_min = models.IntegerField(blank=False, null=False)
    solucion_minutos_max = models.IntegerField(blank=False, null=False)
    nivel_prioridad      = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return str(self.nombre_SLA)

class Estado_Ticket(models.Model):
    id_estado = models.AutoField(db_column='id_estado', primary_key=True)
    estado    = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.estado)

class Ticket(models.Model):
    id_ticket    = models.AutoField(db_column='id_ticket', primary_key=True)
    titulo       = models.CharField(max_length=50, blank=False, null=False)
    fecha        = models.DateTimeField(auto_now_add=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_as_user')  
    tecnico      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets_as_technician') 
    id_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='id_categoria')
    id_prioridad = models.ForeignKey('SLA', on_delete=models.CASCADE, db_column='id_prioridad')
    id_estado    = models.ForeignKey('Estado_Ticket', on_delete=models.CASCADE, db_column='id_estado')

    def __str__(self):
        return str(self.titulo)

class Derivacion(models.Model):
    id_derivacion  = models.AutoField(db_column='id_derivacion', primary_key=True)
    descripcion    = models.CharField(max_length=200, blank=False, null=False)
    tecnico_envia  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='derivaciones_envia')  
    tecnico_recibe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='derivaciones_recibe')  
    id_ticket      = models.ForeignKey('Ticket', on_delete=models.CASCADE, db_column='id_ticket')

    def __str__(self):
        return str(self.id_derivacion)

class Mensaje(models.Model):
    id_mensaje = models.AutoField(db_column='id_mensaje', primary_key=True)
    mensaje    = models.CharField(max_length=1000, blank=False, null=False)
    fecha      = models.DateTimeField(auto_now_add=True)
    id_ticket  = models.ForeignKey('Ticket', on_delete=models.CASCADE, db_column='id_ticket')
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes') 
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes')


    def __str__(self):
        return str(self.id_mensaje)

class Foto_Ticket(models.Model):
    id_foto    = models.AutoField(db_column='id_foto', primary_key=True)
    foto       = models.ImageField(upload_to='ticket_pic/', blank=True, null=True)
    id_mensaje = models.ForeignKey('Mensaje', on_delete=models.CASCADE, db_column='id_mensaje')
    id_ticket  = models.ForeignKey('Ticket', on_delete=models.CASCADE, db_column='id_ticket')

    def __str__(self):
        return str(self.id_foto)

class Tipo_Sancion(models.Model):
    id_tipo_sancion = models.AutoField(db_column='id_tipo_sancion', primary_key=True)
    ban             = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.ban)

class Sancion(models.Model):
    id_sancion       = models.AutoField(db_column='id_sancion', primary_key=True)
    duracion_horas   = models.IntegerField(blank=False, null=False)
    motivo           = models.CharField(max_length=100, blank=False, null=False)
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sanciones') 
    id_tipo_sancion  = models.ForeignKey('Tipo_Sancion', on_delete=models.CASCADE, db_column='id_tipo_sancion')

    def __str__(self):
        return str(self.id_sancion)

class Reporte(models.Model):
    id_reporte = models.AutoField(db_column='id_reporte', primary_key=True)
    fecha      = models.DateTimeField(auto_now_add=True)
    reporte    = models.FileField(upload_to='reportes/', blank=False, null=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes') 

    def __str__(self):
        return str(self.id_reporte)

class Auditoria(models.Model):
    id_accion = models.AutoField(db_column='id_reporte', primary_key=True)
    accion    = models.CharField(max_length=200, blank=False, null=False)
    fecha     = models.DateTimeField(auto_now_add=True)
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auditorias')

    def __str__(self):
        return str(self.id_accion)

class Email(models.Model):
    id_email   = models.AutoField(db_column='id_email', primary_key=True)
    titulo     = models.CharField(max_length=300, blank=False, null=False)
    mensaje    = models.CharField(max_length=5000, blank=False, null=False)
    comentario = models.CharField(max_length=500, blank=False, null=False)
    tipo       = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return str(self.id_email)

class Log_Email(models.Model):
    id_log_email = models.AutoField(db_column='id_log_email', primary_key=True)
    fecha        = models.DateTimeField(auto_now_add=True)
    id_email     = models.ForeignKey('Email', on_delete=models.CASCADE, db_column='id_email')
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs_email')

    def __str__(self):
        return str(self.id_log_email)
