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

RECORD_TYPES = [
    ('record:host', 'Host Record'),
    ('record:a', 'A Record')
]

CRED_TYPES = [
    ('ENABLE_SSH', 'ENABLE_SSH'),
    ('ENABLE_TELNET', 'ENABLE_TELNET'),
    ('SSH', 'SSH'),
    ('TELNET', 'TELNET')
]

AUTH_TYPES = [
    ('CP', 'CP'),
    ('GM', 'GM'),
    (None, 'NONE')
]

DELEGATED_SCOPES = [
    (None, 'NONE'),
    ('RECLAIMING', 'RECLAIMING'),
    ('ROOT', 'ROOT'),
    ('SUBTREE', 'SUBTREE)')
]

USAGE_CHOICES = [
    ('ADAPTER', 'ADAPTER'),
    ('DELEGATED', 'DELEGATED'),
    (None, 'NONE'),
    ('USED_BY', 'USED_BY')
]

AUTH_PROTOCOLS = [
    ('MD5', 'MD5'),
    (None, 'NONE'),
    ('SHA', 'SHA')
]

PRIVACY_PROTOCOLS = [
    ('3DES', '3DES'),
    ('AES', 'AES'),
    ('DES', 'DES'),
    (None, 'NONE')
]

HOST_FIELDS = {
    'aliases',
    'allow_telnet',
    'cli_credentials',
    'cloud_info',
    'comment',
    'configure_for_dns',
    'ddns_protected',
    'device_description',
    'device_location',
    'device_type',
    'device_vendor',
    'disable',
    'disable_discovery',
    'dns_aliases',
    'dns_name',
    'extattrs',
    'ipv4addrs',
    'ipv6addrs',
    'last_queried',
    'ms_ad_user_data',
    'name',
    'network_view',
    'rrset_order',
    'snmp3_credential',
    'snmp_credential',
    'ttl',
    'use_cli_credentials',
    'use_snmp3_credential',
    'use_snmp_credential',
    'use_ttl',
    'view',
    'zone',
}

IPV4_FIELDS = {
    'bootfile',
    'bootserver',
    'configure_for_dhcp',
    'deny_bootp',
    'discover_now_status',
    'discovered_data',
    'enable_pxe_lease_time',
    'host',
    'ignore_client_requested_options',
    'ipv4addr',
    'is_invalid_mac',
    'last_queried',
    'logic_filter_rules',
    'mac',
    'match_client',
    'ms_ad_user_data',
    'network',
    'network_view',
    'nextserver',
    'options',
    'pxe_lease_time',
    'reserved_interface',
    'use_bootfile',
    'use_bootserver',
    'use_deny_bootp',
    'use_for_ea_inheritance',
    'use_ignore_client_requested_options',
    'use_logic_filter_rules',
    'use_nextserver',
    'use_options',
    'use_pxe_lease_time',
    'discovered_data'
}

IPV6_FIELDS = {
    'address_type',
    'configure_for_dhcp',
    'discover_now_status',
    'discovered_data',
    'domain_name',
    'domain_name_servers',
    'duid',
    'host',
    'ipv6addr',
    'ipv6prefix',
    'ipv6prefix_bits',
    'last_queried',
    'match_client',
    'ms_ad_user_data',
    'network',
    'network_view',
    'options',
    'preferred_lifetime',
    'reserved_interface',
    'use_domain_name',
    'use_domain_name_servers',
    'use_for_ea_inheritance',
    'use_options',
    'use_preferred_lifetime',
    'use_valid_lifetime',
    'valid_lifetime'
}

A_FIELDS = {
    'aws_rte53_record_info',
    'cloud_info',
    'comment',
    'creation_time',
    'creator',
    'ddns_principal',
    'disable',
    'discovered_data',
    'dns_name',
    'extattrs',
    'forbid_reclamation',
    'ipv4addr',
    'last_queried',
    'ms_ad_user_data',
    'name',
    'reclaimable',
    'shared_record_group',
    'ttl',
    'use_ttl',
    'view',
    'zone'
}


# One of these to each CloudInformation
class DHCPMember(models.Model):
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "dhcpmember"


#One of these to each ApplicationServer
class CloudInformation(models.Model):
    authority_type = models.CharField(max_length=4, choices=AUTH_TYPES)
    delegated_member = models.ForeignKey(DHCPMember, null=True, blank=True)
    delegated_root = models.CharField(max_length=100, null=True, blank=True)
    delegated_scope = models.CharField(max_length=10, choices=DELEGATED_SCOPES, null=True, blank=True)
    mgmt_platform = models.CharField(max_length=100, null=True, blank=True)
    owned_by_adaptor = models.NullBooleanField(null=True, blank=True)
    tenant = models.CharField(max_length=100, null=True, blank=True)
    usage = models.CharField(max_length=9, choices=USAGE_CHOICES, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "cloudinformation"


#One of these to each ApplicationServer
class SNMP3Credential(models.Model):
    authentication_protocol = models.CharField(max_length=4, null=True, blank=True, choices=AUTH_PROTOCOLS)
    comment = models.TextField(null=True, blank=True)
    privacy_protocol = models.CharField(max_length=4, null=True, blank=True, choices=PRIVACY_PROTOCOLS)
    user = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "snmp3credential"


#One of these to each ApplicationServer
class SNMPCredential(models.Model):
    comment = models.TextField(null=True, blank=True)
    community_string = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "snmpcredential"


#One of these to each ApplicationServer
class AWSRTE53RecordInfo(models.Model):
    alias_target_dns_name = models.CharField(max_length=100, null=True, blank=True)
    alias_target_evaluate_target_health = models.NullBooleanField(null=True, blank=True)
    alias_target_hosted_zone_id = models.CharField(max_length=100, null=True, blank=True)
    failover = models.CharField(max_length=9, null=True, blank=True)
    geolocation_continent_code = models.CharField(max_length=100, null=True, blank=True)
    geolocation_subdivision_code = models.CharField(max_length=100, null=True, blank=True)
    health_check_id = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    set_identifier = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=5, null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "awsrte53recordinfo"


#One of these for each ipv4host/ipv6host/applicationserver (if a record)
class DiscoveredData(models.Model):
    ap_ip_address = models.GenericIPAddressField(max_length=100, null=True, blank=True)
    ap_name = models.CharField(max_length=100, null=True, blank=True)
    ap_ssid = models.CharField(max_length=100, null=True, blank=True)
    bridge_domain = models.CharField(max_length=100, null=True, blank=True)
    cisco_ise_endpoint_profile = models.CharField(max_length=100, null=True, blank=True)
    cisco_ise_security_group = models.CharField(max_length=100, null=True, blank=True)
    cisco_ise_session_state = models.CharField(max_length=100, null=True, blank=True)
    cisco_ise_ssid = models.CharField(max_length=100, null=True, blank=True)
    cmp_type = models.CharField(max_length=100, null=True, blank=True)
    device_contact = models.CharField(max_length=100, null=True, blank=True)
    device_model = models.CharField(max_length=100, null=True, blank=True)
    device_port_name = models.CharField(max_length=100, null=True, blank=True)
    device_port_type = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    device_vendor = models.CharField(max_length=100, null=True, blank=True)
    discovered_name = models.CharField(max_length=100, null=True, blank=True)
    discoverer = models.CharField(max_length=100, null=True, blank=True)
    duid = models.CharField(max_length=100, null=True, blank=True)
    endpoint_groups = models.CharField(max_length=100, null=True, blank=True)
    first_discovered = models.DateTimeField(null=True, blank=True, editable=False)
    iprg_no = models.PositiveIntegerField(null=True, blank=True)
    iprg_state = models.CharField(max_length=100, null=True, blank=True)
    iprg_type = models.CharField(max_length=100, null=True, blank=True)
    last_discovered = models.DateTimeField(null=True, blank=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True)
    mgmt_ip_address = models.GenericIPAddressField(null=True, blank=True)
    netbios_name = models.CharField(max_length=100, null=True, blank=True)
    network_component_contact = models.CharField(max_length=100, null=True, blank=True)
    network_component_description = models.TextField(null=True, blank=True)
    network_component_ip = models.GenericIPAddressField(null=True, blank=True)
    network_component_location = models.CharField(max_length=100, null=True, blank=True)
    network_component_model = models.CharField(max_length=100, null=True, blank=True)
    network_component_name = models.CharField(max_length=100, null=True, blank=True)
    network_component_port_description = models.TextField(null=True, blank=True)
    network_component_port_name = models.CharField(max_length=100, null=True, blank=True)
    network_component_port_number = models.PositiveIntegerField(null=True, blank=True)
    network_component_type = models.CharField(max_length=100, null=True, blank=True)
    network_component_vendor = models.CharField(max_length=100, null=True, blank=True)
    open_ports = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    port_duplex = models.CharField(max_length=100, null=True, blank=True)
    port_link_status = models.CharField(max_length=100, null=True, blank=True)
    port_speed = models.CharField(max_length=100, null=True, blank=True)
    port_status = models.CharField(max_length=100, null=True, blank=True)
    port_type = models.CharField(max_length=100, null=True, blank=True)
    port_vlan_description = models.CharField(max_length=100, null=True, blank=True)
    port_vlan_name = models.CharField(max_length=100, null=True, blank=True)
    port_vlan_number = models.PositiveIntegerField(null=True, blank=True)
    task_name = models.CharField(max_length=100, null=True, blank=True)
    tenant = models.CharField(max_length=100, null=True, blank=True)
    v_adapter = models.CharField(max_length=100, null=True, blank=True)
    v_cluster = models.CharField(max_length=100, null=True, blank=True)
    v_datacenter = models.CharField(max_length=100, null=True, blank=True)
    v_entity_name = models.CharField(max_length=100, null=True, blank=True)
    v_entity_type = models.CharField(max_length=100, null=True, blank=True)
    v_host = models.CharField(max_length=100, null=True, blank=True)
    v_switch = models.CharField(max_length=100, null=True, blank=True)
    vlan_port_group = models.CharField(max_length=100, null=True, blank=True)
    vmhost_ip_address = models.GenericIPAddressField(null=True, blank=True)
    vmhost_mac_address = models.CharField(max_length=100, null=True, blank=True)
    vmhost_name = models.CharField(max_length=100, null=True, blank=True)
    vmhost_nic_names = models.CharField(max_length=100, null=True, blank=True)
    vmhost_subnet_cidr = models.CharField(max_length=100, null=True, blank=True)
    vmi_id = models.CharField(max_length=100, null=True, blank=True)
    vmi_ip_type = models.CharField(max_length=100, null=True, blank=True)
    vmi_is_public_address = models.NullBooleanField(null=True, blank=True, default=False)
    tenant_id = models.CharField(max_length=100, null=True, blank=True)
    vport_conf_mode = models.CharField(max_length=100, null=True, blank=True)
    vport_conf_speed = models.PositiveIntegerField(null=True, blank=True)
    vport_link_status = models.CharField(max_length=100, null=True, blank=True)
    vport_mac_address = models.CharField(max_length=100, null=True, blank=True)
    vport_mode = models.CharField(max_length=100, null=True, blank=True)
    vport_name = models.CharField(max_length=100, null=True, blank=True)
    vport_speed = models.PositiveIntegerField(null=True, blank=True)
    vswitch_available_ports_count = models.PositiveIntegerField(null=True, blank=True)
    vswitch_id = models.CharField(max_length=100, null=True, blank=True)
    vswitch_ipv6_enabled = models.NullBooleanField(null=True, blank=True)
    vswitch_name = models.CharField(max_length=100, null=True, blank=True)
    vswitch_segment_id = models.CharField(max_length=100, null=True, blank=True)
    vswitch_segment_name = models.CharField(max_length=100, null=True, blank=True)
    vswitch_segment_port_group = models.CharField(max_length=100, null=True, blank=True)
    vswitch_segment_type = models.CharField(max_length=100, null=True, blank=True)
    vswitch_tep_dhcp_server = models.CharField(max_length=100, null=True, blank=True)
    vswitch_tep_ip = models.GenericIPAddressField(null=True, blank=True)
    vswitch_tep_multicast = models.CharField(max_length=100, null=True, blank=True)
    vswitch_tep_port_group = models.CharField(max_length=100, null=True, blank=True)
    vswitch_type_type = models.CharField(max_length=100, null=True, blank=True)
    vswitch_tep_vlan = models.CharField(max_length=100, null=True, blank=True)
    vswitch_type = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "discovereddata"



class ApplicationServer(models.Model):

    #TODO: Get rid of all these irrelevant fields
    #General Information
    service = models.CharField(max_length=100, null=True, blank=True)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    primary_application = models.CharField(max_length=100, null=True, blank=True)
    is_virtual_machine = models.NullBooleanField(choices=BOOL_WITH_NULL, default=None, null=True, blank=True)
    environment = models.CharField(max_length=4, choices=ENVIRONMENTS_WITH_NULL, default=None, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    #Location Information
    location = models.CharField(max_length=40, null=True, blank=True)
    data_center = models.CharField(max_length=30, null=True, blank=True)
    rack = models.CharField(max_length=20, null=True, blank=True)


    #Network Information
    network = models.CharField(max_length=4, choices=NETWORKS_WITH_NULL, default=None, null=True, blank=True)
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
    last_edited = models.DateTimeField(null=True, blank=True)

    #Infoblox Record Information
    cloud_information = models.ForeignKey(CloudInformation, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    ddns_protected = models.NullBooleanField(null=True, blank=True)
    disable = models.NullBooleanField(null=True, blank=True)
    last_queried = models.DateTimeField(null=True, blank=True)
    ms_ad_user_data = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    ttl = models.PositiveIntegerField(null=True, blank=True)
    use_ttl = models.NullBooleanField(null=True, blank=True)
    view = models.CharField(max_length=100, null=True, blank=True)
    zone = models.CharField(max_length=100, null=True, blank=True)

    #Infoblox Host Record Information
    ref = models.CharField(max_length=300, null=True, blank=True)
    allow_telnet = models.NullBooleanField(default=None, null=True, blank=True)
    configure_for_dns = models.NullBooleanField(null=True, blank=True)
    device_description = models.CharField(max_length=500, null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    device_vendor = models.CharField(max_length=100, null=True, blank=True)
    disable_discovery = models.NullBooleanField(null=True, blank=True)
    network_view = models.CharField(max_length=100, null=True, blank=True)
    rrset_order = models.CharField(max_length=6, default="cyclic", null=True, blank=True)
    snmp3_credential = models.ForeignKey(SNMP3Credential, null=True, blank=True)
    snmp_credential = models.ForeignKey(SNMPCredential, null=True, blank=True)
    use_cli_credentials = models.NullBooleanField(null=True, blank=True)
    use_snmp3_credential = models.NullBooleanField(null=True, blank=True)
    use_snmp_credential = models.NullBooleanField(null=True, blank=True)


    #Infoblox A Record Information
    aws_rte53_record_info = models.ForeignKey(AWSRTE53RecordInfo, null=True, blank=True)
    creation_time = models.DateTimeField(null=True, blank=True)
    creator = models.CharField(max_length=100, null=True, blank=True)
    ddns_principal = models.CharField(max_length=100, null=True, blank=True)
    discovered_data = models.ForeignKey(DiscoveredData, null=True, blank=True)
    forbid_reclamation = models.NullBooleanField(null=True, blank=True)
    ipv4addr = models.GenericIPAddressField(protocol='ipv4', null=True, blank=True)
    reclaimable = models.NullBooleanField(null=True, blank=True)
    shared_record_group = models.CharField(max_length=300, null=True, blank=True)


    def getAdditionalIPs(self):
        additional_ips = AdditionalIPs.objects.filter(application_server_id=self.id)
        return additional_ips

    def deleteWithForeign(self):
        ipv4addrs = self.ipv4hostaddress_set.all()
        for ipv4addr in ipv4addrs:
            if ipv4addr.discovered_data is not None:
                ipv4addr.discovered_data.delete()

        ipv6addrs = self.ipv6hostaddress_set.all()
        for ipv6addr in ipv6addrs:
            if ipv6addr.discovered_data is not None:
                ipv6addr.discovered_data.delete()

        if self.cloud_information is not None:
            cloud_info = self.cloud_information
            if cloud_info.delegated_member is not None:
                cloud_info.delegated_member.delete()
            cloud_info.delete()

        if self.discovered_data is not None:
            self.discovered_data.delete()
        if self.aws_rte53_record_info is not None:
            self.aws_rte53_record_info.delete()
        if self.snmp3_credential is not None:
            self.snmp3_credential.delete()
        if self.snmp_credential is not None:
            self.snmp_credential.delete()

        self.delete()

    class Meta:
        db_table = "applicationserver"


class AdditionalIPs(models.Model):
    application_server = models.ForeignKey(ApplicationServer, related_name="application_server", null=True, blank=True)
    label = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()

    class Meta:
        db_table = "additionalips"



class FilterProfile(models.Model):

    profile_name = models.CharField(max_length=100)
    all_fields = models.CharField(max_length=100, null=True, blank=True)

    #General Information
    service = models.CharField(max_length=100, null=True, blank=True)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    primary_application = models.CharField(max_length=100, null=True, blank=True)
    is_virtual_machine = models.NullBooleanField(choices=BOOL_WITH_NULL, default=None, null=True)
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

    class Meta:
        db_table = "filterprofile"



#------INFOBLOX STARTS HERE-------- (for the most part)


#Many of these to each ApplicationServer
class IPv4HostAddress(models.Model):
    application_server = models.ForeignKey(ApplicationServer, null=True, blank=True)
    ref = models.CharField(max_length=300, null=True, blank=True)
    bootfile = models.CharField(max_length=100, null=True, blank=True)
    bootserver = models.CharField(max_length=100, null=True, blank=True)
    configure_for_dhcp = models.NullBooleanField(null=True, blank=True)
    deny_bootp = models.NullBooleanField(null=True, blank=True)
    discover_now_status = models.CharField(max_length=100, null=True, blank=True)
    discovered_data = models.ForeignKey(DiscoveredData, null=True, blank=True)
    enable_pxe_lease_time = models.NullBooleanField(null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    ignore_client_requested_options = models.NullBooleanField(null=True, blank=True)
    ipv4addr = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    is_invalid_mac = models.NullBooleanField(null=True, blank=True)
    last_queried = models.DateTimeField(null=True, blank=True)
    mac = models.CharField(max_length=100, null=True, blank=True)
    match_client = models.CharField(max_length=100, null=True, blank=True)
    ms_ad_user_data = models.PositiveIntegerField(null=True, blank=True)
    network = models.CharField(max_length=100, null=True, blank=True)
    network_view = models.CharField(max_length=100, null=True, blank=True)
    nextserver = models.CharField(max_length=100, null=True, blank=True)
    pxe_lease_time = models.PositiveIntegerField(null=True, blank=True)
    reserved_interface = models.CharField(max_length=100, null=True, blank=True)
    use_bootfile = models.NullBooleanField(null=True, blank=True)
    use_deny_bootp = models.NullBooleanField(null=True, blank=True)
    use_for_ea_inheritance = models.NullBooleanField(null=True, blank=True)
    use_ignore_client_requested_options = models.NullBooleanField(null=True, blank=True)
    use_logic_filter_rules = models.NullBooleanField(null=True, blank=True)
    use_nextserver = models.NullBooleanField(null=True, blank=True)
    use_options = models.NullBooleanField(null=True, blank=True)
    use_pxe_lease_time = models.NullBooleanField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def deleteWithForeign(self):
        if self.discovered_data is not None:
            self.discovered_data.delete()
        self.delete()

    class Meta:
        db_table = "ipv4hostaddress"


#Many of these to each ApplicationServer
class IPv6HostAddress(models.Model):
    application_server = models.ForeignKey(ApplicationServer, null=True, blank=True)
    ref = models.CharField(max_length=300, null=True, blank=True)
    address_type = models.CharField(max_length=100, null=True, blank=True)
    configure_for_dhcp = models.NullBooleanField(null=True, blank=True)
    discover_now_status = models.CharField(max_length=100, null=True, blank=True)
    discovered_data = models.ForeignKey(DiscoveredData, null=True, blank=True)
    domain_name = models.CharField(max_length=100, null=True, blank=True)
    duid = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    ipv6addr = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    ipv6prefix = models.CharField(max_length=100, null=True, blank=True)
    ipv6prefix_bits = models.PositiveIntegerField(null=True, blank=True)
    last_queried = models.DateTimeField(null=True, blank=True)
    match_client = models.CharField(max_length=100, null=True, blank=True)
    ms_ad_user_data = models.PositiveIntegerField(null=True, blank=True)
    network = models.CharField(max_length=100, null=True, blank=True)
    network_view = models.CharField(max_length=100, null=True, blank=True)
    preferred_lifetime = models.PositiveIntegerField(null=True, blank=True)
    reserved_interface = models.CharField(max_length=100, null=True, blank=True)
    use_domain_name = models.NullBooleanField(null=True, blank=True)
    use_domain_name_servers = models.NullBooleanField(null=True, blank=True)
    use_for_ea_inheritance = models.NullBooleanField(null=True, blank=True)
    use_options = models.NullBooleanField(null=True, blank=True)
    use_preferred_lifetime = models.NullBooleanField(null=True, blank=True)
    use_valid_lifetime = models.NullBooleanField(null=True, blank=True)
    valid_lifetime = models.PositiveIntegerField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def deleteWithForeign(self):
        if self.discovered_data is not None:
            self.discovered_data.delete()
        self.delete()

    class Meta:
        db_table = "ipv6hostaddress"


#Many of these to each ipv4hostaddress
class LogicFilterRule(models.Model):
    ipv4_host_address = models.ForeignKey(IPv4HostAddress, null=True, blank=True)
    filter = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=6, null=True, blank=True)
    visible = models.BooleanField(default=False)


    class Meta:
        db_table = "logicfilterrule"


#Many of these to each ipv6hostaddress
class DomainNameServer(models.Model):
    ipv6_host_address = models.ForeignKey(IPv6HostAddress, null=True, blank=True)
    domain_name_server = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)


    class Meta:
        db_table = "domainnameserver"


#Many of these to each ipv4/ipv6 host address
class DHCPOption(models.Model):
    ipv4_host_address = models.ForeignKey(IPv4HostAddress, null=True, blank=True)
    ipv6_host_address = models.ForeignKey(IPv6HostAddress, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    num = models.PositiveIntegerField(null=True, blank=True)
    use_option = models.NullBooleanField(null=True, blank=True, default=False)
    value = models.CharField(max_length=100, null=True, blank=True)
    vendor_class = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)


    class Meta:
        db_table = "dhcpoption"



#Many of these to each ApplicationServer
class ExtensibleAttribute(models.Model):
    application_server = models.ForeignKey(ApplicationServer, null=True, blank=True)
    attribute_name = models.CharField(max_length=100, null=True, blank=True)
    attribute_value = models.CharField(max_length=500, null=True, blank=True)
    visible = models.BooleanField(default=False)


    class Meta:
        db_table = "extensibleattribute"


#Many of these to each ApplicationServer
class Alias(models.Model):
    application_server = models.ForeignKey(ApplicationServer, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "alias"


#Many of these to each ApplicationServer
class CliCredential(models.Model):
    application_server = models.ForeignKey(ApplicationServer, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    credential_type = models.CharField(max_length=13, null=True, blank=True, choices=CRED_TYPES)
    user = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "clicredential"



#TODO: Handle CNAME records









