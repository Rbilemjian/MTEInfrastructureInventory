from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from . import models
from .models import ApplicationServer, FilterProfile, DHCPMember, CloudInformation
from .models import SNMP3Credential, SNMPCredential, ExtensibleAttribute, DiscoveredData, IPv4HostAddress
from .models import IPv6HostAddress, DomainNameServer, LogicFilterRule, Alias, CliCredential, DHCPOption, VisibleColumns
from .models import AWSRTE53RecordInfo
from .forms import VisibleColumnForm, FilterProfileForm, AdvancedSearchForm
import json

#-------Filtering Helper Functions--------

#If a user searches for an ipv4address, this function looks at ipv4hostaddresses and finds the applicationserver
#that is associated with the ivp4hostaddress that has that IP address, if such an applicationServer exists
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


#If a user searches for an ipv6address, this function looks at ipv6hostaddresses and finds the applicationserver
#that is associated with the ipv6hostaddress that has that IP address, if such an applicationserver exists
#as well as any record applicationservers that have that IP address
def get_ipv6_application_servers(ipv6addr):
    retServers = ApplicationServer.objects.none()
    if IPv6HostAddress.objects.filter(visible=True).filter(ipv6addr__istartswith=ipv6addr).count() > 0:
        ipv6s = IPv6HostAddress.objects.filter(visible=True).filter(ipv6addr__startswith=ipv6addr)
        for ipv6 in ipv6s:
            as_id = ipv6.application_server.id
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=as_id)
    return retServers


#If a user searches for an alias, this function looks at applicationservers that are associated with that alias
def get_alias_application_servers(alias):
    retServers = ApplicationServer.objects.none()
    if Alias.objects.filter(visible=True).filter(alias__icontains=alias).count() > 0:
        aliases = Alias.objects.filter(visible=True).filter(alias__icontains=alias)
        for alias in aliases:
            as_id = alias.application_server.id
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=as_id)
    return retServers


#If a user searches for an extensible attribute value, this function looks at applicationservers that are associated
#with that extensible attribute value
def get_extensible_attribute_application_servers(extensible_attribute_value):
    retServers = ApplicationServer.objects.none()
    if ExtensibleAttribute.objects.filter(visible=True).filter(attribute_value__icontains=extensible_attribute_value).count() > 0:
        ext_attrs = ExtensibleAttribute.objects.filter(visible=True).filter(attribute_value__icontains=extensible_attribute_value)
        for ext_attr in ext_attrs:
            retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ext_attr.application_server.id)
    return retServers


#If a user searches for a discovered data value, this function looks at applicationservers that are associated with that
#discovered data value and returns them
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


#Removes a substring from the start of a string, if it exists at the start of the string
#If it does not exist, returns the original string
def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


#Returns only application servers that are associated with cloud information that contains the inputted field & value
def filter_by_cloud_information(field, value):
    appServers = ApplicationServer.objects.none()
    field = remove_prefix(field, "ci_")
    field = remove_prefix(field, "delegated_member_")

    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
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


#Returns only applicationservers that are associated with an snmp3 credential with the inputted field & value
def filter_by_snmp3_credential_information(field, value):
    appServers = ApplicationServer.objects.none()

    field = remove_prefix(field, "snmp3_")
    fields = SNMP3Credential._meta.get_all_field_names()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
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
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"

    if field in fields:
        snmps = SNMPCredential.objects.filter(**{filter: value}).filter(visible=True)
        if snmps.count() > 0:
            for snmp in snmps:
                appServers = appServers | ApplicationServer.objects.filter(visible=True).filter(snmp_credential=snmp)
    return appServers


#Returns only applicationservers that are associated with aws rte53 record info that has inputted field & value
def filter_by_aws_rte53_record_information(field, value):
    appServers = ApplicationServer.objects.none()

    field = remove_prefix(field, "aws_")
    fields = AWSRTE53RecordInfo._meta.get_all_field_names()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"
    if field in fields:
        awss = AWSRTE53RecordInfo.objects.filter(**{filter: value}).filter(visible=True)
        if awss.count() > 0:
            for aws in awss:
                appServers = appServers | ApplicationServer.objects.filter(visible=True).filter(aws_rte53_record_info=aws)
    return appServers


#Returns only applicationservers that are associated with discovered data that has inputted field and value
def filter_by_discovered_data(field, value):

    field = remove_prefix(field, "dd_")

    ipv4s = IPv4HostAddress.objects.none()
    ipv6s = IPv6HostAddress.objects.none()

    retServers = ApplicationServer.objects.none()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
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


#Returns only applicationservers that are associated with an ipv4 host address that has inputted field and value
def filter_by_ipv4_host_address(field, value):

    field = remove_prefix(field, "ipv4_")

    retServers = ApplicationServer.objects.none()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"
    ipv4s = IPv4HostAddress.objects.filter(visible=True).filter(**{filter: value})

    for ipv4 in ipv4s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv4.application_server.id)
    return retServers


#Returns only applicationservers that are associated with an ipv6 host address that has inputted field and value
def filter_by_ipv6_host_address(field, value):

    field = remove_prefix(field, "ipv6_")

    retServers = ApplicationServer.objects.none()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"
    ipv6s = IPv6HostAddress.objects.filter(visible=True).filter(**{filter: value})

    for ipv6 in ipv6s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv6.application_server.id)
    return retServers


#Returns only applicationservers that are associated with an ipv4 host address which has
#a filter logic rule with the given field and value
def filter_by_logic_filter_rule(field, value):

    field = remove_prefix(field, "lfr_")
    retServers = ApplicationServer.objects.none()
    ipv4s = IPv4HostAddress.objects.none()
    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"
    lfrs = LogicFilterRule.objects.filter(visible=True).filter(**{filter: value})

    for lfr in lfrs:
        ipv4s = ipv4s | IPv4HostAddress.objects.filter(visible=True).filter(id=lfr.ipv4_host_address.id)
    for ipv4 in ipv4s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv4.application_server.id)
    return retServers


#Returns only applicationservers that are associated with an ipv4/6 address that is associated with
#A DHCP option with the inputted field & value
def filter_by_dhcp_option(field, value):

    field = remove_prefix(field, "dhcp_")
    retServers = ApplicationServer.objects.none()
    ipv4s = IPv4HostAddress.objects.none()
    ipv6s = IPv6HostAddress.objects.none()

    strVal = str(value)
    if strVal == "True" or strVal == "False":
        filter = field
    else:
        filter = field + "__icontains"
    dhcps = DHCPOption.objects.filter(visible=True).filter(**{filter: value})

    for dhcp in dhcps:
        ipv4s = ipv4s | IPv4HostAddress.objects.filter(visible=True).filter(id=dhcp.ipv4_host_address.id)
        ipv6s = ipv6s | IPv6HostAddress.objects.filter(visible=True).filter(id=dhcp.ipv6_host_address.id)

    for ipv4 in ipv4s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv4.application_server.id)
    for ipv6 in ipv6s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv6.application_server.id)

    return retServers


#Returns only applicationservers that are associated with ipv6 host addresses that are associated with
# the DNS with given field and value
def filter_by_domain_name_server(field, value):
    field = remove_prefix(field, "dns_record_")
    retServers = ApplicationServer.objects.none()
    ipv6s = IPv6HostAddress.objects.none()

    filter = field + "__icontains"

    dnses = DomainNameServer.objects.filter(visible=True).filter(**{filter: value})

    for dns in dnses:
        ipv6s = ipv6s | IPv6HostAddress.objects.filter(visible=True).filter(id=dns.ipv6_host_address.id)

    for ipv6 in ipv6s:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=ipv6.application_server.id)

    return retServers


#Returns only applicationservers that are associated with a cli credential with the inputted field & value
def filter_by_cli_credential(field, value):
    field = remove_prefix(field, "cli_")
    retServers = ApplicationServer.objects.none()

    filter = field + "__icontains"

    clis = CliCredential.objects.filter(visible=True).filter(**{filter: value})

    for cli in clis:
        retServers = retServers | ApplicationServer.objects.filter(visible=True).filter(id=cli.application_server.id)

    return retServers


#filters servers based on a filter profile model instance, either created by a user through a filter profile form
#or temporarily instantiated for the purpose of a one-time advanced search
def filter_servers(filterProfile):
    fields = FilterProfile._meta.get_all_field_names()
    if filterProfile.all_fields is not None:
        results = ApplicationServer.objects.none()
        value = filterProfile.all_fields
        for field in fields:
            if field == "id" or field == "profile_name" or field == "all_fields" or field == "ipv6addr" or field == "alias" or field == "extensible_attribute_value" or field == "discovered_data": continue
            if field.startswith("ci_"):
                results = results | filter_by_cloud_information(field, value)
            elif field.startswith("snmp3_"):
                results = results | filter_by_snmp3_credential_information(field, value)
            elif field.startswith("snmp_"):
                results = results | filter_by_snmp_credential_information(field, value)
            elif field.startswith("aws_"):
                results = results | filter_by_aws_rte53_record_information(field, value)
            elif field.startswith("dd_"):
                results = results | filter_by_discovered_data(field, value)
            elif field.startswith("ipv4_"):
                results = results | filter_by_ipv4_host_address(field, value)
            elif field.startswith("ipv6_"):
                results = results | filter_by_ipv6_host_address(field, value)
            elif field.startswith("lfr_"):
                results = results | filter_by_logic_filter_rule(field, value)
            elif field.startswith("dhcp_"):
                results = results | filter_by_dhcp_option(field, value)
            elif field.startswith("dns_record_"):
                results = results | filter_by_domain_name_server(field, value)
            elif field.startswith("cli_"):
                results = results | filter_by_cli_credential(field, value)
            else:
                lookup = "%s__icontains" % field
                query = {lookup: value}
                results = results | ApplicationServer.objects.filter(**query).filter(visible=True)

        results = results | get_ipv4_application_servers(value)
        results = results | get_ipv6_application_servers(value)
        results = results | get_alias_application_servers(value)
        results = results | get_extensible_attribute_application_servers(value)
        results = results | get_discovered_data_application_servers(value)

        search_result = results

    else:
        search_result = ApplicationServer.objects.filter(visible=True)


    if filterProfile.alias is not None:
        search_result = search_result & get_alias_application_servers(filterProfile.alias)
    if filterProfile.extensible_attribute_value is not None:
        search_result = search_result & get_extensible_attribute_application_servers(filterProfile.extensible_attribute_value)
    if filterProfile.discovered_data is not None:
        search_result = search_result & get_discovered_data_application_servers(filterProfile.discovered_data)

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
            elif field.startswith("ipv4_"):
                search_result = search_result & filter_by_ipv4_host_address(field, value)
            elif field.startswith("ipv6_"):
                search_result = search_result & filter_by_ipv6_host_address(field, value)
            elif field.startswith("lfr_"):
                search_result = search_result & filter_by_logic_filter_rule(field, value)
            elif field.startswith("dhcp_"):
                search_result = search_result & filter_by_dhcp_option(field, value)
            elif field.startswith("dns_record_"):
                search_result = search_result & filter_by_domain_name_server(field, value)
            elif field.startswith("cli_"):
                search_result = search_result & filter_by_cli_credential(field, value)
            else:
                filter = field + "__icontains"
                search_result = search_result.filter(**{filter: value})
    search_result = search_result.filter(visible=True)
    return search_result


#If any filter profile fields are empty strings, sets them to null for convenience later
def prep_filter_for_save(filter):
    # setting any empty field to have a null value
    fields = FilterProfile._meta.get_all_field_names()
    for field in fields:
        if getattr(filter, field) == "":
            if FilterProfile._meta.get_field(field).null:
                setattr(filter, field, None)
    return filter


#------Visible Field Helper Functions------

#This group of functions gets the visible fields from the visible field model instance for the current user
#for the relevant model that is designated in the function name


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


def get_visible_cloud_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.CLOUD_INFORMATION_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "ci_"+field[0]):
            if getattr(visible_columns, "ci_"+field[0]) is True:
                retList.append(field)
    return retList


def get_visible_dhcp_member_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.DHCP_MEMBER_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "dm_" + field[0]):
            if getattr(visible_columns, "dm_" + field[0]) is True:
                retList.append(field)
    return retList


def get_visible_snmp3_credential_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.SNMP3_CREDENTIAL_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "snmp3_" + field[0]):
            if getattr(visible_columns, "snmp3_" + field[0]) is True:
                retList.append(field)
    return retList


def get_visible_snmp_credential_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.SNMP_CREDENTIAL_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "snmp_" + field[0]):
            if getattr(visible_columns, "snmp_" + field[0]) is True:
                retList.append(field)
    return retList


def get_visible_aws_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.AWS_RTE53_RECORD_INFO_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "aws_" + field[0]):
            if getattr(visible_columns, "aws_" + field[0]) is True:
                retList.append(field)
    return retList


def get_visible_discovered_data_fields(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    fields = VisibleColumns._meta.get_all_field_names()
    fieldList = models.DISCOVERED_DATA_FIELDS
    retList = []
    for field in fieldList:
        if hasattr(visible_columns, "dd_" + field[0]):
            if getattr(visible_columns, "dd_" + field[0]) is True:
                retList.append(field)
    return retList


#------View Functions-------


#Gets the applicationservers that are to be shown in the home page
@login_required
def view_application_servers(request):
    visible_columns = VisibleColumns.objects.filter(user=request.user).get()
    application_servers = ApplicationServer.objects.filter(visible=True).order_by('id')
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
    cloud_fields = get_visible_cloud_fields(request)
    delegated_member_fields = get_visible_dhcp_member_fields(request)
    snmp3_fields = get_visible_snmp3_credential_fields(request)
    snmp_fields = get_visible_snmp_credential_fields(request)
    aws_fields = get_visible_aws_fields(request)
    dd_fields = get_visible_discovered_data_fields(request)

    args = {'applicationServers': application_servers,
            'fields': fields,
            'cloudFields': cloud_fields,
            'dmFields': delegated_member_fields,
            'snmp3Fields': snmp3_fields,
            'snmpFields': snmp_fields,
            'awsFields': aws_fields,
            'ddFields': dd_fields,
            'form': form,
            }
    return render(request, 'application_server_list.html', args)


#Gets details for a given applicationserver, passes them to the details view
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


@login_required()
def delete_application_server(request, pk):
    application_server = get_object_or_404(ApplicationServer, pk=pk)
    application_server.deleteWithForeign()
    return redirect('/infrastructureinventory/applicationserver/')


#One-time instantiation of a filter profile for the purpose of an advanced search
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


#Renders modal for confirmation of deletion of an applicationserver
@login_required()
def application_server_delete_confirm(request, pk):
    applicationServer = get_object_or_404(ApplicationServer, pk=pk)
    return render(request, 'application_server_delete_confirm.html', {'applicationServer': applicationServer})


#Gets filter profiles and renders filter profile list with those filter profiles
@login_required()
def filter_profile(request):
    filterProfiles = FilterProfile.objects.all()
    return render(request, 'filter_profiles.html', {"filterProfiles": filterProfiles})


#Renders list to create a new filter profile, handles POST case of submitted filter profile form in which case
#the profile needs to be saved
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


#Filters the applicationservers by the fields provided in the passed-in filter profile
#Renders applicationserver list with those applicationservers
@login_required()
def filtered_list(request, pk):
    if request.method == 'POST':

        #If delete modal in filteredlist page was opened and confirmed for deletion of this batch of records
        if request.POST.get('confirmed-delete') == 'true':
            applicationServers = json.loads(request.POST.get('application_servers'), strict=False)
            for applicationServer in applicationServers:
                if applicationServer['fields']['visible'] is True:
                    if ApplicationServer.objects.filter(visible=True).filter(ref=applicationServer['fields']['ref']).count() == 1:
                        currServer = ApplicationServer.objects.filter(visible=True).filter(ref=applicationServer['fields']['ref']).get()
                        currServer.deleteWithForeign()

        #If the user is submitting a visible column form (The other possible POST request from this page
        else:
            form = VisibleColumnForm(request.POST)
            if form.is_valid():
                if VisibleColumns.objects.filter(user=request.user).count() > 0:
                    VisibleColumns.objects.filter(user=request.user).delete()
                visible_columns = form.save(commit=False)
                visible_columns.user = request.user
                visible_columns.save()

    form = VisibleColumnForm(instance=VisibleColumns.objects.filter(user=request.user).get())

    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    filter_result = filter_servers(filterProfile)
    fields = get_visible_fields(request)
    args = {'applicationServers': filter_result, 'fields': fields, "profileName": filterProfile.profile_name, "form": form}
    return render(request, 'filtered_list.html', args)


#Renders modal for confirmation of deletion of a filter profile
@login_required()
def filter_profile_delete_confirm(request, pk):
    filterProfile = get_object_or_404(FilterProfile, pk=pk)
    return render(request, 'filter_profile_delete_confirm.html', {"filterProfile": filterProfile})


#Executes deletion of a filter profile and redirects user to filter profile list page
@login_required()
def filter_profile_delete(request, pk):
    get_object_or_404(FilterProfile, pk=pk).delete()
    return redirect('/infrastructureinventory/applicationserver/filterprofile')


#Renders filter profile form, pre-populated with information from passed-in instance of filter profile.
#After user makes desired modifications & submits form, saves those modifications and redirects user to filter profile list
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


#Renders modal for confirmation of batch delete of applicationservers, with applicationservers to be deleted passed in
#In JSON format

@login_required()
def confirm_batch_delete(request):
    if request.method == "POST":
        applicationServers = request.POST.get('application_servers')
        return render(request, "batch_delete_confirm.html", {"applicationServers": applicationServers})
    return HttpResponse("Should be accessed through a POST Request.")
