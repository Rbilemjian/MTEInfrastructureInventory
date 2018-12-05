from django import forms
from . import models
from .models import ApplicationServer, FilterProfile, FILTER_RECORD_TYPES, RECORD_TYPES, BOOL_WITH_NULL
from .models import IPv6HostAddress, IPv4HostAddress, Alias, ExtensibleAttribute, DiscoveredData
import floppyforms

#helper functions

def get_all_discovered_data_values():
    fields = models.DISCOVERED_DATA_FIELDS
    values = list()
    dds = DiscoveredData.objects.all()
    for dd in dds:
        for field in fields:
            currVal = getattr(dd, field[0])
            if currVal not in values:
                values.append(currVal)
    return values

def get_all_extensible_field_values():
    values = list()
    eas = ExtensibleAttribute.objects.all()
    for ea in eas:
            currVal = getattr(ea, "attribute_value")
            if currVal not in values:
                values.append(currVal)
    return values


#Getting list of unique values for certain columns in the database for use in floppyforms
#
names = ApplicationServer.objects.filter(visible=True).values_list('name', flat=True).order_by('name').distinct()
views = ApplicationServer.objects.filter(visible=True).values_list('view', flat=True).order_by('view').distinct()
zones = ApplicationServer.objects.filter(visible=True).values_list('zone', flat=True).order_by('zone').distinct()
ms_ad_user_datas = ApplicationServer.objects.filter(visible=True).values_list('ms_ad_user_data', flat=True).order_by('ms_ad_user_data').distinct()
ttls = ApplicationServer.objects.filter(visible=True).values_list('ttl', flat=True).order_by('ttl').distinct()
creators = ApplicationServer.objects.filter(visible=True).values_list('creator', flat=True).order_by('creator').distinct()
ddns_principals = ApplicationServer.objects.filter(visible=True).values_list('ddns_principal', flat=True).order_by('ddns_principal').distinct()
shared_record_groups = ApplicationServer.objects.filter(visible=True).values_list('shared_record_group', flat=True).order_by('shared_record_group').distinct()
refs = ApplicationServer.objects.filter(visible=True).values_list('ref', flat=True).order_by('ref').distinct()
device_locations = ApplicationServer.objects.filter(visible=True).values_list('device_location', flat=True).order_by('device_location').distinct()
device_descriptions = ApplicationServer.objects.filter(visible=True).values_list('device_description', flat=True).order_by('device_description').distinct()
device_types = ApplicationServer.objects.filter(visible=True).values_list('device_type', flat=True).order_by('device_type').distinct()
device_vendors = ApplicationServer.objects.filter(visible=True).values_list('device_vendor', flat=True).order_by('device_vendor').distinct()
network_views = ApplicationServer.objects.filter(visible=True).values_list('network_view', flat=True).order_by('network_view').distinct()
ipv4addrs = ApplicationServer.objects.filter(visible=True).values_list('ipv4addr', flat=True).order_by('ipv4addr').distinct()
ipv4hostaddrs = IPv4HostAddress.objects.filter(visible=True).values_list('ipv4addr', flat=True).order_by('ipv4addr').distinct()
ipv4addrs = set(ipv4addrs)
ipv4hostaddrs = set(ipv4hostaddrs)
ipv4addrs = ipv4addrs | ipv4hostaddrs
ipv4addrs = list(ipv4addrs)
canonicals = ApplicationServer.objects.filter(visible=True).values_list('canonical', flat=True).order_by('canonical').distinct()
ipv6addrs = IPv6HostAddress.objects.filter(visible=True).values_list('ipv6addr', flat=True).order_by('ipv6addr').distinct()
aliases = Alias.objects.filter(visible=True).values_list('alias', flat=True).order_by('alias').distinct()
extensible_attribute_values = get_all_extensible_field_values()
discovered_data_values = get_all_discovered_data_values()



#defines form for importing records from a user-designated zone in infoblox

class InfobloxImportForm(forms.Form):
    view = forms.CharField(min_length=1, max_length=50, required=True)
    zone = forms.CharField(min_length=1, max_length=50, required=True)
    record_type = forms.ChoiceField(choices=RECORD_TYPES, required=True, widget=forms.Select())

#defines form for advanced search of application servers
#
# class ServerSearchForm(forms.Form):
#
#     #General Information Search Form Fields
#
#     service = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=services, attrs={'size': 45}))
#     hostname = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=hostnames, attrs={'size': 45}))
#     primary_application = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=primary_applications, attrs={'size': 45}))
#     is_virtual_machine = forms.ChoiceField(required=False, choices=models.BOOL_WITH_NULL, widget=forms.Select())
#     location = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=locations, attrs={'size': 45}))
#     data_center = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=data_centers, attrs={'size': 45}))
#     rack = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=racks, attrs={'size': 45}))
#     operating_system = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=operating_systems, attrs={'size': 45}))
#     model = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=server_models, attrs={'size': 45}))
#     serial_number = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=serial_numbers, attrs={'size': 45}))
#     environment = forms.ChoiceField(required=False, choices=models.ENVIRONMENTS_WITH_NULL, widget=forms.Select())
#     comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 2000, 'style': 'resize: none; width: 99%', 'class': 'container'}))
#
#     #Network Information Search Form Fields
#
#     network = forms.ChoiceField(required=False, choices=models.NETWORKS_WITH_NULL, widget=forms.Select())
#     private_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=private_ips, attrs={'size': 45}))
#     dmz_public_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=dmz_public_ips, attrs={'size': 45}))
#     virtual_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=virtual_ips, attrs={'size': 45}))
#     nat_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=nat_ips, attrs={'size': 45}))
#     ilo_or_cimc = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=ilo_or_cimcs, attrs={'size': 45}))
#     nic_mac_address = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=nic_mac_addresses, attrs={'size': 45}))
#     switch = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=switches, attrs={'size': 45}))
#     port = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=ports, attrs={'size': 45}))
#
#     #Warranty Information Search Form Fields
#
#     purchase_order = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=purchase_orders, attrs={'size': 45}))


class VisibleColumnForm(forms.ModelForm):
    class Meta:
        model = models.VisibleColumns
        exclude = ('user',)



class FilterProfileForm(forms.ModelForm):
    class Meta:
        model = models.FilterProfile
        exclude = []


        widgets = {
            #Profile Info Form Widgets
            'profile_name': forms.TextInput(attrs={'size': 45, 'required': True}),
            'all_fields': forms.TextInput(attrs={'size': 45}),

            #Record Info Form Widgets
            'name': floppyforms.widgets.Input(datalist=names, attrs={'size': 45}),
            'view': floppyforms.widgets.Input(datalist=views, attrs={'size': 45}),
            'zone': floppyforms.widgets.Input(datalist=zones, attrs={'size': 45}),
            'record_type': forms.Select(choices=FILTER_RECORD_TYPES),

            'ms_ad_user_data': floppyforms.widgets.Input(datalist=ms_ad_user_datas, attrs={'size': 45}),
            'ttl': floppyforms.widgets.Input(datalist=ttls, attrs={'size': 45}),
            'creator': floppyforms.widgets.Input(datalist=creators, attrs={'size': 45}),
            'ddns_principal': floppyforms.widgets.Input(datalist=ddns_principals, attrs={'size': 45}),
            'shared_record_group': floppyforms.widgets.Input(datalist=shared_record_groups, attrs={'size': 45}),
            'ref': floppyforms.widgets.Input(datalist=refs, attrs={'size': 45}),

            'device_location': floppyforms.widgets.Input(datalist=device_locations, attrs={'size': 45}),
            'device_description': floppyforms.widgets.Input(datalist=device_descriptions, attrs={'size': 45}),
            'device_type': floppyforms.widgets.Input(datalist=device_types, attrs={'size': 45}),
            'device_vendor': floppyforms.widgets.Input(datalist=device_vendors, attrs={'size': 45}),
            'network_view': floppyforms.widgets.Input(datalist=network_views, attrs={'size': 45}),

            #Select Widgets
            'rrset_order': forms.Select(),
            'use_cli_credentials': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp3_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable_discovery': floppyforms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'forbid_reclamation': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'ddns_protected': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_ttl': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'reclaimable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'allow_telnet': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'configure_for_dns': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),

            #Many-to-one Widgets
            'ipv4addr': floppyforms.widgets.Input(datalist=ipv4addrs, attrs={'size': 45}),
            'ipv6addr': floppyforms.widgets.Input(datalist=ipv6addrs, attrs={'size': 45}),
            'alias': floppyforms.widgets.Input(datalist=aliases, attrs={'size': 45}),
            'extensible_attribute_value': floppyforms.widgets.Input(datalist=extensible_attribute_values, attrs={'size': 45}),
            'discovered_data': floppyforms.widgets.Input(datalist=discovered_data_values, attrs={'size': 45}),
        }


class AdvancedSearchForm(forms.ModelForm):
    class Meta:
        model = models.FilterProfile
        exclude = []


        widgets = {
            'all_fields': forms.TextInput(attrs={'size': 45}),
            'name': floppyforms.widgets.Input(datalist=names, attrs={'size': 45}),
            'view': floppyforms.widgets.Input(datalist=views, attrs={'size': 45}),
            'zone': floppyforms.widgets.Input(datalist=zones, attrs={'size': 45}),
            'record_type': forms.Select(choices=FILTER_RECORD_TYPES),
            'ms_ad_user_data': floppyforms.widgets.Input(datalist=ms_ad_user_datas, attrs={'size': 45}),
            'ttl': floppyforms.widgets.Input(datalist=ttls, attrs={'size': 45}),
            'creator': floppyforms.widgets.Input(datalist=creators, attrs={'size': 45}),
            'ddns_principal': floppyforms.widgets.Input(datalist=ddns_principals, attrs={'size': 45}),
            'shared_record_group': floppyforms.widgets.Input(datalist=shared_record_groups, attrs={'size': 45}),
            'ref': floppyforms.widgets.Input(datalist=refs, attrs={'size': 45}),
            'device_location': floppyforms.widgets.Input(datalist=device_locations, attrs={'size': 45}),
            'device_description': floppyforms.widgets.Input(datalist=device_descriptions, attrs={'size': 45}),
            'device_type': floppyforms.widgets.Input(datalist=device_types, attrs={'size': 45}),
            'device_vendor': floppyforms.widgets.Input(datalist=device_vendors, attrs={'size': 45}),
            'network_view': floppyforms.widgets.Input(datalist=network_views, attrs={'size': 45}),

            #Select Widgets
            'rrset_order': forms.Select(),
            'use_cli_credentials': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp3_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable_discovery': floppyforms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'forbid_reclamation': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'ddns_protected': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_ttl': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'reclaimable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'allow_telnet': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'configure_for_dns': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),

            #Many-to-one Widgets
            'ipv4addr': floppyforms.widgets.Input(datalist=ipv4addrs, attrs={'size': 45}),
            'ipv6addr': floppyforms.widgets.Input(datalist=ipv6addrs, attrs={'size': 45}),
            'alias': floppyforms.widgets.Input(datalist=aliases, attrs={'size': 45}),
            'extensible_attribute_value': floppyforms.widgets.Input(datalist=extensible_attribute_values,attrs={'size': 45}),
            'discovered_data': floppyforms.widgets.Input(datalist=discovered_data_values, attrs={'size': 45}),
        }

#
#
#
# class FilterProfileForm(forms.ModelForm):
#     class Meta:
#         model = models.FilterProfile
#         fields = '__all__'
#         widgets = {
#
#             #Profile Info Form Widgets
#
#             'profile_name': forms.TextInput(attrs={'size': 45}),
#             'all_fields': forms.TextInput(attrs={'size': 45}),
#
#             #General Info Form Widgets
#
#             'service': floppyforms.widgets.Input(datalist=services, attrs={'size': 45}),
#             'hostname': floppyforms.widgets.Input(datalist=hostnames, attrs={'size': 45}),
#             'primary_application': floppyforms.widgets.Input(datalist=primary_applications, attrs={'size': 45}),
#             'is_virtual_machine': forms.Select(choices=models.BOOL, attrs={'cols': 5}),
#             'location': floppyforms.widgets.Input(datalist=locations, attrs={'size': 45}),
#             'data_center': floppyforms.widgets.Input(datalist=data_centers, attrs={'size': 45}),
#             'rack': floppyforms.widgets.Input(datalist=racks, attrs={'size': 45}),
#             'operating_system': floppyforms.widgets.Input(datalist=operating_systems, attrs={'size': 45}),
#             'model': floppyforms.widgets.Input(datalist=server_models, attrs={'size': 45}),
#             'serial_number': floppyforms.widgets.Input(datalist=serial_numbers, attrs={'size': 45}),
#
#             #Network Info Form Widgets
#
#             'private_ip': floppyforms.widgets.Input(datalist=private_ips, attrs={'size': 45}),
#             'dmz_public_ip': floppyforms.widgets.Input(datalist=dmz_public_ips, attrs={'size': 45}),
#             'virtual_ip': floppyforms.widgets.Input(datalist=virtual_ips, attrs={'size': 45}),
#             'nat_ip': floppyforms.widgets.Input(datalist=nat_ips, attrs={'size': 45}),
#             'ilo_or_cimc': floppyforms.widgets.Input(datalist=ilo_or_cimcs, attrs={'size': 45}),
#             'nic_mac_address': floppyforms.widgets.Input(datalist=nic_mac_addresses, attrs={'size': 45}),
#             'switch': floppyforms.widgets.Input(datalist=switches, attrs={'size': 45}),
#             'port': floppyforms.widgets.Input(datalist=ports, attrs={'size': 45}),
#
#             #Warranty Info Form Widgets
#
#             'purchase_order': floppyforms.widgets.Input(datalist=purchase_orders, attrs={'size': 45}),
#
#
#         }



