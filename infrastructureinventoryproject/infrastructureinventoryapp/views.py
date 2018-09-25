from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ApplicationServer


@login_required
def home(request):
    applicationServers = ApplicationServer.objects.all()
    return render(request, 'home.html', {'applicationServers': applicationServers})