from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ApplicationServer
from .forms import ServerForm

@login_required
def home(request):
    applicationServers = ApplicationServer.objects.all()
    return render(request, 'home.html', {'applicationServers': applicationServers})

@login_required
def create_serverForm(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.save()
            return redirect('/infrastructureinventory')
    else:
        form = ServerForm()
    # if form invalid or GET request
    return render(request, 'serverform.html', {"form": form})
