from django.db import models

# Create your models here.

ENVIRONMENTS = [
    ('Prod', 'Production'),
    ('Dev', 'Development'),
    ('QA', 'Quality Assurance'),
]

LOCATIONS = [
    'New York',
    '30Rock',
    'Centennial',
    'Englewood Cliffs',
    'Universal City',
    'Ashburn',
]

DATA_CENTERS = [
    '32 Avenue of Americas',
    '2nd Floor Machine Room ER-F',
    'Dry Creek',
    'CER3',
    'CER',
    '990',
    'Broadcast DMZ',
    'USH 1360',
    'WC DMZ - 1360',
    'Ashburn',
]

OPERATING_SYSTEMS = [
    'Oracle Linux - OEL 5.7 64-Bit',
    'Oracle Linux - OEL 6.5 64-Bit',
    'Redhat Linux - RHEL AS 3.0',
    'Redhat Linux - RHEL AS 4.0',
    'Ubuntu 14.04.2 LTS 64-Bit',
    'Windows 2008 R2 Standard 64-Bit',
    'Windows 2012 R2 Standard 64-Bit',
]


NETWORKS = [
    ('Corp', 'Corp'),
    ('DMZ', 'DMZ'),
]

BOOL = [
    (0, 'No'),
    (1, 'Yes'),
]


class ApplicationServer(models.Model):

    service = models.CharField(max_length=40)
    hostname = models.CharField(max_length=30)
    primary_application = models.CharField(max_length=40)
    is_virtual_machine = models.BooleanField(default=False)
    environment = models.CharField(max_length=4, choices=ENVIRONMENTS, default="Prod")
    location = models.CharField(max_length=40)
    data_center = models.CharField(max_length=30)
    operating_system = models.CharField(max_length=30)
    rack = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

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
    c_drive = models.IntegerField(null=True, blank=True)
    d_drive = models.IntegerField(null=True, blank=True)
    e_drive = models.IntegerField(null=True, blank=True)







