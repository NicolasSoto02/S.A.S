from django.shortcuts import render,redirect,get_object_or_404
from .models import Categoria,SLA,Ticket,Estado_Ticket,Mensaje,Usuario,Foto_Ticket
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

# Create your views here.

def index(request):
    context = {}
    return render(request, 'SAS_tickets/index.html', context)

@login_required
def tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    context = {
        "tickets": tickets
    }

    return render(request,'SAS_tickets/tickets.html', context)

@login_required
def crear_ticket(request):
    categorias = Categoria.objects.all()
    sla = SLA.objects.all()
    context = {
        "categorias": categorias,
        "sla": sla
    }

    if request.method == 'POST':
        titulo    = request.POST['titulo']
        user   = request.user
        categoria = request.POST['categoria']
        prioridad = request.POST['nivel_urgencia']
        estado    = Estado_Ticket.objects.get(estado="Nuevo")
        fotos_subidas = request.FILES.getlist('fotos')

        categoriaObj = Categoria.objects.get(id_categoria=categoria) 
        prioridadObj = SLA.objects.get(id_prioridad=prioridad)
        estadoObj    = Estado_Ticket.objects.get(estado=estado)
        ticketObj    = Ticket.objects.create(
            titulo       = titulo,
            user         = user,
            id_categoria = categoriaObj,
            id_prioridad = prioridadObj,
            id_estado    = estadoObj
        )

        mensajeObj   = request.POST['mensaje']

        usuario = Usuario.objects.get(user=user)
        nuevo_mensaje = Mensaje.objects.create(
            mensaje   = mensajeObj,
            id_ticket = ticketObj,
            user      = user,
            usuario = usuario
        )

        for foto_ticket in fotos_subidas:
            Foto_Ticket.objects.create(
                foto=foto_ticket,
                id_mensaje = nuevo_mensaje, 
                id_ticket  = ticketObj
            )
        return redirect('ver_ticket', id_ticket=ticketObj.id_ticket)

    return render(request, 'SAS_tickets/crear_ticket.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        profilepic = request.FILES.get('profilepic')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El usuario ya existe.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo ya esta registrado.')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                user.save()


                usuario = Usuario(user=user, is_techsupp=False, profilepic=profilepic)
                usuario.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('tickets') 

        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    return render(request, 'registration/signup.html')


@login_required
def ver_ticket(request, id_ticket):
    ticket = get_object_or_404(Ticket, id_ticket=id_ticket)
    mensajes = Mensaje.objects.filter(id_ticket=id_ticket)
    fotos = Foto_Ticket.objects.filter(id_ticket=ticket)
    default_pfp = f"{settings.MEDIA_URL}pfp/default_pfp.png"
    
    context = {
        "ticket": ticket,
        "mensajes": mensajes,
        "fotos": fotos,
        "default_pfp": default_pfp
    }

    if request.method == 'POST':
        mensaje = request.POST['mensaje']
        user = request.user
        usuario = Usuario.objects.get(user=user)

        fotos_subidas = request.FILES.getlist('fotos')
        nuevo_mensaje = Mensaje.objects.create(
            mensaje   = mensaje,
            id_ticket = ticket,
            user      = user,
            usuario   = usuario
        )

        for foto_ticket in fotos_subidas:
            Foto_Ticket.objects.create(
                foto=foto_ticket,
                id_mensaje=nuevo_mensaje, 
                id_ticket=ticket
            )

        return redirect('ver_ticket', id_ticket=ticket.id_ticket)
    return render(request, 'SAS_TICKETS/ver_ticket.html', context)

@login_required
def perfil(request):
    user    = request.user
    usuario = Usuario.objects.get(user=user)
    default_pfp = f"{settings.MEDIA_URL}pfp/default_pfp.png"
    context = {
        "user": user,
        "usuario": usuario,
        "default_pfp": default_pfp
    }
    return render(request,'SAS_TICKETS/perfil.html', context)

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='/login/')
def panel_de_control(request):
    return render(request, 'SuperUser/panel_de_control.html')

@user_passes_test(is_superuser, login_url='/login/')
def view_SLA(request):
    sla = SLA.objects.all()
    context ={
        "sla":sla
    }
    return render(request, 'SuperUser/SLA.html', context)


@user_passes_test(is_superuser, login_url='/login/')
def categorias(request):
    categorias = Categoria.objects.all()
    context ={
        "categorias":categorias
    }
    return render(request, 'SuperUser/categorias.html', context)

@user_passes_test(is_superuser, login_url='/login/')
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        Categoria.objects.create(
            nombre = nombre,
            descripcion = descripcion
        )
        return redirect('categorias')

    return render(request,'SuperUser/crear_categoria.html')

@user_passes_test(is_superuser, login_url='/login/')
def editar_categoria(request, id_categoria):
    categoria = Categoria.objects.get(id_categoria=id_categoria)
    context = {
        "categoria": categoria
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        categoria.nombre      = nombre
        categoria.descripcion = descripcion
        categoria.save()

        return redirect('categorias')
    return render(request, 'SuperUser/editar_categoria.html', context)

@user_passes_test(is_superuser, login_url='/login/')
def borrar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    categoria.delete()
    return redirect('categorias')

@user_passes_test(is_superuser, login_url='/login/')
def crear_admin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        password = User.objects.make_random_password()
        password_short = password[-5:]

        print(password)

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password_short
        )

        user.is_staff = True
        user.save()

        Usuario.objects.create(
            user=user,
            is_techsupp=True
        )
        return redirect('panel_de_control')
    return render(request, 'SuperUser/crear_admin.html')

