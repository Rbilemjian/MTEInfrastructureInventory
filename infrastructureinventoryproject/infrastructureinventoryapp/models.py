from django.db import models
from django.contrib.auth.models import User


ENVIRONMENTS = [
    ('Prod', 'Production'),
    ('Dev', 'Development'),
    ('QA', 'Quality Assurance'),
]

ENVIRONMENTS_WITH_NULL = [
    ('Prod', 'Production'),
    ('Dev', 'Development'),
    ('QA', 'Quality Assurance'),
    (None, 'N/A')
]


NETWORKS = [
    ('Corp', 'Corp'),
    ('DMZ', 'DMZ'),
]

NETWORKS_WITH_NULL = [
    (None, 'N/A'),
    ('Corp', 'Corp'),
    ('DMZ', 'DMZ'),
]


BOOL = [
    (0, 'No'),
    (1, 'Yes'),
]

BOOL_WITH_NULL = [
    (None, 'N/A'),
    (0, 'No'),
    (1, 'Yes'),
]


class ApplicationServer(models.Model):

    #General Information
    service = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    primary_application = models.CharField(max_length=100)
    is_virtual_machine = models.BooleanField(default=False)
    environment = models.CharField(max_length=4, choices=ENVIRONMENTS, default="Prod")
    operating_system = models.CharField(max_length=100)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    #Location Information
    location = models.CharField(max_length=40)
    data_center = models.CharField(max_length=30)
    rack = models.CharField(max_length=20, null=True, blank=True)


    #Network Information
    network = models.CharField(max_length=4, choices=NETWORKS, default="Corp")
    private_ip = models.GenericIPAddressField(null=True, blank=True)
    dmz_public_ip = models.GenericIPAddressField(null=True, blank=True)
    virtual_ip = models.GenericIPAddressField(null=True, blank=True)
    nat_ip = models.GenericIPAddressField(null=True, blank=True)
    ilo_or_cimc = models.GenericIPAddressField(null=True, blank=True)
    nic_mac_address = models.CharField(max_length=23, null=True, blank=True)
    switch = models.CharField(max_length=40, null=True, blank=True)
    port = models.CharField(max_length=40, null=True, blank=True)

    #Warranty Information

    purchase_order = models.CharField(max_length=20, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    next_hardware_support_date = models.DateField(null=True, blank=True)
    base_warranty = models.DateField(null=True, blank=True)

    #Storage Information
    cpu = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    c_drive = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    d_drive = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    e_drive = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    #Visible Boolean
    visible = models.BooleanField(default=True)

    #Logistical Information
    published_by = models.ForeignKey(User, null=True, related_name='application_server_owner')
    published_date = models.DateTimeField(null=True, blank=True, editable=False)
    last_edited = models.DateTimeField(null=True, blank=True)
    last_editor = models.ForeignKey(User, null=True, related_name='last_application_server_editor')



class filterProfile(models.Model):

    #General Information
    service = models.CharField(max_length=100, null=True, blank=True)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    primary_application = models.CharField(max_length=100, null=True, blank=True)
    is_virtual_machine = models.NullBooleanField(choices=BOOL_WITH_NULL, default=None, null=True, blank=True)
    environment = models.CharField(max_length=4, choices=ENVIRONMENTS_WITH_NULL, default=None, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    purchase_order = models.CharField(max_length=20, null=True, blank=True)

    #Location Information
    location = models.CharField(max_length=40, null=True, blank=True)
    data_center = models.CharField(max_length=30, null=True, blank=True)
    rack = models.CharField(max_length=20, null=True, blank=True)

    # Network Information
    network = models.CharField(max_length=4, choices=NETWORKS_WITH_NULL, default=None, null=True, blank=True)
    private_ip = models.GenericIPAddressField(null=True, blank=True)
    dmz_public_ip = models.GenericIPAddressField(null=True, blank=True)
    virtual_ip = models.GenericIPAddressField(null=True, blank=True)
    nat_ip = models.GenericIPAddressField(null=True, blank=True)
    ilo_or_cimc = models.GenericIPAddressField(null=True, blank=True)
    nic_mac_address = models.CharField(max_length=23, null=True, blank=True)
    switch = models.CharField(max_length=40, null=True, blank=True)
    port = models.CharField(max_length=40, null=True, blank=True)