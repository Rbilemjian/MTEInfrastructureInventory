from django.shortcuts import render, redirect, get_object_or_404, HttpResponse


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ApplicationServer, FilterProfile, AdditionalIPs, HOST_FIELDS, DHCPMember, CloudInformation
from .models import SNMP3Credential, SNMPCredential, ExtensibleAttribute, DiscoveredData, IPv4HostAddress
from .models import IPv6HostAddress, DomainNameServer, LogicFilterRule, Alias, CliCredential, DHCPOption
from .forms import ServerForm, ServerImportForm, ServerSearchForm, FilterProfileForm, AdditionalIPForm, InfobloxImportForm
import xlrd
import requests
import json
import urllib3

#helper functions


def get_str_date(row, column, worksheet, book):
    date_tuple = xlrd.xldate.xldate_as_tuple(worksheet.cell_value(row, column), book.datemode)
    return str(date_tuple[0]) + "-" + str(date_tuple[1]) + "-" + str(date_tuple[2])


def sanitize_server(server, request):
    #correcting fields
    fields = ApplicationServer._meta.get_all_field_names()
    for field in fields:
        if hasattr(server, field):
            if getattr(server, field) == "":
                    setattr(server, field, None)
    if server.is_virtual_machine == "TBD":
        server.is_virtual_machine = None
    if server.environment == "TBD":
        server.environment = None
    server.published_by = request.user
    server.published_date = timezone.now()

    #checking if exists already in database
    if ApplicationServer.objects.filter(
        service=server.service,
        hostname=server.hostname,
        primary_application=server.primary_application,
        is_virtual_machine=server.is_virtual_machine,
        environment=server.environment,
        location=server.location,
        data_center=server.data_center,
        operating_system=server.operating_system,
        rack=server.rack,
        model=server.model,
        serial_number=server.serial_number,
        comment=server.comment,
        network=server.network,
        private_ip=server.private_ip,
        dmz_public_ip=server.dmz_public_ip,
        virtual_ip=server.virtual_ip,
        nat_ip=server.nat_ip,
        ilo_or_cimc=server.ilo_or_cimc,
        nic_mac_address=server.nic_mac_address,
        switch=server.switch,
        port=server.port,
        base_warranty=server.base_warranty,
    ).exists():
        return {'exists_in_database': True, 'server': server}
    return {'exists_in_database': False, 'server': server}


def update_server(server, request):
    fields = ApplicationServer._meta.get_all_field_names()
    for field in fields:
        if hasattr(server, field):
            if getattr(server, field) == "":
                    setattr(server, field, None)
    if server.is_virtual_machine == "TBD":
        server.is_virtual_machine = 0
    if server.environment == "TBD":
        server.environment = "Prod"
    server.last_edited = timezone.now()
    server.last_editor = request.user
    server.save()
    return server


def filter_servers(data):
    search_result = ApplicationServer.objects.all()

    if data.get('service') != '':
        search_result = search_result.filter(service__icontains=data.get('service'))

    if data.get('hostname') != '':
        search_result = search_result.filter(hostname__icontains=data.get('hostname'))

    if data.get('primary_application') != '':
        search_result = search_result.filter(primary_application__icontains=data.get('primary_application'))

    if data.get('is_virtual_machine') != '':
        search_result = search_result.filter(is_virtual_machine=data.get('is_virtual_machine'))

    if data.get('environment') != '':
        search_result = search_result.filter(environment=data.get('environment'))

    if data.get('location') != '':
        search_result = search_result.filter(location__icontains=data.get('location'))

    if data.get('data_center') != '':
        search_result = search_result.filter(data_center__icontains=data.get('data_center'))

    if data.get('operating_system') != '':
        search_result = search_result.filter(operating_system__icontains=data.get('operating_system'))

    if data.get('rack') != '':
        search_result = search_result.filter(rack__icontains=data.get('rack'))

    if data.get('model') != '':
        search_result = search_result.filter(model__icontains=data.get('model'))

    if data.get('serial_number') != '':
        search_result = search_result.filter(serial_number__icontains=data.get('serial_number'))

    if data.get('network') != '':
        search_result = search_result.filter(network__icontains=data.get('network'))

    if data.get('private_ip') != '':
        search_result = search_result.filter(private_ip__icontains=data.get('private_ip'))

    if data.get('dmz_public_ip') != '':
        search_result = search_result.filter(dmz_public_ip__icontains=data.get('dmz_public_ip'))

    if data.get('virtual_ip') != '':
        search_result = search_result.filter(virtual_ip__icontains=data.get('virtual_ip'))

    if data.get('nat_ip') != '':
        search_result = search_result.filter(nat_ip__icontains=data.get('nat_ip'))

    if data.get('ilo_or_cimc') != '':
        search_result = search_result.filter(ilo_or_cimc__icontains=data.get('ilo_or_cimc'))

    if data.get('nic_mac_address') != '':
        search_result = search_result.filter(nic_mac_address__icontains=data.get('nic_mac_address'))

    if data.get('switch') != '':
        search_result = search_result.filter(switch__icontains=data.get('switch'))

    if data.get('port') != '':
        search_result = search_result.filter(port__icontains=data.get('port'))

    if data.get('purchase_order') != '':
        search_result = search_result.filter(purchase_order__icontains=data.get('purchase_order'))

    return search_result


def filter_from_profile(filter_profile):
    filter_result = ApplicationServer.objects.all()
    if filter_profile.all_fields is not None:
        fields = filter_profile._meta.get_all_field_names()
        results = ApplicationServer.objects.none()
        for field in fields:
            if field == "user_id" or field == "user" or field == "profile_name" or field == "all_fields":
                continue
            lookup = "%s__icontains" % field
            query = {lookup: filter_profile.all_fields}
            results = results | ApplicationServer.objects.filter(**query)
        filter_result = results


    if filter_profile.service is not None:
        filter_result = filter_result.filter(service__icontains=filter_profile.service)

    if filter_profile.hostname is not None:
        filter_result = filter_result.filter(hostname__icontains=filter_profile.hostname)

    if filter_profile.primary_application is not None:
        filter_result = filter_result.filter(primary_application__icontains=filter_profile.primary_application)

    if filter_profile.is_virtual_machine is not None:
        filter_result = filter_result.filter(is_virtual_machine=filter_profile.is_virtual_machine)

    if filter_profile.environment is not None:
        filter_result = filter_result.filter(environment=filter_profile.environment)

    if filter_profile.location is not None:
        filter_result = filter_result.filter(location__icontains=filter_profile.location)

    if filter_profile.data_center is not None:
        filter_result = filter_result.filter(data_center__icontains=filter_profile.data_center)

    if filter_profile.operating_system is not None:
        filter_result = filter_result.filter(operating_system__icontains=filter_profile.operating_system)

    if filter_profile.rack is not None:
        filter_result = filter_result.filter(rack__icontains=filter_profile.rack)

    if filter_profile.model is not None:
        filter_result = filter_result.filter(model__icontains=filter_profile.model)

    if filter_profile.serial_number is not None:
        filter_result = filter_result.filter(serial_number__icontains=filter_profile.serial_number)

    if filter_profile.network is not None:
        filter_result = filter_result.filter(network__icontains=filter_profile.network)

    if filter_profile.private_ip is not None:
        filter_result = filter_result.filter(private_ip__icontains=filter_profile.private_ip)

    if filter_profile.dmz_public_ip is not None:
        filter_result = filter_result.filter(dmz_public_ip__icontains=filter_profile.dmz_public_ip)

    if filter_profile.virtual_ip is not None:
        filter_result = filter_result.filter(virtual_ip__icontains=filter_profile.virtual_ip)

    if filter_profile.nat_ip is not None:
        filter_result = filter_result.filter(nat_ip__icontains=filter_profile.nat_ip)

    if filter_profile.ilo_or_cimc is not None:
        filter_result = filter_result.filter(ilo_or_cimc__icontains=filter_profile.ilo_or_cimc)

    if filter_profile.nic_mac_address is not None:
        filter_result = filter_result.filter(nic_mac_address__icontains=filter_profile.nic_mac_address)

    if filter_profile.switch is not None:
        filter_result = filter_result.filter(switch__icontains=filter_profile.switch)

    if filter_profile.port is not None:
        filter_result = filter_result.filter(port__icontains=filter_profile.port)

    if filter_profile.purchase_order is not None:
        filter_result = filter_result.filter(purchase_order__icontains=filter_profile.purchase_order)


    return filter_result


def prep_filter_for_save(filter):
    # setting any empty field to have a null value
    fields = FilterProfile._meta.get_all_field_names()
    for field in fields:
        if getattr(filter, field) == "":
            if FilterProfile._meta.get_field(field).null:
                setattr(filter, field, None)
    return filter


#view functions


@login_required
def view_application_servers(request):
    application_servers = ApplicationServer.objects.filter(visible=True)
    additional_ips = AdditionalIPs.objects.all()
    return render(request, 'application_server_list.html', {'applicationServers': application_servers, 'additionalIPs': additional_ips})


@login_required
def create_application_server_form(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            sanitization_result = sanitize_server(server, request)
            server = sanitization_result['server']
            server.save()
            return redirect('/infrastructureinventory/applicationserver/')
    else:
        form = ServerForm()
    # if form invalid or GET request
    return render(request, 'application_server_form.html', {"form": form})


@login_required
def import_application_server(request):
    if request.method == 'POST':
        form = ServerImportForm(request.POST, request.FILES)
        if form.is_valid():
            ApplicationServer.objects.filter(visible=False).delete()
            file = request.FILES['file']
            book = xlrd.open_workbook(file_contents=file.read())
            worksheet = book.sheet_by_name('Sheet1')
            num_rows = worksheet.nrows - 1
            for i in range(1, num_rows + 1):

                app_server = ApplicationServer()

                app_server.service = worksheet.cell_value(i, 0).strip()
                app_server.primary_application = worksheet.cell_value(i, 1).strip()
                app_server.hostname = worksheet.cell_value(i, 2).strip()
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

                if worksheet.cell_value(i, 29) == "":
                    app_server.comment = None
                else:
                    app_server.comment = worksheet.cell_value(i, 29)

                sanitization_result = sanitize_server(app_server, request)
                if sanitization_result['exists_in_database'] is False:
                    app_server = sanitization_result['server']
                    app_server.visible = False
                    app_server.save()

            return redirect('/infrastructureinventory/applicationserver/import/confirm')

            #return redirect('/infrastructureinventory/applicationserver')
    else:
        form = ServerImportForm()
    # if form invalid or GET request
    return render(request, 'application_server_import.html', {"form": form})

@login_required()
def confirm_import_application_server(request):
    parsed_servers = ApplicationServer.objects.filter(visible=False)
    if request.method == "POST":
        for ps in parsed_servers:
            ps.visible=True
            ps.save()
        return redirect('/infrastructureinventory/applicationserver')
    else:
        return render(request, 'application_server_import_confirm.html', {"applicationServers": parsed_servers})



@login_required()
def edit_application_server(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    if request.method == "POST":
        form = ServerForm(request.POST, instance=applicationServer)
        if form.is_valid():
            server = form.save(commit=False)
            update_server(server, request)
            return redirect('details-view', pk=server.pk)
    else:
        form = ServerForm(instance=applicationServer)

    #if form is invalid or GET request
    args = {'form': form}
    return render(request, 'application_server_edit.html', args)


@login_required()
def details_application_server(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    IPs = AdditionalIPs.objects.filter(application_server_id=pk)
    if request.method == "POST":
        form = AdditionalIPForm(request.POST)
        if form.is_valid():
            ip = form.save(commit=False)
            ip.application_server_id = pk
            ip.save()
            form = AdditionalIPForm()
    else:
        form = AdditionalIPForm()
    return render(request, 'application_server_details.html', {'applicationServer': applicationServer, "IPs": IPs, "form": form})


@login_required()
def delete_application_server(request, pk):
    application_server = get_object_or_404(ApplicationServer, pk=pk)
    AdditionalIPs.objects.filter(application_server_id=application_server.id).delete()
    application_server.delete()
    return redirect('/infrastructureinventory/applicationserver/')


@login_required()
def search_application_server(request):
    if request.method == "POST":
        form = ServerSearchForm(request.POST)
        if form.is_valid:
            search_result = filter_servers(form.data)
            search_result = search_result.filter(visible=True)
            return render(request, 'application_server_search_result.html', {'applicationServers': search_result})
    else:
        form = ServerSearchForm()
    return render(request, 'application_server_search_form.html', {'form': form})


@login_required()
def application_server_delete_confirm(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    return render(request, 'application_server_delete_confirm.html', {'applicationServer': applicationServer})


@login_required()
def filter_profile(request):
    filterProfiles = FilterProfile.objects.all()
    return render(request, 'filter_profiles.html', {"filterProfiles": filterProfiles})


@login_required()
def filter_profile_form(request):
    if request.method == "POST":
        form = FilterProfileForm(request.POST, instance=FilterProfile())
        if form.is_valid():
            filter = form.save(commit=False)
            filter = prep_filter_for_save(filter)
            filter.save()
            return redirect('/infrastructureinventory/applicationserver/filterprofile')
    else:
        form = FilterProfileForm()
    return render(request, 'filter_profile_form.html', {'form': form})


@login_required()
def filtered_list(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    filter_result = filter_from_profile(filterProfile)
    filter_result = filter_result.filter(visible=True)
    return render(request, 'filtered_list.html', {"filterProfile": filterProfile, "applicationServers": filter_result})


@login_required()
def filter_profile_delete_confirm(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    return render(request, 'filter_profile_delete_confirm.html', {"filterProfile": filterProfile})


@login_required()
def filter_profile_delete(request, pk):
    get_object_or_404(FilterProfile, pk=pk).delete()
    return redirect('/infrastructureinventory/applicationserver/filterprofile')


@login_required()
def filter_profile_edit(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    if request.method == "POST":
        form = FilterProfileForm(request.POST, instance=filterProfile)
        if form.is_valid():
            filter = form.save(commit=False)
            filter = prep_filter_for_save(filter)
            filter.save()
            return redirect('filter-profile-view')
    else:
        form = FilterProfileForm(instance=filterProfile)
    args = {"form": form, "filterProfile": filterProfile}
    return render(request, "filter_profile_edit.html", args)

#InfoBlox views



