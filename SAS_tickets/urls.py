from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('tickets/', views.tickets, name="tickets"),
    path('crear_ticket/',views.crear_ticket, name="crear_ticket"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='registration/signup'),
    path('ticket/<int:id_ticket>/', views.ver_ticket, name='ver_ticket'),
    path('perfil/', views.perfil, name="perfil"),
    path('panel_de_control/',views.panel_de_control, name="panel_de_control"),
    path('SLA/', views.view_SLA, name="SLA"),
    path('categorias/', views.categorias, name="categorias"),
    path('crear_categoria/', views.crear_categoria, name="crear_categoria"),
    path('editar_categoria/<int:id_categoria>/', views.editar_categoria, name="editar_categoria"),
    path('borrar_categoria/<int:id_categoria>/', views.borrar_categoria, name="borrar_categoria"),
    path('crear_admin/', views.crear_admin , name="crear_admin"),
    path('panel_admin/', views.panel_admin , name="panel_admin"),
    path('tecnicos/', views.tecnicos , name="tecnicos"),
    path('crear_tecnico/', views.crear_tecnico , name="crear_tecnico"),
    path('areas_tecnico/<str:username>/', views.areas_tecnico , name="areas_tecnico"), 
    path('borrar_categoria_tecnico/<int:id_asignacion>/', views.borrar_categoria_tecnico, name='borrar_categoria_tecnico'),
    path('tickets_tecnico/', views.tickets_tecnico , name="tickets_tecnico"),
    path('ver_ticket_tecnico/<int:id_ticket>/', views.ver_ticket_tecnico , name="ver_ticket_tecnico"),
    path('cambiar_estado_ticket/<int:id_ticket>/', views.cambiar_estado_ticket, name='cambiar_estado_ticket'),
    #path('', views. , name=""),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
