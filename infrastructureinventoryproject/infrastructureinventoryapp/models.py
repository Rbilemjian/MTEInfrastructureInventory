from django.db import models
from django.contrib.auth.models import User

# Create your models here.

SERVICES = [
    'Anvato Server',
    'Aspera / Orchaestrator Cluster',
    'Aspera / Orchaestrator Node',
    'Aspera ACM Node A (New)',
    'Aspera ACM Node A (New) HUB Console',
    'Aspera ACM Node B (New)',
    'Aspera ACM Node B (New) HUB Console',
    'Aspera Agent',
    'Aspera Agent DVS',
    'Aspera Agent VM',
    'Aspera Cargo',
    'Aspera Console Cluster - Node A',
    'Aspera Console Node 1',
    'Aspera Console Node 2',
    'Aspera Faspex ACM Cluster',
    'Aspera Faspex Node A',
    'Aspera Faspex Node B',
    'Aspera Faspex Server',
    'Aspera Orchaestrator Node',
    'Aspera P2P',
    'Aspera P2P Node',
    'Aspera Proxy',
    'Aspera Proxy (MCP)',
    'Aspera Server',
    'Database Server',
    'FMS Server',
    'FMS Server (MyVideo)',
    'FMS Server ASH',
    'FMS Server WC',
    'MCDS Server',
    'MCDS Server (Hot Folder Manager - USNYCPAPL291)',
    'MCDS Server (Hot Folder Manager - VIP)',
    'MCDS Servers (Signiant External Relay)',
    'MCP Agent (Anvato)',
    'Nagios Server',
    'Not Being Used',
    'Open',
    'Pentaho Server',
    'Rhozet Managers',
    'Rhozet WFS Manager',
    'Rhozet WFS Manager (Backup)',
    'Signiant Agent',
    'Signiant Agent - LB Group',
    'Signiant Agent VM',
    'Signiant Cluster - (Signiant Manager - USECLAPLP103',
    'Signiant Cluster Node A - Database Server',
    'Signiant Cluster Node B - Database Server',
    'Signiant DMZ Relay Server',
    'Signiant Relay',
    'Signiant Server',
    'Signiant Staging Manager',
    'Symantec Virus Scanner',
    'Syndie Servers',
    'Syndie Transcode Server',
    'Transcode Manager (Rhozet WFS - Backup)',
    'Transcode Manager (Rhozet WFS)',
    'Transcoding Server - Rhozet',
    'Transcoding Server - Rhozet (MICAH Farm)',
    'Transcoding Server - Rhozet To replace 385)',
    'Transcoding Server (Rhozet WFS)',
    'Unused',
    'Virus Scanner',
]

PRIMARY_APPLICATIONS = [
    'Anvato MCP Agent - (SHUTDOWN)',
    'Apache Web Server - Matt Remis',
    'Aspera (Denver Cozi -FTP workflow)',
    'Aspera Agent',
    'Aspera Agent  - DVS P2P (ArQiva Node1)',
    'Aspera Agent  - DVS P2P (ArQiva Node2)',
    'Aspera Agent - P2P',
    'Aspera Agent - P2P Node',
    'Aspera Agent - P2P Node (NOC Telestream)',
    'Aspera Agent - P2P Node (NOC Transfers)',
    'Aspera Agent - P2P Node (Stratus)  (Refreshed with VM)',
    'Aspera Agent - Replaced USUSHPAPW655',
    'Aspera Agent VM (Replaced ECLAPWP00044)',
    'Aspera Agent VM (Replaced ECLAPWP00055)',
    'Aspera AppLication (Retire)',
    'Aspera Cargo Agent',
    'Aspera Connect cLuster (Node A) OLD',
    'Aspera Connect cLuster (Node B) OLD',
    'Aspera Connect/Relay (DMZ)',
    'Aspera Console (Backup  VM)',
    'Aspera ConsoLe (Old Console)',
    'Aspera Console (Primary VM)',
    'Aspera Console Cluster (Node A)',
    'Aspera Console Cluster (Node B)',
    'Aspera Faspex Cluster',
    'Aspera Faspex Cluster - Node A',
    'Aspera Faspex Cluster - Node B',
    'Aspera Faspex Cluster (Node A)',
    'Aspera Faspex Servers (replacement ECLAPWP00117)',
    'Aspera Faspex Servers (replacement ECLAPWP00118)',
    'Aspera iTunes P2P (DMZ)',
    'Aspera Orchaestrator  / Anvato Server CLuster',
    'Aspera Orchaestrator - iTunes ECMO Delivery',
    'Aspera P2P Node (To be retired - Refresh with VM)',
    'Aspera P2P Proxy DMZ',
    'Aspera Proxy - Aspera Proxy v.3.1',
    'Aspera Proxy - Proxy v.3.1',
    'Aspera Proxy - WC Aspera Proxy v.3.1',
    'Aspera Proxy - WC Aspera Proxy v.3.1 (Needs upgrading)',
    'Aspera Proxy (MCP)',
    'CLuster VirtuaL Name',
    'DME Digital Rapids Manager (FineCut)',
    'FLash Servers - DMZ',
    'FMS Server',
    'FMS Server - External (New)',
    'FMS Server - Internal',
    'FMS Server - Internal  (New)',
    'FMS Server 5.0 - Internal',
    'FMS Streaming Server  Node 1',
    'FMS Streaming Server  Node 2',
    'FMS Streaming Server - DMZ',
    'iTunes - NOC to AppLe',
    'MCP Agent',
    'Nagios Manager',
    'Needs Image',
    'Not Being used',
    'Pentaho DB Datawarehouse Server',
    'Rhozet - WFS Manager & Teletrax License Manager',
    'Rhozet - Workflow Manager (Backup)',
    'Rhozet Agent (2K8)',
    'Rhozet Development Agent (2K8)',
    'Rhozet Managers (WFS Manager & Affiliates Watermark)',
    'Rhozet Managers (WFS Manager & Teletrax Lic Manager)',
    'Rhozet QA Server- Replaced USNYCAPWPQ234',
    'Rhozet Transcode Agent',
    'Rhozet Transcode Agent - (Affiliates Watermark)',
    'Rhozet Transcode Agent - (Facilis Storage client - PRORES) Replaced USECLAPWP387',
    'Rhozet Transcode Agent - (Replacing with ECLAPWP00093)',
    'Rhozet Transcode Agent - extreme reach agent',
    'Rhozet Transcode Agent - Replaced USECLAPWP385',
    'Rhozet Transcode Agent - Syndie (Shutdown)',
    'Rhozet Transcode Agent - WFS Agent',
    'Rhozet Transcode Agent (WC Extreme Reach Media Uploader)',
    'Rhozet WFS Agent',
    'Rhozet WFS Agent - (Affiliates Watermark - PRORES)',
    'Rhozet WFS SQL Dev Server (db Name: WFSDB)',
    'Rhozet WFS SQL Server (db Name: WFSDB)',
    'Rhozet WFS Transcode Agent',
    'Rhozet WFS Transcode Agent - Affliates Watermark',
    'Signiant',
    'Signiant - UDS ReLay Server',
    'Signiant (Retiring)',
    'Signiant (Stratus Transfers & WorkfLows) Soon to be retired',
    'Signiant Agent',
    'Signiant Agent (EC LB Group) - Migrate',
    'Signiant Agent (LB Group)',
    'Signiant Agent (LB Group) - Replaced USECLAPWP193',
    'Signiant Agent (LB Group) - Replaced USECLAPWP194',
    'Signiant Agent (LB Group) - Replaced USHAPWP00085',
    'Signiant Agent (LB Group) - Replaced USHAPWP00086',
    'Signiant Agent (LB Group) - Replaced USNYCAPWPQ235',
    'Signiant Agent (LB Group) - Replaced USUSHPAPW648 (In Process)',
    'Signiant Agent (LB Group) - Replaced USUSHPAPW717 (In Process)',
    'Signiant Agent (LB Group) - Replaced USUSHPAPW718 (In Process)',
    'Signiant Agent (Load BaLanced Farm)',
    'Signiant Agent LB Group',
    'Signiant Agent VM',
    'Signiant DMZ Relay Agent',
    'Signiant DMZ Relay Agent (REFRESH)',
    'Signiant Manager - Cluster Node 1, Hotfolder',
    'Signiant Manager - Cluster Node 2 HotfoLder',
    'Signiant Manager Cluster - Node A',
    'Signiant Manager Cluster - Node B',
    'Signiant Manager/Signiant Prod Manager',
    'Signiant Relay Agent (DMZ)',
    'Signiant Relay Agent (DMZ)',
    'Signiant Server  (REFRESH)',
    'Signiant Staging Manager',
    'Sophos Viruscan - NETAPP NOC Dropbox',
    'Sophox Virus Scanner - Faspex Virus Scanner',
    'Stratus CLuster Node A',
    'Stratus CLuster Node B',
    'Symantec VIrus Scanner - Storage: USDRYNSNP002',
    'Symantec Viruscanner - NETAPP NOC Dropbox - Replaced USECLPAPW788',
    'Symantec Viruscanner - NETAPP NOC Dropbox - Replaced USECLPAPW789',
    'Symantec Viruscanner - NETAPP NOC Dropbox Virus Scanner - AV for VfiLer',
    'Transcode Agent',
    'Transcode Manager (Rhozet WFS)',
    'Unused',
    'Virus Scanner (USUSHNSLP013 & USUSHNSLP014) VM USHAPWP00653',
    'WFS Rhozet Agent',
]

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

    service = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    primary_application = models.CharField(max_length=100)
    is_virtual_machine = models.BooleanField(default=False)
    environment = models.CharField(max_length=4, choices=ENVIRONMENTS, default="Prod")
    location = models.CharField(max_length=40)
    data_center = models.CharField(max_length=30)
    operating_system = models.CharField(max_length=100)
    rack = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
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