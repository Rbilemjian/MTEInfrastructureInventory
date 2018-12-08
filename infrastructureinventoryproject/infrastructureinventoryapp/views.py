from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . import models
from .models import ApplicationServer, FilterProfile, HOST_FIELDS, DHCPMember, CloudInformation, DISCOVERED_DATA_FIELDS
from .models import SNMP3Credential, SNMPCredential, ExtensibleAttribute, DiscoveredData, IPv4HostAddress
from .models import IPv6HostAddress, DomainNameServer, LogicFilterRule, Alias, CliCredential, DHCPOption, VisibleColumns
from .models import HOST_FIELDS, AWSRTE53RecordInfo
from .forms import InfobloxImportForm, VisibleColumnForm, FilterProfileForm, AdvancedSearchForm
import xlrd
import requests
import json
import urllib3

#helper functions


# def get_str_date(row, column, worksheet, book):
#     date_tuple = xlrd.xldate.xldate_as_tuple(worksheet.cell_value(row, column), book.datemode)
#     return str(date_tuple[0]) + "-" + str(date_tuple[1]) + "-" + str(date_tuple[2])
#
#
# def sanitize_server(server, request):
#     #correcting fields
#     fields = ApplicationServer._meta.get_all_field_names()
#     for field in fields:
#         if hasattr(server, field):
#             if getattr(server, field) == "":
#                     setattr(server, field, None)
#     if server.is_virtual_machine == "TBD":
#         server.is_virtual_machine = None
#     if server.environment == "TBD":
#         server.environment = None
#     server.published_by = request.user
#     server.published_date = timezone.now()
#
#     #checking if exists already in database
#     if ApplicationServer.objects.filter(
#         service=server.service,
#         hostname=server.hostname,
#         primary_application=server.primary_application,
#         is_virtual_machine=server.is_virtual_machine,
#         environment=server.environment,
#         location=server.location,
#         data_center=server.data_center,
#         operating_system=server.operating_system,
#         rack=server.rack,
#         model=server.model,
#         serial_number=server.serial_number,
#         comment=server.comment,
#         network=server.network,
#         private_ip=server.private_ip,
#         dmz_public_ip=server.dmz_public_ip,
#         virtual_ip=server.virtual_ip,
#         nat_ip=server.nat_ip,
#         ilo_or_cimc=server.ilo_or_cimc,
#         nic_mac_address=server.nic_mac_address,
#         switch=server.switch,
#         port=server.port,
#         base_warranty=server.base_warranty,
#     ).exists():
#         return {'exists_in_database': True, 'server': server}
#     return {'exists_in_database': False, 'server': server}
#
#
# def update_server(server, request):
#     fields = ApplicationServer._meta.get_all_field_names()
#     for field in fields:
#         if hasattr(server, field):
#             if getattr(server, field) == "":
#                     setattr(server, field, None)
#     if server.is_virtual_machine == "TBD":
#         server.is_virtual_machine = 0
#     if server.environment == "TBD":
#         server.environment = "Prod"
#     server.last_edited = timezone.now()
#     server.last_editor = request.user
#     server.save()
#     return server
#
#

#If a user searches for an ipv4address, this function looks at ipv4hostaddresses and finds the applicationserver
#that is associated with the ivp4hostaddress that has that IP address, if such an appliationServer exists
#as well as any record applicationservers that have that ip address
def get_ipv4_application_servers(ipv4addr):
    ipv4s = IPv4HostAddress.objects.filter(visible=True)
    appServers = ApplicationServer.objects.filter(visible=True)
    retServers = ApplicationServer.objects.none()
    if ipv4s.filter(ipv4addr__startswith=ipv4addr).count() > 0:
        ipv4s = ipv4s.filter(ipv4addr__startswith=ipv4addr)
        for ipv4 in ipv4s:
            as_id = ipv4.application_server.id
            retServers = retServers | appServers.filter(id=as_id)
    retServers = retServers | appServers.filter(ipv4addr__startswith=ipv4addr)
    return retServers


def get_ipv6_application_servers(ipv6addr):
    retServers = ApplicationServer.objects.none()
    if IPv6HostAddress.objects.filter(visible=True).filter(ipv6addr__istartswith=ipv6addr).count() > 0:
        ipv6s = IPv6HostAddress.objects.filter(visible=True).filter(ipv6addr__startswith=ipv6addr)
        for ipv6 in ipv6s:
            as_id = ipv6.application_server.id
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=as_id)
    return retServers


def get_alias_application_servers(alias):
    retServers = ApplicationServer.objects.none()
    if Alias.objects.filter(visible=True).filter(alias__icontains=alias).count() > 0:
        aliases = Alias.objects.filter(visible=True).filter(alias__icontains=alias)
        for alias in aliases:
            as_id = alias.application_server.id
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=as_id)
    return retServers


def get_extensible_attribute_application_servers(extensible_attribute_value):
    retServers = ApplicationServer.objects.none()
    if ExtensibleAttribute.objects.filter(visible=True).filter(attribute_value__icontains=extensible_attribute_value).count() > 0:
        ext_attrs = ExtensibleAttribute.objects.filter(visible=True).filter(attribute_value__icontains=extensible_attribute_value)
        for ext_attr in ext_attrs:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ext_attr.application_server.id)
    return retServers


def get_discovered_data_application_servers(discovered_data_value):
    retServers = ApplicationServer.objects.none()
    ipv4s = IPv4HostAddress.objects.none()
    ipv6s = IPv6HostAddress.objects.none()

    dds = DiscoveredData.objects.filter(visible=True)
    dds_of_interest = DiscoveredData.objects.none()
    fields = models.DISCOVERED_DATA_FIELDS
    icontains = "__icontains"

    for field in fields:
        field = field[0]
        filter = field + icontains
        dds_of_interest = dds_of_interest | dds.filter(**{filter: discovered_data_value})

    if dds_of_interest.count() > 0:
        for dd in dds_of_interest:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(discovered_data=dd)
            ipv4s = ipv4s | IPv4HostAddress.objects.filter(visible=True).filter(discovered_data=dd)
            ipv6s = ipv6s | IPv6HostAddress.objects.filter(visible=True).filter(discovered_data=dd)

    if ipv4s.count() > 0:
        for ipv4 in ipv4s:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv4.application_server.id)

    if ipv6s.count() > 0:
        for ipv6 in ipv6s:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv6.application_server.id)

    return retServers


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


def filter_by_cloud_information(field, value):
    appServers = ApplicationServer.objects.none()
    field = remove_prefix(field, "ci_")
    field = remove_prefix(field, "delegated_member_")


    filter = field + "__icontains"

    cFields = CloudInformation._meta.get_all_field_names()
    dFields = DHCPMember._meta.get_all_field_names()

    if field in cFields:
        cis = CloudInformation.objects.filter(**{filter: value}).filter(visible=True)
        if cis.count() > 0:
            cis = CloudInformation.objects.filter(**{filter:value}).filter(visible=True)
            for ci in cis:
                appServers = appServers | ApplicationServer.objects.filter(cloud_information=ci).filter(visible=True)

    elif field in dFields:
        cloudInfos = CloudInformation.objects.filter(visible=True)
        dms = DHCPMember.objects.filter(**{filter: value})
        if dms.count() > 0:
            dms = DHCPMember.objects.filter(**{filter:value})
            for dm in dms:
                cloudInfos = cloudInfos | CloudInformation.objects.filter(delegated_member=dm).filter(visible=True)
            for cloudInfo in cloudInfos:
                appServers = appServers | ApplicationServer.objects.filter(cloud_information=cloudInfo).filter(visible=True)

    return appServers


def filter_by_snmp3_credential_information(field, value):
    appServers = ApplicationServer.objects.none()

    field = remove_prefix(field, "snmp3_")
    fields = SNMP3Credential._meta.get_all_field_names()

    filter = field + "__icontains"

    if field in fields:
        snmp3s = SNMP3Credential.objects.filter(**{filter: value}).filter(visible=True)
        if snmp3s.count() > 0:
            for snmp3 in snmp3s:
                appServers = appServers | ApplicationServer.objects.filter(visible=True).filter(snmp3_credential=snmp3)
    return appServers



def filter_by_snmp_credential_information(field, value):
    appServers = ApplicationServer.objects.none()

    field = remove_prefix(field, "snmp_")
    fields = SNMPCredential._meta.get_all_field_names()

    filter = field + "__icontains"

    if field in fields:
        snmps = SNMPCredential.objects.filter(**{filter: value}).filter(visible=True)
        if snmps.count() > 0:
            for snmp in snmps:
                appServers = appServers | ApplicationServer.objects.filter(visible=True).filter(snmp_credential=snmp)
    return appServers



def filter_by_aws_rte53_record_information(field, value):
    appServers = ApplicationServer.objects.none()

    field = remove_prefix(field, "aws_")
    fields = AWSRTE53RecordInfo._meta.get_all_field_names()

    filter = field + "__icontains"
    print(field)
    if field in fields:
        awss = AWSRTE53RecordInfo.objects.filter(**{filter: value}).filter(visible=True)
        if awss.count() > 0:
            for aws in awss:
                appServers = appServers | ApplicationServer.objects.filter(visible=True).filter(aws_rte53_record_info=aws)
    return appServers


def filter_by_discovered_data(field, value):

    field = remove_prefix(field, "dd_")

    ipv4s = IPv4HostAddress.objects.none()
    ipv6s = IPv6HostAddress.objects.none()

    retServers = ApplicationServer.objects.none()
    filter = field + "__icontains"
    dds = DiscoveredData.objects.filter(visible=True).filter(**{filter: value})
    for dd in dds:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(discovered_data=dd)
        ipv4s = ipv4s | IPv4HostAddress.objects.filter(visible=True).filter(discovered_data=dd)
        ipv6s = ipv6s | IPv6HostAddress.objects.filter(visible=True).filter(discovered_data=dd)

    if ipv4s.count() > 0:
        for ipv4 in ipv4s:
            retServers = retServers| ApplicationServer.objects.filter(visible=True).filter(id=ipv4.application_server.id)
    if ipv6s.count() > 0:
        for ipv6 in ipv6s:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv6.application_server.id)
    return retServers




def filter_servers(filterProfile):
    fields = FilterProfile._meta.get_all_field_names()
    if filterProfile.all_fields is not None:
        results = ApplicationServer.objects.none()
        for field in fields:
            if field == "id" or field == "profile_name" or field == "all_fields" or field == "ipv6addr" or field == "alias" or field == "extensible_attribute_value" or field == "discovered_data": continue
            lookup = "%s__icontains" % field
            query = {lookup: filterProfile.all_fields}
            results = results | ApplicationServer.objects.filter(**query).filter(visible=True)
        results = results | get_ipv4_application_servers(filterProfile.all_fields)
        results = results | get_ipv6_application_servers(filterProfile.all_fields)
        results = results | get_alias_application_servers(filterProfile.all_fields)
        results = results | get_extensible_attribute_application_servers(filterProfile.all_fields)
        results = results | get_discovered_data_application_servers(filterProfile.all_fields)
        search_result = results

    else:
        search_result = ApplicationServer.objects.filter(visible=True)


    if filterProfile.alias is not None:
        search_result = search_result & get_alias_application_servers(filterProfile.alias)
    if filterProfile.extensible_attribute_value is not None:
        search_result = search_result & get_extensible_attribute_application_servers(filterProfile.extensible_attribute_value)

    for field in fields:
        if field == "id" or field == "profile_name" or field == "all_fields" or field == "ipv6addr" or field == "ipv4addr" or field == "alias" or field == "extensible_attribute_value" or field == "discovered_data": continue
        if hasattr(filterProfile, field) and getattr(filterProfile, field) is not None:
            value = getattr(filterProfile, field)

            #Checking if field is in a model other than applicationserver
            if field.startswith("ci_"):
                search_result = search_result & filter_by_cloud_information(field, value)
            elif field.startswith("snmp3_"):
                search_result = search_result & filter_by_snmp3_credential_information(field, value)
            elif field.startswith("snmp_"):
                search_result = search_result & filter_by_snmp_credential_information(field, value)
            elif field.startswith("aws_"):
                search_result = search_result & filter_by_aws_rte53_record_information(field, value)
            elif field.startswith("dd_"):
                search_result = search_result & filter_by_discovered_data(field, value)
            else:
                filter = field + "__icontains"
                search_result = search_result.filter(**{filter: value})
            print(field)
            print(len(search_result))
    return search_result
#
#
# def filter_from_profile(filter_profile):
#     filter_result = ApplicationServer.objects.all()
#     if filter_profile.all_fields is not None:
#         fields = filter_profile._meta.get_all_field_names()
#         results = ApplicationServer.objects.none()
#         for field in fields:
#             if field == "user_id" or field == "user" or field == "profile_name" or field == "all_fields":
#                 continue
#             lookup = "%s__icontains" % field
#             query = {lookup: filter_profile.all_fields}
#             results = results | ApplicationServer.objects.filter(**query)
#         filter_result = results
#
#
#     if filter_profile.service is not None:
#         filter_result = filter_result.filter(service__icontains=filter_profile.service)
#
#     if filter_profile.hostname is not None:
#         filter_result = filter_result.filter(hostname__icontains=filter_profile.hostname)
#
#     if filter_profile.primary_application is not None:
#         filter_result = filter_result.filter(primary_application__icontains=filter_profile.primary_application)
#
#     if filter_profile.is_virtual_machine is not None:
#         filter_result = filter_result.filter(is_virtual_machine=filter_profile.is_virtual_machine)
#
#     if filter_profile.environment is not None:
#         filter_result = filter_result.filter(environment=filter_profile.environment)
#
#     if filter_profile.location is not None:
#         filter_result = filter_result.filter(location__icontains=filter_profile.location)
#
#     if filter_profile.data_center is not None:
#         filter_result = filter_result.filter(data_center__icontains=filter_profile.data_center)
#
#     if filter_profile.operating_system is not None:
#         filter_result = filter_result.filter(operating_system__icontains=filter_profile.operating_system)
#
#     if filter_profile.rack is not None:
#         filter_result = filter_result.filter(rack__icontains=filter_profile.rack)
#
#     if filter_profile.model is not None:
#         filter_result = filter_result.filter(model__icontains=filter_profile.model)
#
#     if filter_profile.serial_number is not None:
#         filter_result = filter_result.filter(serial_number__icontains=filter_profile.serial_number)
#
#     if filter_profile.network is not None:
#         filter_result = filter_result.filter(network__icontains=filter_profile.network)
#
#     if filter_profile.private_ip is not None:
#         filter_result = filter_result.filter(private_ip__icontains=filter_profile.private_ip)
#
#     if filter_profile.dmz_public_ip is not None:
#         filter_result = filter_result.filter(dmz_public_ip__icontains=filter_profile.dmz_public_ip)
#
#     if filter_profile.virtual_ip is not None:
#         filter_result = filter_result.filter(virtual_ip__icontains=filter_profile.virtual_ip)
#
#     if filter_profile.nat_ip is not None:
#         filter_result = filter_result.filter(nat_ip__icontains=filter_profile.nat_ip)
#
#     if filter_profile.ilo_or_cimc is not None:
#         filter_result = filter_result.filter(ilo_or_cimc__icontains=filter_profile.ilo_or_cimc)
#
#     if filter_profile.nic_mac_address is not None:
#         filter_result = filter_result.filter(nic_mac_address__icontains=filter_profile.nic_mac_address)
#
#     if filter_profile.switch is not None:
#         filter_result = filter_result.filter(switch__icontains=filter_profile.switch)
#
#     if filter_profile.port is not None:
#         filter_result = filter_result.filter(port__icontains=filter_profile.port)
#
#     if filter_profile.purchase_order is not None:
#         filter_result = filter_result.filter(purchase_order__icontains=filter_profile.purchase_order)
#
#
#     return filter_result
#
#

#
#
# @login_required
# def create_application_server_form(request):
#     if request.method == 'POST':
#         form = ServerForm(request.POST)
#         if form.is_valid():
#             server = form.save(commit=False)
#             sanitization_result = sanitize_server(server, request)
#             server = sanitization_result['server']
#             server.save()
#             return redirect('/infrastructureinventory/applicationserver/')
#     else:
#         form = ServerForm()
#     # if form invalid or GET request
#     return render(request, 'application_server_form.html', {"form": form})
#
#
# @login_required
# def import_application_server(request):
#     if request.method == 'POST':
#         form = ServerImportForm(request.POST, request.FILES)
#         if form.is_valid():
#             ApplicationServer.objects.filter(visible=False).delete()
#             file = request.FILES['file']
#             book = xlrd.open_workbook(file_contents=file.read())
#             worksheet = book.sheet_by_name('Sheet1')
#             num_rows = worksheet.nrows - 1
#             for i in range(1, num_rows + 1):
#
#                 app_server = ApplicationServer()
#
#                 app_server.service = worksheet.cell_value(i, 0).strip()
#                 app_server.primary_application = worksheet.cell_value(i, 1).strip()
#                 app_server.hostname = worksheet.cell_value(i, 2).strip()
#                 app_server.is_virtual_machine = worksheet.cell_value(i, 3)
#                 app_server.environment = worksheet.cell_value(i, 4).strip()
#                 app_server.location = worksheet.cell_value(i, 5).strip()
#                 app_server.data_center = str(worksheet.cell_value(i, 6)).strip()
#                 app_server.operating_system = worksheet.cell_value(i, 8).strip()
#                 app_server.model = worksheet.cell_value(i, 9).strip()
#                 app_server.serial_number = worksheet.cell_value(i, 10).strip()
#                 app_server.network = worksheet.cell_value(i, 11).strip()
#
#                 if type(worksheet.cell_value(i, 7)) is float:
#                     app_server.rack = str(int(worksheet.cell_value(i, 7)))
#                 else:
#                     app_server.rack = str(worksheet.cell_value(i, 7)).strip()
#
#                 app_server.private_ip = worksheet.cell_value(i, 12)
#                 app_server.dmz_public_ip = worksheet.cell_value(i, 13)
#                 app_server.virtual_ip = worksheet.cell_value(i, 14)
#                 app_server.nat_ip = worksheet.cell_value(i, 15)
#                 app_server.ilo_or_cimc = worksheet.cell_value(i, 16).strip()
#                 app_server.nic_mac_address = worksheet.cell_value(i, 17).strip()
#                 app_server.switch = worksheet.cell_value(i, 18).strip()
#                 app_server.port = worksheet.cell_value(i, 19).strip()
#
#                 if type(worksheet.cell_value(i, 20)) is float:
#                     app_server.purchase_order = str(int(worksheet.cell_value(i, 20)))
#                 else:
#                     app_server.purchase_order = worksheet.cell_value(i, 20)
#
#                 if worksheet.cell_value(i, 21) == "":
#                     app_server.start_date = None
#                 else:
#                     app_server.start_date = get_str_date(i, 21, worksheet, book)
#
#                 if worksheet.cell_value(i, 22) == "":
#                     app_server.next_hardware_support_date = None
#                 else:
#                     app_server.next_hardware_support_date = get_str_date(i, 22, worksheet, book)
#
#                 if worksheet.cell_value(i, 23) == "":
#                     app_server.base_warranty = None
#                 else:
#                     app_server.base_warranty = get_str_date(i, 23, worksheet, book)
#
#                 app_server.cpu = worksheet.cell_value(i, 24)
#                 app_server.ram = worksheet.cell_value(i, 25)
#                 app_server.c_drive = worksheet.cell_value(i, 26)
#                 app_server.d_drive = worksheet.cell_value(i, 27)
#                 app_server.e_drive = worksheet.cell_value(i, 28)
#
#                 if worksheet.cell_value(i, 29) == "":
#                     app_server.comment = None
#                 else:
#                     app_server.comment = worksheet.cell_value(i, 29)
#
#                 sanitization_result = sanitize_server(app_server, request)
#                 if sanitization_result['exists_in_database'] is False:
#                     app_server = sanitization_result['server']
#                     app_server.visible = False
#                     app_server.save()
#
#             return redirect('/infrastructureinventory/applicationserver/import/confirm')
#
#             #return redirect('/infrastructureinventory/applicationserver')
#     else:
#         form = ServerImportForm()
#     # if form invalid or GET request
#     return render(request, 'application_server_import.html', {"form": form})
#
# @login_required()
# def confirm_import_application_server(request):
#     parsed_servers = ApplicationServer.objects.filter(visible=False)
#     if request.method == "POST":
#         for ps in parsed_servers:
#             ps.visible=True
#             ps.save()
#         return redirect('/infrastructureinventory/applicationserver')
#     else:
#         return render(request, 'application_server_import_confirm.html', {"applicationServers": parsed_servers})
#
#
#
# @login_required()
# def edit_application_server(request, pk):
#     applicationServer = get_object_or_404(ApplicationServer, pk=pk)
#     if request.method == "POST":
#         form = ServerForm(request.POST, instance=applicationServer)
#         if form.is_valid():
#             server = form.save(commit=False)
#             update_server(server, request)
#             return redirect('details-view', pk=server.pk)
#     else:
#         form = ServerForm(instance=applicationServer)
#
#     #if form is invalid or GET request
#     args = {'form': form}
#     return render(request, 'application_server_edit.html', args)


def prep_filter_for_save(filter):
    # setting any empty field to have a null value
    fields = FilterProfile._meta.get_all_field_names()
    for field in fields:
        if getattr(filter, field) == "":
            if FilterProfile._meta.get_field(field).null:
                setattr(filter, field, None)
    return filter

def get_visible_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.APPLICATION_SERVER_FIELDS
    retList = []

    for field in fieldList:
        if hasattr(visible_columns, field[0]):
            if getattr(visible_columns, field[0]) is True:
                retList.append(field)

    return retList



#View Functions



@login_required
def view_application_servers(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    application_servers = ApplicationServer.objects.filter(visible=True)
    if request.method == 'POST':
        form = VisibleColumnForm(request.POST)
        if form.is_valid():
            if VisibleColumns.objects.filter(user=request.user).count() > 0:
                VisibleColumns.objects.filter(user=request.user).delete()
            visible_columns = form.save(commit=False)
            visible_columns.user = request.user
            visible_columns.save()
        else:
            form = VisibleColumnForm()

    else:
        form = VisibleColumnForm(instance=VisibleColumns.objects.filter(user=request.user).get())

    fields = get_visible_fields(request)

    args = {'applicationServers': application_servers, 'fields': fields, 'form': form}
    return render(request, 'application_server_list.html', args)


@login_required()
def details_application_server(request, pk):
    applicationServer = ApplicationServer.objects.filter(pk=pk, visible=True)

    if len(applicationServer) == 0:
        return HttpResponseNotFound("Application server not found in database.")

    applicationServer = applicationServer.get()
    applicationServerFieldList = models.APPLICATION_SERVER_FIELDS

    ipv4HostAddresses = applicationServer.ipv4hostaddress_set.filter(visible=True)
    ipv4HostAddressFields = models.IPV4_FIELDS

    #Getting ipv4hostaddresses' one-to-many record field lists
    logicFilterRuleFields = models.LOGIC_FILTER_RULE_FIELDS
    DHCPOptionFields = models.DHCP_OPTION_FIELDS

    #Getting ipv6hostaddresses' one-to-many record field lists
    domainNameServerFields = models.DOMAIN_NAME_SERVER_FIELDS




    ipv6HostAddresses = applicationServer.ipv6hostaddress_set.filter(visible=True)
    ipv6HostAddressFields = models.IPV6_FIELDS


    extensibleAttributes = applicationServer.extensibleattribute_set.filter(visible=True)
    aliases = applicationServer.alias_set.filter(visible=True)
    cliCredentials = applicationServer.clicredential_set.filter(visible=True)

    #Getting one-to-one Field Lists
    discoveredFieldList = models.DISCOVERED_DATA_FIELDS
    cloudInformationFieldList = models.CLOUD_INFORMATION_FIELDS
    delegatedMemberFieldList = models.DHCP_MEMBER_FIELDS
    snmp3CredentialFieldList = models.SNMP3_CREDENTIAL_FIELDS
    snmpCredentialFieldList = models.SNMP_CREDENTIAL_FIELDS
    AWSRTE53RecordInfoFieldList = models.AWS_RTE53_RECORD_INFO_FIELDS

    args = {
        "applicationServer": applicationServer,
        "ipv4s": ipv4HostAddresses,
        "ipv6s": ipv6HostAddresses,
        "extattrs": extensibleAttributes,
        "aliases": aliases,
        "clicreds": cliCredentials,
        "applicationServerFieldList": applicationServerFieldList,
        "ipv4FieldList": ipv4HostAddressFields,
        "ipv6FieldList": ipv6HostAddressFields,
        "discoveredFieldList": discoveredFieldList,
        "cloudInformationFieldList": cloudInformationFieldList,
        "delegatedMemberFieldList": delegatedMemberFieldList,
        "snmp3CredentialFieldList": snmp3CredentialFieldList,
        "snmpCredentialFieldList": snmpCredentialFieldList,
        "AWSRTE53RecordInfoFieldList": AWSRTE53RecordInfoFieldList,
        "logicFilterRuleFields": logicFilterRuleFields,
        "DHCPOptionFields": DHCPOptionFields,
        "domainNameServerFields": domainNameServerFields
            }
    return render(request, 'application_server_details.html', args)
#
#
@login_required()
def delete_application_server(request, pk):
    application_server = get_object_or_404(ApplicationServer, pk=pk)
    application_server.deleteWithForeign()
    return redirect('/infrastructureinventory/applicationserver/')


@login_required()
def search_application_server(request):

    if request.method == "POST":
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            filterProfile = form.save(commit=False)
            prep_filter_for_save(filterProfile)
            search_result = filter_servers(filterProfile)
            fields = get_visible_fields(request)
            args = {'applicationServers': search_result, 'fields': fields}
            return render(request, 'filtered_list.html', args)
    else:
        form = AdvancedSearchForm()
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
        form = FilterProfileForm(request.POST)
        if form.is_valid():
            filter = form.save(commit=False)
            filter = prep_filter_for_save(filter)
            filter.save()
            return redirect('/infrastructureinventory/applicationserver/filterprofile')
    else:
        form = FilterProfileForm()
    return render(request, 'filter_profile_form.html', {'form': form})

#
@login_required()
def filtered_list(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    filter_result = filter_servers(filterProfile)
    fields = get_visible_fields(request)
    args = {'applicationServers': filter_result, 'fields': fields, "profileName": filterProfile.profile_name}
    return render(request, 'filtered_list.html', args)
#
#
@login_required()
def filter_profile_delete_confirm(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    return render(request, 'filter_profile_delete_confirm.html', {"filterProfile": filterProfile})
#
#
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
#
# #InfoBlox views
#
#
#
