from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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
    ('record:a', 'A Record'),
    ('record:cname', 'CNAME Record'),
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

CNAME_FIELDS = {
    'aws_rte53_record_info',
    'canonical',
    'cloud_info',
    'comment',
    'creation_time',
    'creator',
    'ddns_principal',
    'ddns_protected',
    'disable',
    'extattrs',
    'forbid_reclamation',
    'last_queried',
    'name',
    'reclaimable',
    'shared_record_group',
    'ttl',
    'use_ttl',
    'view',
    'zone'
}


#TODO: Use the ordering defined here in the future to make the ordering of the display of the columns consistent
APPLICATION_SERVER_FIELDS = [
    ('record_type', 'Record Type'),
    ('zone', 'Zone'),
    ('name', 'Name'),
    ('view', 'View'),
    ('last_pulled', 'Last Pulled'),
    ('ddns_protected', 'DDNS Protected'),
    ('disable', 'Disable'),
    ('last_queried', 'Last Queried'),
    ('ms_ad_user_data', 'MS Ad User Data'),
    ('ttl', 'TTL'),
    ('use_ttl', 'Use TTL'),
    ('creation_time', 'Creation Time'),
    ('creator', 'Creator'),
    ('ddns_principal', 'DDNS Principal'),
    ('reclaimable', 'Reclaimable'),
    ('shared_record_group', 'Shared Record Group'),
    ('forbid_reclamation', 'Forbid Reclamation'),
    ('ref', 'Reference'),
    ('allow_telnet', 'Allow Telnet'),
    ('configure_for_dns', 'Configure for DNS'),
    ('device_location', 'Device Location'),
    ('device_description', 'Device Description'),
    ('device_type', 'Device Type'),
    ('device_vendor', 'Device Vendor'),
    ('disable_discovery', 'Disable Discovery'),
    ('network_view', 'Network View'),
    ('rrset_order', 'RRSet Order'),
    ('use_cli_credentials', 'Use CLI Credentials'),
    ('use_snmp3_credential', 'Use SNMP3 Credential'),
    ('use_snmp_credential', 'Use SNMP Credential'),
    ('ipv4addr', 'IPv4 Address'),
    ('canonical', 'Canonical'),
    ('ipv4addrs', 'IPv4 Addresses'),
    ('ipv6addrs', 'IPv6 Addresses'),
    ('extattrs', 'Extensible Attributes'),
    ('aliases', 'Aliases'),
    ('cli_credentials', 'CLI Credentials'),
]

DISCOVERED_DATA_FIELDS = [
    ('ap_ip_address', 'AP IP Address'),
    ('ap_name', 'AP Name'),
    ('ap_ssid', 'AP SSID'),
    ('bridge_domain', 'Bridge Domain'),
    ('cisco_ise_endpoint', 'Cisco ISE Endpoint'),
    ('cisco_ise_security_group', 'Cisco ISE Security Group'),
    ('cisco_ise_session_store', 'Cisco ISE Session Store'),
    ('cisco_ise_ssid', 'Cisco ISE SSID'),
    ('cmp_type', 'CMP Type'),
    ('device_contact', 'Device Contact'),
    ('device_model', 'Device Model'),
    ('device_port_name', 'Device Port Name'),
    ('device_port_type', 'Device Port Type'),
    ('device_type', 'Device Type'),
    ('device_vendor', 'Device Vendor'),
    ('discovered_name', 'Discovered Name'),
    ('discoverer', 'Discoverer'),
    ('duid', 'DUID'),
    ('endpoint_groups', 'Endpoint Groups'),
    ('first_discovered', 'First Discovered'),
    ('iprg_no', 'IPRG Number'),
    ('iprg_state', 'IPRG State'),
    ('iprg_type', 'IPRG Type'),
    ('last_discovered', 'Last Discovered'),
    ('mac_address', 'Mac Address'),
    ('mgmt_ip_address', 'Management IP Address'),
    ('netbios_name', 'Netbios Name'),
    ('network_component_contact', 'Network Component Contact'),
    ('network_component_description', 'Network Component Description'),
    ('network_component_ip', 'Network Component IP'),
    ('network_component_location', 'Network Component Location'),
    ('network_component_model', 'Network Component Model'),
    ('network_component_name', 'Network Component Name'),
    ('network_component_port_description', 'Network Component Port Description'),
    ('network_component_port_name', 'Network Component Port Name'),
    ('network_component_port_number', 'Network Component Port Number'),
    ('network_component_type', 'Network Component Type'),
    ('network_component_vendor', 'Network Component Vendor'),
    ('open_ports', 'Open Ports'),
    ('os', 'OS'),
    ('port_duplex', 'Port Duplex'),
    ('port_link_status', 'Port Link Status'),
    ('port_speed', 'Port Speed'),
    ('port_status', 'Port Status'),
    ('port_type', 'Port Type'),
    ('port_vlan_description', 'Port VLAN Description'),
    ('port_vlan_name', 'Port VLAN Name'),
    ('port_vlan_number', 'Port VLAN Number'),
    ('task_name', 'Task Name'),
    ('tenant', 'Tenant'),
    ('v_adapter', 'V Adapter'),
    ('v_cluster', 'V Cluster'),
    ('v_datacenter', 'V Datacenter'),
    ('v_entity_name', 'V Entity Name'),
    ('v_entity_type', 'V_Entity Type'),
    ('v_host', 'V Host'),
    ('v_switch', 'V Switch'),
    ('vlan_port_group', 'VLAN Port Group'),
    ('vmhost_ip_address', 'VM Host IP Address'),
    ('vmhost_mac_address', 'VM Host Mac Address'),
    ('vmhost_ip_address', 'VM Host IP Address'),
    ('vmhost_mac_address', 'VM Host IP Address'),
    ('vmhost_name', 'VM Host Name'),
    ('vmhost_nic_names', 'VM Host NIC Names'),
    ('vmhost_subnet_cidr', 'VM Host Subnet CIDR'),
    ('vmi_id', 'VMI ID'),
    ('vmi_ip_type', 'VMI IP Type'),
    ('vmi_is_public_address', 'VMI Is Public Address'),
    ('tenant_id', 'Tenant ID'),
    ('vport_conf_mode', 'VPort Conf Mode'),
    ('vport_conf_speed', 'VPort Conf Speed'),
    ('vport_link_status', 'VPort Link Status'),
    ('vport_mac_address', 'VPort Mac Address'),
    ('vport_mode', 'VPort Mode'),
    ('vport_name', 'VPort Name'),
    ('vport_speed', 'VPort Speed'),
    ('vswitch_available_ports_count', 'VSwitch Available Port Count'),
    ('vswitch_id', 'VSwitch ID'),
    ('vswitch_ipv6_enabled', 'VSwitch IPv6 Enabled'),
    ('vswitch_name', 'VSwitch Name'),
    ('vswitch_segment_id', 'VSwitch Segment ID'),
    ('vswitch_segment_name', 'VSwitch Segment Name'),
    ('vswitch_segment_port_group', 'VSwitch Segment Port Group'),
    ('vswitch_segment_type', 'VSwitch Segment Type'),
    ('vswitch_tep_dhcp_server', 'VSwitch TEP DHCP Server'),
    ('vswitch_tep_ip', 'VSwitch TEP IP'),
    ('vswitch_tep_multicast', 'VSwitch TEP Multicast'),
    ('vswitch_tep_port_group', 'VSwitch TEP Port Group'),
    ('vswitch_tep_type', 'VSwitch TEP Type'),
    ('vswitch_tep_vlan', 'VSwitch TEP VLAN'),
    ('vswitch_type', 'VSwitch Type')
]



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
    authority_type = models.CharField(max_length=4)
    delegated_member = models.ForeignKey(DHCPMember, null=True, blank=True)
    delegated_root = models.CharField(max_length=100, null=True, blank=True)
    delegated_scope = models.CharField(max_length=10, null=True, blank=True)
    mgmt_platform = models.CharField(max_length=100, null=True, blank=True)
    owned_by_adaptor = models.NullBooleanField(null=True, blank=True)
    tenant = models.CharField(max_length=100, null=True, blank=True)
    usage = models.CharField(max_length=9, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "cloudinformation"


#One of these to each ApplicationServer
class SNMP3Credential(models.Model):
    authentication_protocol = models.CharField(max_length=4, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    privacy_protocol = models.CharField(max_length=4, null=True, blank=True)
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
    vswitch_tep_type = models.CharField(max_length=100, null=True, blank=True)
    vswitch_tep_vlan = models.CharField(max_length=100, null=True, blank=True)
    vswitch_type = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "discovereddata"


#One of these to each user - defines column visibility preferences
class VisibleColumns(models.Model):

    #Associate Visible Column Preference with a User
    user = models.OneToOneField(User, null=True, blank=True)

    #Infoblox Record Information
    name = models.BooleanField(default=True)
    view = models.BooleanField(default=True)
    zone = models.BooleanField(default=True)
    record_type = models.BooleanField(default=True)
    ddns_protected = models.BooleanField(default=True)
    disable = models.BooleanField(default=True)
    last_queried = models.BooleanField(default=True)
    ms_ad_user_data = models.BooleanField(default=True)
    ttl = models.BooleanField(default=True)
    use_ttl = models.BooleanField(default=True)
    creation_time = models.BooleanField(default=True)
    creator = models.BooleanField(default=True)
    ddns_principal = models.BooleanField(default=True)
    reclaimable = models.BooleanField(default=True)
    shared_record_group = models.BooleanField(default=True)
    forbid_reclamation = models.BooleanField(default=True)

    #One-to-Many Fields
    ipv4addrs = models.BooleanField(default=True)
    ipv6addrs = models.BooleanField(default=True)
    extattrs = models.BooleanField(default=True)
    aliases = models.BooleanField(default=True)
    cli_credentials = models.BooleanField(default=True)

    #Infoblox A Record Information (Only for A Records)
    ipv4addr = models.BooleanField(default=True)

    #Logistical Information
    last_pulled = models.BooleanField(default=True)

    #Infoblox Host Record Information (Only for Host Records)
    ref = models.BooleanField(default=True)
    allow_telnet = models.BooleanField(default=True)
    configure_for_dns = models.BooleanField(default=True)
    device_location = models.BooleanField(default=True)
    device_description = models.BooleanField(default=True)
    device_type = models.BooleanField(default=True)
    device_vendor = models.BooleanField(default=True)
    disable_discovery = models.BooleanField(default=True)
    network_view = models.BooleanField(default=True)
    rrset_order = models.BooleanField(default=True)
    use_cli_credential = models.BooleanField(default=True)
    use_snmp3_credential = models.BooleanField(default=True)
    use_snmp_credential = models.BooleanField(default=True)

    #Infoblox CName Record Information (Only for CNAME Records)
    canonical = models.BooleanField(default=True)

    class Meta:
        db_table = "visiblecolumns"






class ApplicationServer(models.Model):

    #Visible Boolean
    visible = models.BooleanField(default=True)

    #Logistical Information
    last_pulled = models.DateTimeField(null=True, blank=True)

    #Infoblox Record Information (In two or more record types)
    record_type = models.CharField(max_length=15, null=True, blank=True)
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
    creation_time = models.DateTimeField(null=True, blank=True)
    creator = models.CharField(max_length=100, null=True, blank=True)
    ddns_principal = models.CharField(max_length=100, null=True, blank=True)
    reclaimable = models.NullBooleanField(null=True, blank=True)
    shared_record_group = models.CharField(max_length=300, null=True, blank=True)
    forbid_reclamation = models.NullBooleanField(null=True, blank=True)

    #Infoblox Host Record Information (only for host records)
    ref = models.CharField(max_length=300, null=True, blank=True)
    allow_telnet = models.NullBooleanField(default=None, null=True, blank=True)
    configure_for_dns = models.NullBooleanField(null=True, blank=True)
    device_location = models.CharField(max_length=100, null=True, blank=True)
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

    #Infoblox A Record Information (only for a records)
    aws_rte53_record_info = models.ForeignKey(AWSRTE53RecordInfo, null=True, blank=True)
    discovered_data = models.ForeignKey(DiscoveredData, null=True, blank=True)
    ipv4addr = models.GenericIPAddressField(protocol='ipv4', null=True, blank=True)

    #Infoblox CName Record Information (Only for cname records)
    canonical = models.CharField(max_length=100, null=True, blank=True)

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

    def getIPv4Addresses(self):
        return self.ipv4hostaddress_set.values_list('host', 'ipv4addr').all()

    def getIPv6Addresses(self):
        return self.ipv6hostaddress_set.values_list('host', 'ipv6addr').all()

    def getAliases(self):
        return self.alias_set.values_list('alias').all()

    def getExtensibleAttributes(self):
        # print(self.extensibleattribute_set.values.all())
        return self.extensibleattribute_set.values_list('attribute_name', 'attribute_value').all()

    def getCliCredentials(self):
        return self.clicredential_set.values_list('credential_type', 'user').all()



    class Meta:
        db_table = "applicationserver"



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
    credential_type = models.CharField(max_length=13, null=True, blank=True)
    user = models.CharField(max_length=100, null=True, blank=True)
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "clicredential"


#When user is created, make a visiblecolumn preference for them
def create_visible_column(sender, **kwargs):
    if kwargs['created']:
        VisibleColumns.objects.create(user=kwargs['instance'])


post_save.connect(create_visible_column, sender=User)












