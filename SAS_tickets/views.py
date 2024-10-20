from django.shortcuts import render,redirect,get_object_or_404
from .models import Categoria,SLA,Ticket,Estado_Ticket,Mensaje,Usuario
from django.contrib.auth.decorators import login_required
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
        usuario   = request.user
        categoria = request.POST['categoria']
        prioridad = request.POST['nivel_urgencia']
        estado    = Estado_Ticket.objects.get(estado="Nuevo")

        categoriaObj = Categoria.objects.get(id_categoria=categoria) 
        prioridadObj = SLA.objects.get(id_prioridad=prioridad)
        estadoObj    = Estado_Ticket.objects.get(estado=estado)
        ticketObj    = Ticket.objects.create(
            titulo       = titulo,
            user         = usuario,
            id_categoria = categoriaObj,
            id_prioridad = prioridadObj,
            id_estado    = estadoObj
        )

        mensajeObj   = request.POST['mensaje']
        Mensaje.objects.create(
            mensaje   = mensajeObj,
            id_ticket = ticketObj,
            user      = usuario
        )
        return redirect('tickets')

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
    context= {
        "ticket": ticket,
        "mensajes": mensajes
    }  

    if request.method == 'POST':
        mensajeObj   = request.POST['mensaje']
        usuario   = request.user
        Mensaje.objects.create(
            mensaje   = mensajeObj,
            id_ticket = ticket,
            user      = usuario
        )
        return render(request, 'SAS_TICKETS/ver_ticket.html', context)
    return render(request, 'SAS_TICKETS/ver_ticket.html', context)

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