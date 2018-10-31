from django import forms
from . import models
from .models import ApplicationServer, FilterProfile
import floppyforms

#Getting list of unique values for certain columns in the database for use in floppyforms

services = ApplicationServer.objects.filter().values_list('service', flat=True).order_by('service').distinct()
hostnames = ApplicationServer.objects.filter().values_list('hostname', flat=True).order_by('hostname').distinct().exclude
primary_applications = ApplicationServer.objects.filter().values_list('primary_application', flat=True).order_by('primary_application').distinct()
locations = ApplicationServer.objects.filter().values_list('location', flat=True).order_by('location').distinct()
data_centers = ApplicationServer.objects.filter().values_list('data_center', flat=True).order_by('data_center').distinct()
operating_systems = ApplicationServer.objects.filter().values_list('operating_system', flat=True).order_by('operating_system').distinct()
racks = ApplicationServer.objects.filter().values_list('rack', flat=True).order_by('rack').distinct().exclude(rack__isnull=True)
server_models = ApplicationServer.objects.filter().values_list('model', flat=True).order_by('model').distinct().exclude(model__isnull=True)
serial_numbers = ApplicationServer.objects.filter().values_list('serial_number', flat=True).order_by('serial_number').distinct().exclude(serial_number__isnull=True)
private_ips = ApplicationServer.objects.filter().values_list('private_ip', flat=True).order_by('private_ip').distinct().exclude(private_ip__isnull=True)
dmz_public_ips = ApplicationServer.objects.filter().values_list('dmz_public_ip', flat=True).order_by('dmz_public_ip').distinct().exclude(dmz_public_ip__isnull=True)
virtual_ips = ApplicationServer.objects.filter().values_list('virtual_ip', flat=True).order_by('virtual_ip').distinct().exclude(virtual_ip__isnull=True)
nat_ips = ApplicationServer.objects.filter().values_list('nat_ip', flat=True).order_by('nat_ip').distinct().exclude(nat_ip__isnull=True)
ilo_or_cimcs = ApplicationServer.objects.filter().values_list('ilo_or_cimc', flat=True).order_by('ilo_or_cimc').distinct().exclude(ilo_or_cimc__isnull=True)
nic_mac_addresses = ApplicationServer.objects.filter().values_list('nic_mac_address', flat=True).order_by('nic_mac_address').distinct().exclude(nic_mac_address__isnull=True)
switches = ApplicationServer.objects.filter().values_list('switch', flat=True).order_by('switch').distinct().exclude(switch__isnull=True)
ports = ApplicationServer.objects.filter().values_list('port', flat=True).order_by('port').distinct().exclude(port__isnull=True)
purchase_orders = ApplicationServer.objects.filter().values_list('purchase_order', flat=True).order_by('purchase_order').distinct().exclude(purchase_order__isnull=True)
filter_profiles = FilterProfile.objects.filter().values_list('profile_name', flat=True)

#Defines form for new application server and application server edit pages

class ServerForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationServer
        fields = '__all__'
        widgets = {

            #General Info Form Widgets

            'service': floppyforms.widgets.Input(datalist=services, attrs={'size': 45}),
            'hostname': floppyforms.widgets.Input(datalist=hostnames, attrs={'size': 45}),
            'primary_application': floppyforms.widgets.Input(datalist=primary_applications, attrs={'size': 45}),
            'is_virtual_machine': forms.Select(choices=models.BOOL, attrs={'width': '335px'}),
            'location': floppyforms.widgets.Input(datalist=locations, attrs={'size': 45}),
            'data_center': floppyforms.widgets.Input(datalist=data_centers, attrs={'size': 45}),
            'rack': floppyforms.widgets.Input(datalist=racks, attrs={'size': 45}),
            'operating_system': floppyforms.widgets.Input(datalist=operating_systems, attrs={'size': 45}),
            'model': floppyforms.widgets.Input(datalist=server_models, attrs={'size': 45}),
            'serial_number': floppyforms.widgets.Input(datalist=serial_numbers, attrs={'size': 45}),
            'notes': forms.Textarea(attrs={'rows': 5, 'cols': 20000, 'style': 'resize:none; width:99%', 'class': 'container'}),

            #Network Info Form Widgets

            'private_ip': floppyforms.widgets.Input(datalist=private_ips, attrs={'size': 45}),
            'dmz_public_ip': floppyforms.widgets.Input(datalist=dmz_public_ips, attrs={'size': 45}),
            'virtual_ip': floppyforms.widgets.Input(datalist=virtual_ips, attrs={'size': 45}),
            'nat_ip': floppyforms.widgets.Input(datalist=nat_ips, attrs={'size': 45}),
            'ilo_or_cimc': floppyforms.widgets.Input(datalist=ilo_or_cimcs, attrs={'size': 45}),
            'nic_mac_address': floppyforms.widgets.Input(datalist=nic_mac_addresses, attrs={'size': 45}),
            'switch': floppyforms.widgets.Input(datalist=switches, attrs={'size': 45}),
            'port': floppyforms.widgets.Input(datalist=ports, attrs={'size': 45}),

            #Warranty Info Form Widgets

            'purchase_order': floppyforms.widgets.Input(datalist=purchase_orders, attrs={'size': 31}),
            'start_date': forms.DateInput(attrs={'class': 'datepicker', 'size': 31, 'autocomplete': 'off'}),
            'next_hardware_support_date': forms.DateInput(attrs={'class': 'datepicker', 'size': 31, 'autocomplete': 'off'}),
            'base_warranty': forms.DateInput(attrs={'class': 'datepicker', 'size': 31, 'autocomplete': 'off'}),

            #Storage Info Form Widgets

            'cpu': forms.NumberInput(attrs={'min_value': 0}),
            'ram': forms.NumberInput(attrs={'min_value': 0}),
            'c_drive': forms.NumberInput(attrs={'min_value': 0, 'decimal_places': 2, 'size': 45}),
            'd_drive': forms.NumberInput(attrs={'min_value': 0, 'decimal_places': 2, 'size': 45}),
            'e_drive': forms.NumberInput(attrs={'min_value': 0, 'decimal_places': 2, 'size': 45}),
        }
        exclude = ['visible', 'published_by', 'published_date', 'last_edited', 'last_editor']

#defins form for importing servers (just a file picker)

class ServerImportForm(forms.Form):
    file = forms.FileField()

#defines form for advanced search of application servers

class ServerSearchForm(forms.Form):

    #General Information Search Form Fields

    service = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=services, attrs={'size': 45}))
    hostname = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=hostnames, attrs={'size': 45}))
    primary_application = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=primary_applications, attrs={'size': 45}))
    is_virtual_machine = forms.ChoiceField(required=False, choices=models.BOOL_WITH_NULL, widget=forms.Select())
    location = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=locations, attrs={'size': 45}))
    data_center = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=data_centers, attrs={'size': 45}))
    rack = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=racks, attrs={'size': 45}))
    operating_system = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=operating_systems, attrs={'size': 45}))
    model = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=server_models, attrs={'size': 45}))
    serial_number = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=serial_numbers, attrs={'size': 45}))
    environment = forms.ChoiceField(required=False, choices=models.ENVIRONMENTS_WITH_NULL, widget=forms.Select())
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 2000, 'style': 'resize: none; width: 99%', 'class': 'container'}))

    #Network Information Search Form Fields

    network = forms.ChoiceField(required=False, choices=models.NETWORKS_WITH_NULL, widget=forms.Select())
    private_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=private_ips, attrs={'size': 45}))
    dmz_public_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=dmz_public_ips, attrs={'size': 45}))
    virtual_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=virtual_ips, attrs={'size': 45}))
    nat_ip = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=nat_ips, attrs={'size': 45}))
    ilo_or_cimc = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=ilo_or_cimcs, attrs={'size': 45}))
    nic_mac_address = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=nic_mac_addresses, attrs={'size': 45}))
    switch = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=switches, attrs={'size': 45}))
    port = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=ports, attrs={'size': 45}))

    #Warranty Information Search Form Fields

    purchase_order = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=purchase_orders, attrs={'size': 45}))


class FilterProfileForm(forms.ModelForm):
    class Meta:
        model = models.FilterProfile
        fields = '__all__'
        widgets = {

            #Profile Info Form Widgets

            'profile_name': forms.TextInput(attrs={'size': 45}),

            #General Info Form Widgets

            'service': floppyforms.widgets.Input(datalist=services, attrs={'size': 45}),
            'hostname': floppyforms.widgets.Input(datalist=hostnames, attrs={'size': 45}),
            'primary_application': floppyforms.widgets.Input(datalist=primary_applications, attrs={'size': 45}),
            'is_virtual_machine': forms.Select(choices=models.BOOL, attrs={'cols': 5}),
            'location': floppyforms.widgets.Input(datalist=locations, attrs={'size': 45}),
            'data_center': floppyforms.widgets.Input(datalist=data_centers, attrs={'size': 45}),
            'rack': floppyforms.widgets.Input(datalist=racks, attrs={'size': 45}),
            'operating_system': floppyforms.widgets.Input(datalist=operating_systems, attrs={'size': 45}),
            'model': floppyforms.widgets.Input(datalist=server_models, attrs={'size': 45}),
            'serial_number': floppyforms.widgets.Input(datalist=serial_numbers, attrs={'size': 45}),

            #Network Info Form Widgets

            'private_ip': floppyforms.widgets.Input(datalist=private_ips, attrs={'size': 45}),
            'dmz_public_ip': floppyforms.widgets.Input(datalist=dmz_public_ips, attrs={'size': 45}),
            'virtual_ip': floppyforms.widgets.Input(datalist=virtual_ips, attrs={'size': 45}),
            'nat_ip': floppyforms.widgets.Input(datalist=nat_ips, attrs={'size': 45}),
            'ilo_or_cimc': floppyforms.widgets.Input(datalist=ilo_or_cimcs, attrs={'size': 45}),
            'nic_mac_address': floppyforms.widgets.Input(datalist=nic_mac_addresses, attrs={'size': 45}),
            'switch': floppyforms.widgets.Input(datalist=switches, attrs={'size': 45}),
            'port': floppyforms.widgets.Input(datalist=ports, attrs={'size': 45}),

            #Warranty Info Form Widgets

            'purchase_order': floppyforms.widgets.Input(datalist=purchase_orders, attrs={'size': 45}),


        }



