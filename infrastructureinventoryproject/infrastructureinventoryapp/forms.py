from django import forms
from . import models
import floppyforms

class ServerForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationServer
        fields = '__all__'
        widgets = {
            #General Info Form Widget

            'service': floppyforms.widgets.Input(datalist=models.SERVICES, attrs={'size': 45}),
            'hostname': forms.TextInput(attrs={'size': 45}),
            'primary_application': floppyforms.widgets.Input(datalist=models.PRIMARY_APPLICATIONS, attrs={'size': 45}),
            'is_virtual_machine': forms.Select(choices=models.BOOL, attrs={'width': '335px'}),
            'location': floppyforms.widgets.Input(datalist=models.LOCATIONS, attrs={'size': 45}),
            'data_center': floppyforms.widgets.Input(datalist=models.DATA_CENTERS, attrs={'size': 45}),
            'rack': forms.TextInput(attrs={'size': 45}),
            'operating_system': floppyforms.widgets.Input(datalist=models.OPERATING_SYSTEMS, attrs={'size': 45}),
            'model': forms.TextInput(attrs={'size': 45}),
            'serial_number': forms.TextInput(attrs={'size': 45}),
            'notes': forms.Textarea(attrs={'rows': 5, 'cols': 99, 'style': 'resize:none'}),

            #Network Info Form Widgets

            'private_ip': forms.TextInput(attrs={'size': 45}),
            'dmz_public_ip': forms.TextInput(attrs={'size': 45}),
            'virtual_ip': forms.TextInput(attrs={'size': 45}),
            'nat_ip': forms.TextInput(attrs={'size': 45}),
            'ilo_or_cimc': forms.TextInput(attrs={'size': 45}),
            'nic_mac_address': forms.TextInput(attrs={'size': 45}),
            'switch': forms.TextInput(attrs={'size': 45}),
            'port': forms.TextInput(attrs={'size': 45}),

            #Warranty Info Form Widgets

            'purchase_order': forms.TextInput(attrs={'size': 31}),
            'start_date': forms.DateInput(attrs={'class': 'datepicker', 'size': 31}),
            'next_hardware_support_date': forms.DateInput(attrs={'class': 'datepicker', 'size': 31}),
            'base_warranty': forms.DateInput(attrs={'class': 'datepicker', 'size': 31}),

            #Storage Info Form Widgets

            'cpu': forms.NumberInput(attrs={'min_value': 0}),
            'ram': forms.NumberInput(attrs={'min_value': 0}),
            'c_drive': forms.NumberInput(attrs={'min_value': 0, 'size': 45}),
            'd_drive': forms.NumberInput(attrs={'min_value': 0,'size': 45}),
            'e_drive': forms.NumberInput(attrs={'min_value': 0,'size': 45}),
            'storage_type': forms.NumberInput(attrs={'min_value': 0}),
        }
