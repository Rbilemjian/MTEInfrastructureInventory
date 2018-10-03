from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ApplicationServer
from .forms import ServerForm, ServerImportForm
import xlrd


#helper functions
def get_str_date(row, column, worksheet, book):
    tuple = xlrd.xldate.xldate_as_tuple(worksheet.cell_value(row, column), book.datemode)
    return str(tuple[0]) + "-" + str(tuple[1]) + "-" + str(tuple[2])

def save_server(server):
    print(server.private_ip)
    fields = ApplicationServer._meta.get_all_field_names()
    for field in fields:
        if getattr(server, field) == "":
            if ApplicationServer._meta.get_field(field).null:
                setattr(server, field, None)
            else:
                setattr(server, field, "TBD")
    if server.is_virtual_machine == "TBD":
        server.is_virtual_machine = 0
    if server.environment == "TBD":
        server.environment = "Prod"
    server.save()
    return server



#view functions
@login_required
def view_application_servers(request):
    application_servers = ApplicationServer.objects.all()
    return render(request, 'application_server_list.html', {'applicationServers': application_servers})


@login_required
def create_application_server_form(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            save_server(server)
            return redirect('details-view', pk=server.pk)
    else:
        form = ServerForm()
    # if form invalid or GET request
    return render(request, 'application_server_form.html', {"form": form})


@login_required
def import_application_server(request):
    if request.method == 'POST':
        form = ServerImportForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            book = xlrd.open_workbook(file_contents=file.read())
            worksheet = book.sheet_by_name('Sheet1')
            num_rows = worksheet.nrows - 1
            for i in range(1, num_rows):

                app_server = ApplicationServer()

                app_server.service = worksheet.cell_value(i, 0).strip()
                app_server.hostname = worksheet.cell_value(i, 1).strip()
                app_server.primary_application = worksheet.cell_value(i, 2).strip()
                app_server.is_virtual_machine = worksheet.cell_value(i, 3)
                app_server.environment = worksheet.cell_value(i, 4).strip()
                app_server.location = worksheet.cell_value(i, 5).strip()
                app_server.data_center = str(worksheet.cell_value(i, 6)).strip()
                app_server.operating_system = worksheet.cell_value(i, 8).strip()
                app_server.model = worksheet.cell_value(i, 9).strip()
                app_server.serial_number = worksheet.cell_value(i, 10).strip()
                app_server.network = worksheet.cell_value(i, 11).strip()

                if type(worksheet.cell_value(i, 7)) is float:
                    app_server.rack = str(int(worksheet.cell_value(i, 7)))
                else:
                    app_server.rack = str(worksheet.cell_value(i, 7)).strip()

                app_server.private_ip = worksheet.cell_value(i, 12)
                app_server.dmz_public_ip = worksheet.cell_value(i, 13)
                app_server.virtual_ip = worksheet.cell_value(i, 14)
                app_server.nat_ip = worksheet.cell_value(i, 15)
                app_server.ilo_or_cimc = worksheet.cell_value(i, 16).strip()
                app_server.nic_mac_address = worksheet.cell_value(i, 17).strip()
                app_server.switch = worksheet.cell_value(i, 18).strip()
                app_server.port = worksheet.cell_value(i, 19).strip()

                if type(worksheet.cell_value(i, 20)) is float:
                    app_server.purchase_order = str(int(worksheet.cell_value(i, 20)))
                else:
                    app_server.purchase_order = worksheet.cell_value(i, 20)

                if worksheet.cell_value(i, 21) == "":
                    app_server.start_date = None
                else:
                    app_server.start_date = get_str_date(i, 21, worksheet, book)

                if worksheet.cell_value(i, 22) == "":
                    app_server.next_hardware_support_date = None
                else:
                    app_server.next_hardware_support_date = get_str_date(i, 22, worksheet, book)

                if worksheet.cell_value(i, 23) == "":
                    app_server.base_warranty = None
                else:
                    app_server.base_warranty = get_str_date(i, 23, worksheet, book)

                app_server.cpu = worksheet.cell_value(i, 24)
                app_server.ram = worksheet.cell_value(i, 25)
                app_server.c_drive = worksheet.cell_value(i, 26)
                app_server.d_drive = worksheet.cell_value(i, 27)
                app_server.e_drive = worksheet.cell_value(i, 28)
                save_server(app_server)
            return redirect('/infrastructureinventory/applicationserver')
    else:
        form = ServerImportForm()
    # if form invalid or GET request
    return render(request, 'application_server_import.html', {"form": form})


def edit_application_server(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    if request.method == "POST":
        form = ServerForm(request.POST, instance=applicationServer)
        if form.is_valid():
            server = form.save(commit=False)
            save_server(server)
            return redirect('details-view', pk=applicationServer.pk)
    else:
        form = ServerForm(instance=applicationServer)

    #if form is invalid or GET request
    args = {'form': form}
    return render(request, 'application_server_edit.html', args)


def details_application_server(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    return render(request, 'application_server_details.html', {'applicationServer': applicationServer})
