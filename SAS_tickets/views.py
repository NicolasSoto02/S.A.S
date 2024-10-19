from django.shortcuts import render,redirect,get_object_or_404
from .models import Categoria,SLA,Ticket,Estado_Ticket,Mensaje
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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

    return render(request, 'SAS_tickets/crear_ticket.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def ver_ticket(request, id_ticket):
    ticket = get_object_or_404(Ticket, id_ticket=id_ticket)
    context= {
        "ticket": ticket
    }  
    return render(request, 'SAS_TICKETS/ver_ticket.html', context)