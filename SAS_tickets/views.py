from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'SAS_tickets/index.html', context)