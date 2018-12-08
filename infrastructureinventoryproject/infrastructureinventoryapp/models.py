from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


CLI_CREDENTIAL_TYPES = [
    (None, 'N/A'),
    ('ENABLE_SSH', 'ENABLE_SSH'),
    ('ENABLE_TELNET', 'ENABLE_TELNET'),
    ('SSH', 'SSH'),
    ('TELNET', 'TELNET'),
]

CISCO_ISE_SESSION_STATES = [
    (None, 'N/A'),
    ('AUTHENTICATED', 'AUTHENTICATED'),
    ('AUTHENTICATING', 'AUTHENTICATING'),
    ('DISCONNECTED', 'DISCONNECTED'),
    ('POSTURED', 'POSTURED'),
    ('STARTED', 'STARTED'),
]

ENVIRONMENTS = [
    ('Prod', 'Production'),
    ('Dev', 'Development'),
    ('QA', 'Quality Assurance'),
]

ADDRESS_TYPES = [
    (None, 'N/A'),
    ('ADDRESS', 'ADDRESS'),
    ('BOTH', 'BOTH'),
    ('PREFIX', 'PREFIX'),
]

ENVIRONMENTS_WITH_NULL = [
    ('Prod', 'Production'),
    ('Dev', 'Development'),
    ('QA', 'Quality Assurance'),
    (None, 'N/A')
]

VPORT_MODES = [
    (None, 'N/A'),
    ('Full-duplex', 'Full-duplex'),
    ('Half-duplex', 'Half-duplex'),
    ('Unknown', 'Unknown'),
]

VSWITCH_TYPES = [
    (None, 'N/A'),
    ('Distributed', 'Distributed'),
    ('Standard', 'Standard'),
    ('Unknown', 'Unknown'),
]

DISCOVER_NOW_STATUSES = [
    (None, 'N/A'),
    ('COMPLETE', 'COMPLETE'),
    ('FAILED', 'FAILED'),
    ('NONE', 'NONE'),
    ('PENDING', 'PENDING'),
    ('RUNNING', 'RUNNING'),
]

DHCP_USE_OPTIONS = [
    (None, 'N/A'),
    ('routers', 'routers'),
    ('router-templates', 'router-templates'),
    ('domain-name-servers', 'domain-name-servers'),
    ('domain-name', 'domain-name'),
    ('broadcast-address', 'broadcast-address'),
    ('broadcast-address-offset', 'broadcast-address-offset'),
    ('dhcp-lease-time', 'dhcp-lease-time'),
    ('dhcp6.name-servers', 'dhcp6.name-servers'),
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

LOGIC_FILTER_RULE_TYPES = [
    (None, 'N/A'),
    ('MAC', 'MAC'),
    ('NAC', 'NAC'),
    ('Option', 'Option'),
]


BOOL = [
    (0, 'No'),
    (1, 'Yes'),
]

BOOL_WITH_NULL = [
    (None, 'N/A'),
    (1, 'Yes'),
    (0, 'No'),
]

RECORD_TYPES = [
    ('record:host', 'Host Record'),
    ('record:a', 'A Record'),
    ('record:cname', 'CNAME Record'),
]

AUTHORITY_TYPES = [
    (None, 'N/A'),
    ('CP', 'CP'),
    ('GM', 'GM'),
    ('NONE', 'None'),
]

DELEGATED_SCOPES = [
    (None, 'N/A'),
    ('NONE', 'NONE'),
    ('RECLAIMING', 'RECLAIMING'),
    ('ROOT', 'ROOT'),
    ('SUBTREE', 'SUBTREE'),
]

USAGES = [
    (None, 'N/A'),
    ('ADAPTER', 'ADAPTER'),
    ('DELEGATED', 'DELEGATED'),
    ('NONE', 'NONE'),
    ('USED_BY', 'USED_BY'),
]

AUTHENTICATION_PROTOCOLS = [
    (None, 'N/A'),
    ('MD5', 'MD5'),
    ('NONE', 'NONE'),
    ('SHA', 'SHA'),
]

PRIVACY_PROTOCOLS = [
    (None, 'N/A'),
    ('3DES', '3DES'),
    ('AES', 'AES'),
    ('DES', 'DES'),
    ('NONE', 'NONE'),
]

FAILOVERS = [
    (None, 'N/A'),
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY')
]

AWS_TYPES = [
    (None, 'N/A'),
    ('A', 'A'),
    ('AAAA', 'AAAA'),
    ('CNAME', 'CNAME'),
    ('MX', 'MX'),
    ('NS', 'NS'),
    ('PTR', 'PTR'),
    ('SOA', 'SOA'),
    ('SPF', 'SPF'),
    ('SRV', 'SRV'),
    ('TXT', 'TXT')
]

FILTER_RECORD_TYPES = [
    (None, 'N/A'),
    ('Host Record', 'Host Record'),
    ('A Record', 'A Record'),
    ('CNAME Record', 'CNAME Record'),
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
    ('ipv4addr', 'IPv4 Address'),
    ('host', 'Host'),
    ('network', 'Network'),
    ('network_view', 'Network View'),
    ('mac', 'Mac'),
    ('last_queried', 'Last Queried'),
    ('bootfile', 'Bootfile'),
    ('bootserver', 'Bootserver'),
    ('configure_for_dhcp', 'Configure for DHCP'),
    ('deny_bootp', 'Deny BOOTP'),
    ('discover_now_status', 'Discover Now Status'),
    ('discovered_data', 'Discovered Data'),
    ('enable_pxe_lease_time', 'Enable PXE Lease Time'),
    ('ignore_client_requested_options', 'Ignore Client Requested Options'),
    ('is_invalid_mac', 'Is Invalid Mac'),
    ('logic_filter_rules', 'Logic Filter Rules'),
    ('match_client', 'Match Client'),
    ('ms_ad_user_data', 'MS AD User Count'),
    ('nextserver', 'Next Server'),
    ('options', 'Options'),
    ('pxe_lease_time', 'PXE Lease Time'),
    ('reserved_interface', 'Reserved Interface'),
    ('use_bootfile', 'Use Bootfile'),
    ('use_bootserver', 'Use Bootserver'),
    ('use_deny_bootp', 'Use Deny BOOTP'),
    ('use_for_ea_inheritance', 'Use For EA Inheritance'),
    ('use_ignore_client_requested_options', 'Use Ignore Client Requested Options'),
    ('use_logic_filter_rules', 'Use Logic Filter Rules'),
    ('use_nextserver', 'Use Next Server'),
    ('use_options', 'Use Options'),
    ('use_pxe_lease_time', 'Use PXE Lease Time'),
}

IPV6_FIELDS = [
    ('ipv6addr', 'IPv6 Address'),
    ('host', 'Host'),
    ('address_type','Address Type'),
    ('domain_name', 'Domain Name'),
    ('last_queried', 'Last Queried'),
    ('configure_for_dhcp','Configure for DHCP'),
    ('discover_now_status', 'Discover Now Status'),
    ('discovered_data', 'Discovered Data'),
    ('domain_name_servers', 'Domain Name Servers'),
    ('duid', 'DUID'),
    ('ipv6prefix', 'IPv6 Prefix'),
    ('ipv6prefix_bits', 'IPv6 Prefix Bits'),
    ('match_client', 'Match Client'),
    ('ms_ad_user_data', 'MS AD User Count'),
    ('network', 'Network'),
    ('network_view', 'Network View'),
    ('options', 'Options'),
    ('preferred_lifetime', 'Preferred Lifetime'),
    ('reserved_interface', 'Reserved Interface'),
    ('use_domain_name', 'Use Domain Name'),
    ('use_domain_name_servers', 'Use Domain Name Servers'),
    ('use_for_ea_inheritance', 'Use for EA Inheritance'),
    ('use_options', 'Use Options'),
    ('use_preferred_lifetime', 'Use Preferred Lifetime'),
    ('use_valid_lifetime', 'Use Valid Lifetime'),
    ('valid_lifetime', 'Valid Lifetime')
]

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

RRSET_ORDERS = [
    (None, 'N/A'),
    ('cyclic', 'Cyclic'),
    ('random', 'Random'),
    ('fixed', 'Fixed'),
]

CLOUD_INFORMATION_FIELDS = [
    ('authority_type', 'Authority Type'),
    ('delegated_root', 'Delegated Root'),
    ('delegated_scope', 'Delegated Scope'),
    ('mgmt_platform', 'Management Platform'),
    ('owned_by_adaptor', 'Owned By Adaptor'),
    ('tenant', 'Tenant'),
    ('usage_field', 'Usage'),
    ('delegated_member', 'Delegated Member')
]

DHCP_MEMBER_FIELDS = [
    ('ipv4_address', 'Delegated Member IPv4 Address'),
    ('ipv6_address', 'Delegated Member IPv6 Address'),
    ('name', 'Delegated Member Name'),
]

SNMP3_CREDENTIAL_FIELDS = [
    ('authentication_protocol', 'Authentication Protocol'),
    ('privacy_protocol', 'Privacy Protocol'),
    ('user', 'SNMP3 User'),
    ('comment', 'Comment')
]

SNMP_CREDENTIAL_FIELDS = [
    ('community_string', 'Community String'),
    ('comment', 'Comment'),
]

AWS_RTE53_RECORD_INFO_FIELDS = [
    ('type', 'Type'),
    ('region', 'Region'),
    ('weight', 'Weight'),
    ('alias_target_dns_name', 'Alias Target DNS Name'),
    ('alias_target_evaluate_target_health', 'Alias Target Evaluate Target Health'),
    ('alias_target_hosted_zone_id', 'Alias Target Hosted Zone ID'),
    ('failover', 'Failover'),
    ('geolocation_continent_code', 'Geolocation Continent Code'),
    ('geolocation_country_code', 'Geolocation Country Code'),
    ('geolocation_subdivision_code', 'Geolocation Subdivision Code'),
    ('health_check_id', 'Health Check ID'),
    ('set_identifier', 'Set Identifier')
]

LOGIC_FILTER_RULE_FIELDS = [
    ('filter', 'Filter'),
    ('type', 'Type')
]

DHCP_OPTION_FIELDS = [
    ('name', 'Name'),
    ('num', 'Num'),
    ('use_option', 'Use Option'),
    ('value', 'Value'),
    ('vendor_class', 'Vendor Class')
]

DOMAIN_NAME_SERVER_FIELDS = [
    ('domain_name_server', 'Domain Name Server')
]


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
    ('ms_ad_user_data', 'MS Ad User Count'),
    ('ttl', 'TTL'),
    ('use_ttl', 'Use TTL'),
    ('creation_time', 'Creation Time'),
    ('creator', 'Creator'),
    ('ddns_principal', 'DDNS Principal'),
    ('reclaimable', 'Reclaimable'),
    ('shared_record_group', 'Shared Record Group'),
    ('forbid_reclamation', 'Forbid Reclamation'),
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
    ('ref', 'Reference'),
]

DISCOVERED_DATA_FIELDS = [
    ('ap_ip_address', 'AP IP Address'),
    ('ap_name', 'AP Name'),
    ('ap_ssid', 'AP SSID'),
    ('bridge_domain', 'Bridge Domain'),
    ('cisco_ise_endpoint_profile', 'Cisco ISE Endpoint Profile'),
    ('cisco_ise_security_group', 'Cisco ISE Security Group'),
    ('cisco_ise_session_state', 'Cisco ISE Session State'),
    ('cisco_ise_ssid', 'Cisco ISE SSID'),
    ('cmp_type', 'CMP Type'),
    ('device_contact', 'Device Contact'),
    ('device_location', 'Device Location'),
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
    ('vmhost_name', 'VM Host Name'),
    ('vmhost_nic_names', 'VM Host NIC Names'),
    ('vmhost_subnet_cidr', 'VM Host Subnet CIDR'),
    ('vmi_id', 'VMI ID'),
    ('vmi_ip_type', 'VMI IP Type'),
    ('vmi_is_public_address', 'VMI Is Public Address'),
    ('vmi_name', 'VMI Name'),
    ('vmi_private_address', 'VMI Private Address'),
    ('vmi_tenant_id', 'VMI Tenant ID'),
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


#Holds Views and Zones from Infoblox
class AuthoritativeZone(models.Model):
    view = models.CharField(max_length=20)
    zone = models.CharField(max_length=150)
    last_host_pull = models.DateTimeField(null=True)
    last_a_pull = models.DateTimeField(null=True)
    last_cname_pull = models.DateTimeField(null=True)

    class Meta:
        db_table = "authoritativezone"


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
    usage_field = models.CharField(max_length=9, null=True, blank=True)
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
    geolocation_country_code = models.CharField(max_length=100, null=True, blank=True)
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
    device_location = models.CharField(max_length=100, null=True, blank=True)
    device_port_name = models.CharField(max_length=100, null=True, blank=True)
    device_port_type = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    device_vendor = models.CharField(max_length=100, null=True, blank=True)

    discovered_name = models.CharField(max_length=100, null=True, blank=True)
    discoverer = models.CharField(max_length=100, null=True, blank=True)
    duid = models.CharField(max_length=100, null=True, blank=True)
    endpoint_groups = models.CharField(max_length=100, null=True, blank=True)
    first_discovered = models.DateTimeField(null=True, blank=True)
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
    vmi_is_public_address = models.NullBooleanField(null=True, blank=True)
    vmi_name = models.NullBooleanField(null=True, blank=True)
    vmi_private_address = models.NullBooleanField(null=True, blank=True)
    vmi_tenant_id = models.CharField(max_length=100, null=True, blank=True)
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
    ddns_protected = models.BooleanField(default=False)
    disable = models.BooleanField(default=False)
    last_queried = models.BooleanField(default=False)
    ms_ad_user_data = models.BooleanField(default=False)
    ttl = models.BooleanField(default=False)
    use_ttl = models.BooleanField(default=False)
    creation_time = models.BooleanField(default=False)
    creator = models.BooleanField(default=False)
    ddns_principal = models.BooleanField(default=False)
    reclaimable = models.BooleanField(default=False)
    shared_record_group = models.BooleanField(default=False)
    forbid_reclamation = models.BooleanField(default=False)

    #Infoblox A Record Information (Only for A Records)
    ipv4addr = models.BooleanField(default=True)

    #Logistical Information
    last_pulled = models.BooleanField(default=True)

    #Infoblox Host Record Information (Only for Host Records)
    ref = models.BooleanField(default=False)
    allow_telnet = models.BooleanField(default=False)
    configure_for_dns = models.BooleanField(default=False)
    device_location = models.BooleanField(default=False)
    device_description = models.BooleanField(default=False)
    device_type = models.BooleanField(default=False)
    device_vendor = models.BooleanField(default=False)
    disable_discovery = models.BooleanField(default=False)
    network_view = models.BooleanField(default=False)
    rrset_order = models.BooleanField(default=False)
    use_cli_credential = models.BooleanField(default=False)
    use_snmp3_credential = models.BooleanField(default=False)
    use_snmp_credential = models.BooleanField(default=False)

    #Infoblox CName Record Information (Only for CNAME Records)
    canonical = models.BooleanField(default=False)

    #One-to-Many Fields
    ipv4addrs = models.BooleanField(default=False)
    ipv6addrs = models.BooleanField(default=False)
    extattrs = models.BooleanField(default=False)
    aliases = models.BooleanField(default=False)
    cli_credentials = models.BooleanField(default=False)

    #Cloud Information Fields
    ci_authority_type = models.BooleanField(default=False)
    ci_delegated_root = models.BooleanField(default=False)
    ci_delegated_scope = models.BooleanField(default=False)
    ci_mgmt_platform = models.BooleanField(default=False)
    ci_owned_by_adaptor = models.BooleanField(default=False)
    ci_tenant = models.BooleanField(default=False)
    ci_usage_field = models.BooleanField(default=False)

    #Delegated Member Fields
    dm_ipv4_address = models.BooleanField(default=False)
    dm_ipv6_address = models.BooleanField(default=False)
    dm_name = models.BooleanField(default=False)

    #SNMP3 Credential Fields
    snmp3_authentication_protocol = models.BooleanField(default=False)
    snmp3_privacy_protocol = models.BooleanField(default=False)
    snmp3_user = models.BooleanField(default=False)

    #AWS RTE53 Record Info Fields
    aws_alias_target_dns_name = models.BooleanField(default=False)
    aws_alias_target_evaluate_target_health = models.BooleanField(default=False)
    aws_alias_target_hosted_zone_id = models.BooleanField(default=False)
    aws_failover = models.BooleanField(default=False)
    aws_geolocation_continent_code = models.BooleanField(default=False)
    aws_geolocation_country_code = models.BooleanField(default=False)
    aws_geolocation_subdivision_code = models.BooleanField(default=False)
    aws_health_check_id = models.BooleanField(default=False)
    aws_region= models.BooleanField(default=False)
    aws_set_identifier = models.BooleanField(default=False)
    aws_type = models.BooleanField(default=False)
    aws_weight = models.BooleanField(default=False)

    #Discovered Data Fields
    dd_ap_ip_address = models.BooleanField(default=False)
    dd_ap_name = models.BooleanField(default=False)
    dd_ap_ssid = models.BooleanField(default=False)
    dd_bridge_domain = models.BooleanField(default=False)
    dd_cisco_ise_endpoint_profile = models.BooleanField(default=False)
    dd_cisco_ise_security_group = models.BooleanField(default=False)
    dd_cisco_ise_session_state = models.BooleanField(default=False)
    dd_cisco_ise_ssid = models.BooleanField(default=False)
    dd_cmp_type = models.BooleanField(default=False)
    dd_device_contact = models.BooleanField(default=False)
    dd_device_model = models.BooleanField(default=False)
    dd_device_location = models.BooleanField(default=False)
    dd_device_port_name = models.BooleanField(default=False)
    dd_device_port_type = models.BooleanField(default=False)
    dd_device_type = models.BooleanField(default=False)
    dd_device_vendor = models.BooleanField(default=False)
    dd_discovered_name = models.BooleanField(default=False)
    dd_discoverer = models.BooleanField(default=False)
    dd_duid = models.BooleanField(default=False)
    dd_endpoint_groups = models.BooleanField(default=False)
    dd_iprg_no = models.BooleanField(default=False)
    dd_iprg_state = models.BooleanField(default=False)
    dd_iprg_type = models.BooleanField(default=False)
    dd_mac_address = models.BooleanField(default=False)
    dd_mgmt_ip_address = models.BooleanField(default=False)
    dd_netbios_name = models.BooleanField(default=False)
    dd_network_component_contact = models.BooleanField(default=False)
    dd_network_component_description = models.BooleanField(default=False)
    dd_network_component_ip = models.BooleanField(default=False)
    dd_network_component_location = models.BooleanField(default=False)
    dd_network_component_model = models.BooleanField(default=False)
    dd_network_component_name = models.BooleanField(default=False)
    dd_network_component_port_description = models.BooleanField(default=False)
    dd_network_component_port_name = models.BooleanField(default=False)
    dd_network_component_port_number = models.BooleanField(default=False)
    dd_network_component_type = models.BooleanField(default=False)
    dd_network_component_vendor = models.BooleanField(default=False)
    dd_open_ports = models.BooleanField(default=False)
    dd_os = models.BooleanField(default=False)
    dd_port_duplex = models.BooleanField(default=False)
    dd_port_link_status = models.BooleanField(default=False)
    dd_port_speed = models.BooleanField(default=False)
    dd_port_status = models.BooleanField(default=False)
    dd_port_type = models.BooleanField(default=False)
    dd_port_vlan_description = models.BooleanField(default=False)
    dd_port_vlan_name = models.BooleanField(default=False)
    dd_port_vlan_number = models.BooleanField(default=False)
    dd_task_name = models.BooleanField(default=False)
    dd_tenant = models.BooleanField(default=False)
    dd_v_adapter = models.BooleanField(default=False)
    dd_v_cluster = models.BooleanField(default=False)
    dd_v_datacenter = models.BooleanField(default=False)
    dd_v_entity_name = models.BooleanField(default=False)
    dd_v_entity_type = models.BooleanField(default=False)
    dd_v_host = models.BooleanField(default=False)
    dd_v_switch = models.BooleanField(default=False)
    dd_vlan_port_group = models.BooleanField(default=False)
    dd_vmhost_ip_address = models.BooleanField(default=False)
    dd_vmhost_mac_address = models.BooleanField(default=False)
    dd_vmhost_name = models.BooleanField(default=False)
    dd_vmhost_nic_names = models.BooleanField(default=False)
    dd_vmhost_subnet_cidr = models.BooleanField(default=False)
    dd_vmi_id = models.BooleanField(default=False)
    dd_vmi_ip_type = models.BooleanField(default=False)
    dd_vmi_is_public_address = models.BooleanField(default=False)
    dd_vmi_name = models.BooleanField(default=False)
    dd_vmi_private_address = models.BooleanField(default=False)
    dd_vmi_tenant_id = models.BooleanField(default=False)
    dd_vport_conf_mode = models.BooleanField(default=False)
    dd_vport_conf_speed = models.BooleanField(default=False)
    dd_vport_link_status = models.BooleanField(default=False)
    dd_vport_mac_address = models.BooleanField(default=False)
    dd_vport_mode = models.BooleanField(default=False)
    dd_vport_name = models.BooleanField(default=False)
    dd_vport_speed = models.BooleanField(default=False)
    dd_vswitch_available_ports_count = models.BooleanField(default=False)
    dd_vswitch_id = models.BooleanField(default=False)
    dd_vswitch_ipv6_enabled = models.BooleanField(default=False)
    dd_vswitch_name = models.BooleanField(default=False)
    dd_vswitch_segment_id = models.BooleanField(default=False)
    dd_vswitch_segment_name = models.BooleanField(default=False)
    dd_vswitch_segment_port_group = models.BooleanField(default=False)
    dd_vswitch_segment_type = models.BooleanField(default=False)
    dd_vswitch_tep_dhcp_server = models.BooleanField(default=False)
    dd_vswitch_tep_ip = models.BooleanField(default=False)
    dd_vswitch_tep_multicast = models.BooleanField(default=False)
    dd_vswitch_tep_port_group = models.BooleanField(default=False)
    dd_vswitch_tep_type = models.BooleanField(default=False)
    dd_vswitch_tep_vlan = models.BooleanField(default=False)
    dd_vswitch_type = models.BooleanField(default=False)

    #SNMP Credential Fields
    snmp_community_string = models.BooleanField(default=True)

    class Meta:
        db_table = "visiblecolumns"






class ApplicationServer(models.Model):

    #Visible Boolean
    visible = models.BooleanField(default=True)

    #Logistical Information
    last_pulled = models.DateTimeField(null=True, blank=True)

    #Infoblox Record Information (In two or more record types)
    record_type = models.CharField(max_length=15, choices=RECORD_TYPES, null=True, blank=True)
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
        return self.ipv4hostaddress_set.values_list('ipv4addr').filter(visible=True)

    def getIPv6Addresses(self):
        return self.ipv6hostaddress_set.values_list('ipv6addr').filter(visible=True)

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

    #Filter Profile Information
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    all_fields = models.CharField(max_length=100, null=True, blank=True)

    #Infoblox Record Information (In two or more record types)
    record_type = models.CharField(max_length=15, choices=FILTER_RECORD_TYPES, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    view = models.CharField(max_length=100, null=True, blank=True)
    zone = models.CharField(max_length=100, null=True, blank=True)
    ddns_protected = models.NullBooleanField(null=True, blank=True)
    disable = models.NullBooleanField(null=True, blank=True)
    ms_ad_user_data = models.PositiveIntegerField(null=True, blank=True)
    ttl = models.PositiveIntegerField(null=True, blank=True)
    use_ttl = models.NullBooleanField(null=True, blank=True)
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
    rrset_order = models.CharField(max_length=6, null=True, blank=True, choices=RRSET_ORDERS)
    use_cli_credentials = models.NullBooleanField(null=True, blank=True)
    use_snmp3_credential = models.NullBooleanField(null=True, blank=True)
    use_snmp_credential = models.NullBooleanField(null=True, blank=True)

    #A Record informaiton
    ipv4addr = models.CharField(max_length=30, null=True, blank=True)

    #Many to One Fields
    alias = models.CharField(max_length=100, null=True, blank=True)
    extensible_attribute_value = models.CharField(max_length=100, null=True, blank=True)
    discovered_data = models.CharField(max_length=100, null=True, blank=True)

    #Infoblox CName Record Information (Only for cname records)
    canonical = models.CharField(max_length=100, null=True, blank=True)

    #Cloud Information
    ci_authority_type = models.CharField(max_length=4, null=True, blank=True, choices=AUTHORITY_TYPES)
    ci_delegated_root = models.CharField(max_length=100, null=True, blank=True)
    ci_delegated_scope = models.CharField(max_length=10, null=True, blank=True)
    ci_mgmt_platform = models.CharField(max_length=100, null=True, blank=True)
    ci_owned_by_adaptor = models.NullBooleanField(null=True, blank=True)
    ci_tenant = models.CharField(max_length=100, null=True, blank=True)
    ci_usage_field = models.CharField(max_length=9, null=True, blank=True)
    ci_delegated_member_ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    ci_delegated_member_ipv6_address = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    ci_delegated_member_name = models.CharField(max_length=100, null=True, blank=True)

    #SNMP3 Credential Information
    snmp3_authentication_protocol = models.CharField(max_length=4, null=True, blank=True)
    snmp3_privacy_protocol = models.CharField(max_length=4, null=True, blank=True)
    snmp3_user = models.CharField(max_length=100, null=True, blank=True)

    #SNMP Credential Information
    snmp_community_string = models.CharField(max_length=100, null=True, blank=True)

    #AWS RTE53 Record Information
    aws_alias_target_dns_name = models.CharField(max_length=100, null=True, blank=True)
    aws_alias_target_evaluate_target_health = models.NullBooleanField(null=True, blank=True)
    aws_alias_target_hosted_zone_id = models.CharField(max_length=100, null=True, blank=True)
    aws_failover = models.CharField(max_length=9, null=True, blank=True)
    aws_geolocation_continent_code = models.CharField(max_length=100, null=True, blank=True)
    aws_geolocation_country_code = models.CharField(max_length=100, null=True, blank=True)
    aws_geolocation_subdivision_code = models.CharField(max_length=100, null=True, blank=True)
    aws_health_check_id = models.CharField(max_length=100, null=True, blank=True)
    aws_region = models.CharField(max_length=100, null=True, blank=True)
    aws_set_identifier = models.CharField(max_length=100, null=True, blank=True)
    aws_type = models.CharField(max_length=5, null=True, blank=True)
    aws_weight = models.PositiveIntegerField(null=True, blank=True)


    #Discovered Data Record Information
    dd_ap_ip_address = models.GenericIPAddressField(max_length=100, null=True, blank=True)
    dd_ap_name = models.CharField(max_length=100, null=True, blank=True)
    dd_ap_ssid = models.CharField(max_length=100, null=True, blank=True)
    dd_bridge_domain = models.CharField(max_length=100, null=True, blank=True)
    dd_cisco_ise_endpoint_profile = models.CharField(max_length=100, null=True, blank=True)
    dd_cisco_ise_security_group = models.CharField(max_length=100, null=True, blank=True)
    dd_cisco_ise_session_state = models.CharField(max_length=100, null=True, blank=True)
    dd_cisco_ise_ssid = models.CharField(max_length=100, null=True, blank=True)
    dd_cmp_type = models.CharField(max_length=100, null=True, blank=True)
    dd_device_contact = models.CharField(max_length=100, null=True, blank=True)
    dd_device_model = models.CharField(max_length=100, null=True, blank=True)
    dd_device_location = models.CharField(max_length=100, null=True, blank=True)
    dd_device_port_name = models.CharField(max_length=100, null=True, blank=True)
    dd_device_port_type = models.CharField(max_length=100, null=True, blank=True)
    dd_device_type = models.CharField(max_length=100, null=True, blank=True)
    dd_device_vendor = models.CharField(max_length=100, null=True, blank=True)
    dd_discovered_name = models.CharField(max_length=100, null=True, blank=True)
    dd_discoverer = models.CharField(max_length=100, null=True, blank=True)
    dd_duid = models.CharField(max_length=100, null=True, blank=True)
    dd_endpoint_groups = models.CharField(max_length=100, null=True, blank=True)
    dd_iprg_no = models.PositiveIntegerField(null=True, blank=True)
    dd_iprg_state = models.CharField(max_length=100, null=True, blank=True)
    dd_iprg_type = models.CharField(max_length=100, null=True, blank=True)
    dd_mac_address = models.CharField(max_length=100, null=True, blank=True)
    dd_mgmt_ip_address = models.GenericIPAddressField(null=True, blank=True)
    dd_netbios_name = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_contact = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_description = models.TextField(null=True, blank=True)
    dd_network_component_ip = models.GenericIPAddressField(null=True, blank=True)
    dd_network_component_location = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_model = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_name = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_port_description = models.TextField(null=True, blank=True)
    dd_network_component_port_name = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_port_number = models.PositiveIntegerField(null=True, blank=True)
    dd_network_component_type = models.CharField(max_length=100, null=True, blank=True)
    dd_network_component_vendor = models.CharField(max_length=100, null=True, blank=True)
    dd_open_ports = models.CharField(max_length=100, null=True, blank=True)
    dd_os = models.CharField(max_length=100, null=True, blank=True)
    dd_port_duplex = models.CharField(max_length=100, null=True, blank=True)
    dd_port_link_status = models.CharField(max_length=100, null=True, blank=True)
    dd_port_speed = models.CharField(max_length=100, null=True, blank=True)
    dd_port_status = models.CharField(max_length=100, null=True, blank=True)
    dd_port_type = models.CharField(max_length=100, null=True, blank=True)
    dd_port_vlan_description = models.CharField(max_length=100, null=True, blank=True)
    dd_port_vlan_name = models.CharField(max_length=100, null=True, blank=True)
    dd_port_vlan_number = models.PositiveIntegerField(null=True, blank=True)
    dd_task_name = models.CharField(max_length=100, null=True, blank=True)
    dd_tenant = models.CharField(max_length=100, null=True, blank=True)
    dd_v_adapter = models.CharField(max_length=100, null=True, blank=True)
    dd_v_cluster = models.CharField(max_length=100, null=True, blank=True)
    dd_v_datacenter = models.CharField(max_length=100, null=True, blank=True)
    dd_v_entity_name = models.CharField(max_length=100, null=True, blank=True)
    dd_v_entity_type = models.CharField(max_length=100, null=True, blank=True)
    dd_v_host = models.CharField(max_length=100, null=True, blank=True)
    dd_v_switch = models.CharField(max_length=100, null=True, blank=True)
    dd_vlan_port_group = models.CharField(max_length=100, null=True, blank=True)
    dd_vmhost_ip_address = models.GenericIPAddressField(null=True, blank=True)
    dd_vmhost_mac_address = models.CharField(max_length=100, null=True, blank=True)
    dd_vmhost_name = models.CharField(max_length=100, null=True, blank=True)
    dd_vmhost_nic_names = models.CharField(max_length=100, null=True, blank=True)
    dd_vmhost_subnet_cidr = models.CharField(max_length=100, null=True, blank=True)
    dd_vmi_id = models.CharField(max_length=100, null=True, blank=True)
    dd_vmi_ip_type = models.CharField(max_length=100, null=True, blank=True)
    dd_vmi_is_public_address = models.NullBooleanField(null=True, blank=True)
    dd_vmi_name = models.NullBooleanField(null=True, blank=True)
    dd_vmi_private_address = models.NullBooleanField(null=True, blank=True)
    dd_vmi_tenant_id = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_conf_mode = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_conf_speed = models.PositiveIntegerField(null=True, blank=True)
    dd_vport_link_status = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_mac_address = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_mode = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_name = models.CharField(max_length=100, null=True, blank=True)
    dd_vport_speed = models.PositiveIntegerField(null=True, blank=True)
    dd_vswitch_available_ports_count = models.PositiveIntegerField(null=True, blank=True)
    dd_vswitch_id = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_ipv6_enabled = models.NullBooleanField(null=True, blank=True)
    dd_vswitch_name = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_segment_id = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_segment_name = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_segment_port_group = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_segment_type = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_tep_dhcp_server = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_tep_ip = models.GenericIPAddressField(null=True, blank=True)
    dd_vswitch_tep_multicast = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_tep_port_group = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_tep_type = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_tep_vlan = models.CharField(max_length=100, null=True, blank=True)
    dd_vswitch_type = models.CharField(max_length=100, null=True, blank=True)

    #IPv4 Host Information
    ipv4_ref = models.CharField(max_length=300, null=True, blank=True)
    ipv4_bootfile = models.CharField(max_length=100, null=True, blank=True)
    ipv4_bootserver = models.CharField(max_length=100, null=True, blank=True)
    ipv4_configure_for_dhcp = models.NullBooleanField(null=True, blank=True)
    ipv4_deny_bootp = models.NullBooleanField(null=True, blank=True)
    ipv4_discover_now_status = models.CharField(max_length=100, null=True, blank=True)
    ipv4_enable_pxe_lease_time = models.NullBooleanField(null=True, blank=True)
    ipv4_host = models.CharField(max_length=100, null=True, blank=True)
    ipv4_ignore_client_requested_options = models.NullBooleanField(null=True, blank=True)
    ipv4_ipv4addr = models.CharField(max_length=25, null=True, blank=True)
    ipv4_is_invalid_mac = models.NullBooleanField(null=True, blank=True)
    ipv4_mac = models.CharField(max_length=100, null=True, blank=True)
    ipv4_match_client = models.CharField(max_length=100, null=True, blank=True)
    ipv4_ms_ad_user_data = models.CharField(max_length=100, null=True, blank=True)
    ipv4_network = models.CharField(max_length=100, null=True, blank=True)
    ipv4_network_view = models.CharField(max_length=100, null=True, blank=True)
    ipv4_nextserver = models.CharField(max_length=100, null=True, blank=True)
    ipv4_pxe_lease_time = models.CharField(max_length=100, null=True, blank=True)
    ipv4_reserved_interface = models.CharField(max_length=100, null=True, blank=True)
    ipv4_use_bootfile = models.NullBooleanField(null=True, blank=True)
    ipv4_use_deny_bootp = models.NullBooleanField(null=True, blank=True)
    ipv4_use_for_ea_inheritance = models.NullBooleanField(null=True, blank=True)
    ipv4_use_ignore_client_requested_options = models.NullBooleanField(null=True, blank=True)
    ipv4_use_logic_filter_rules = models.NullBooleanField(null=True, blank=True)
    ipv4_use_nextserver = models.NullBooleanField(null=True, blank=True)
    ipv4_use_options = models.NullBooleanField(null=True, blank=True)
    ipv4_use_pxe_lease_time = models.NullBooleanField(null=True, blank=True)

    #Logic Filter Rule Information
    lfr_filter = models.CharField(max_length=100, null=True, blank=True)
    lfr_type = models.CharField(max_length=6, null=True, blank=True)

    #DHCP Option Information
    dhcp_name = models.CharField(max_length=100, null=True, blank=True)
    dhcp_num = models.PositiveIntegerField(null=True, blank=True)
    dhcp_use_option = models.NullBooleanField(null=True, blank=True, default=False)
    dhcp_value = models.CharField(max_length=100, null=True, blank=True)
    dhcp_vendor_class = models.CharField(max_length=100, null=True, blank=True)

    #IPv6 Host Information
    ipv6_ref = models.CharField(max_length=300, null=True, blank=True)
    ipv6_address_type = models.CharField(max_length=100, null=True, blank=True)
    ipv6_configure_for_dhcp = models.NullBooleanField(null=True, blank=True)
    ipv6_discover_now_status = models.CharField(max_length=100, null=True, blank=True)
    ipv6_discovered_data = models.ForeignKey(DiscoveredData, null=True, blank=True)
    ipv6_domain_name = models.CharField(max_length=100, null=True, blank=True)
    ipv6_duid = models.CharField(max_length=100, null=True, blank=True)
    ipv6_host = models.CharField(max_length=100, null=True, blank=True)
    ipv6_ipv6addr = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    ipv6_ipv6prefix = models.CharField(max_length=100, null=True, blank=True)
    ipv6_ipv6prefix_bits = models.PositiveIntegerField(null=True, blank=True)
    ipv6_last_queried = models.DateTimeField(null=True, blank=True)
    ipv6_match_client = models.CharField(max_length=100, null=True, blank=True)
    ipv6_ms_ad_user_data = models.PositiveIntegerField(null=True, blank=True)
    ipv6_network = models.CharField(max_length=100, null=True, blank=True)
    ipv6_network_view = models.CharField(max_length=100, null=True, blank=True)
    ipv6_preferred_lifetime = models.PositiveIntegerField(null=True, blank=True)
    ipv6_reserved_interface = models.CharField(max_length=100, null=True, blank=True)
    ipv6_use_domain_name = models.NullBooleanField(null=True, blank=True)
    ipv6_use_domain_name_servers = models.NullBooleanField(null=True, blank=True)
    ipv6_use_for_ea_inheritance = models.NullBooleanField(null=True, blank=True)
    ipv6_use_options = models.NullBooleanField(null=True, blank=True)
    ipv6_use_preferred_lifetime = models.NullBooleanField(null=True, blank=True)
    ipv6_use_valid_lifetime = models.NullBooleanField(null=True, blank=True)
    ipv6_valid_lifetime = models.PositiveIntegerField(null=True, blank=True)

    cli_credential_type = models.CharField(max_length=13, null=True, blank=True)
    cli_user = models.CharField(max_length=100, null=True, blank=True)

    #Domain Name Server Information
    dns_record_domain_name_server = models.CharField(max_length=100, null=True, blank=True)

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

    def getLogicFilterRules(self):
        return self.logicfilterrule_set.filter(visible=True)

    def getDHCPOptions(self):
        return self.dhcpoption_set.filter(visible=True)

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

    def getDHCPOptions(self):
        return self.dhcpoption_set.filter(visible=True)

    def getDomainNameServers(self):
        return self.domainnameserver_set.filter(visible=True)

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
