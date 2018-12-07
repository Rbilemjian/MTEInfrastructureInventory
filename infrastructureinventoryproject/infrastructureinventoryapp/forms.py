from django import forms
from . import models
from .models import ApplicationServer, FilterProfile, FILTER_RECORD_TYPES, RECORD_TYPES, BOOL_WITH_NULL
from.models import CloudInformation, SNMP3Credential, SNMPCredential, AWSRTE53RecordInfo
from .models import IPv6HostAddress, IPv4HostAddress, Alias, ExtensibleAttribute, DiscoveredData, DHCPMember
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

#Cloud Information datalists
delegated_roots = CloudInformation.objects.filter(visible=True).values_list('delegated_root', flat=True).order_by('delegated_root').distinct()
mgmt_platforms = CloudInformation.objects.filter(visible=True).values_list('mgmt_platform', flat=True).order_by('mgmt_platform').distinct()
tenants = CloudInformation.objects.filter(visible=True).values_list('tenant', flat=True).order_by('tenant').distinct()
delegated_member_ipv4s = DHCPMember.objects.filter(visible=True).values_list('ipv4_address', flat=True).order_by('ipv4_address').distinct()
delegated_member_ipv6s = DHCPMember.objects.filter(visible=True).values_list('ipv6_address', flat=True).order_by('ipv6_address').distinct()
delegated_member_names = DHCPMember.objects.filter(visible=True).values_list('name', flat=True).order_by('name').distinct()

#SNMP3 Credential Information datalists
snmp3_users = SNMP3Credential.objects.filter(visible=True).values_list('user', flat=True).order_by('user').distinct()

#SNMP Credential Information datalists
community_strings = SNMPCredential.objects.filter(visible=True).values_list('community_string', flat=True).order_by('community_string').distinct()

#AWS Recoord Information datalists
alias_target_dns_names = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('alias_target_dns_name', flat=True).order_by('alias_target_dns_name').distinct()
alias_target_hosted_zone_ids = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('alias_target_hosted_zone_id', flat=True).order_by('alias_target_hosted_zone_id').distinct()
geolocation_continent_codes = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('geolocation_continent_code', flat=True).order_by('geolocation_continent_code').distinct()
geolocation_subdivision_codes = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('geolocation_subdivision_code', flat=True).order_by('geolocation_subdivision_code').distinct()
geolocation_country_codes = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('geolocation_country_code', flat=True).order_by('geolocation_country_code').distinct()
health_check_ids = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('health_check_id', flat=True).order_by('health_check_id').distinct()
regions = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('region', flat=True).order_by('region').distinct()
set_identifiers = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('set_identifier', flat=True).order_by('set_identifier').distinct()
weights = AWSRTE53RecordInfo.objects.filter(visible=True).values_list('weight', flat=True).order_by('weight').distinct()


#Discovered Data Information datalists

dd_fields = DiscoveredData._meta.get_all_field_names()
ddv = {}
for field in dd_fields:
    ddv[field] = DiscoveredData.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


#Many-to-one datalists
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
            'record_type': forms.widgets.Select(choices=FILTER_RECORD_TYPES),

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
            'rrset_order': forms.widgets.Select(),
            'use_cli_credentials': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp3_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable_discovery': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'forbid_reclamation': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'ddns_protected': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_ttl': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'reclaimable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'allow_telnet': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'configure_for_dns': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),

            # Cloud Information Widgets
            'ci_authority_type': forms.widgets.Select(choices=models.AUTHORITY_TYPES, attrs={'cols': 5}),
            'ci_delegated_root': floppyforms.widgets.Input(datalist=delegated_roots, attrs={'size': 45}),
            'ci_delegated_scope': forms.widgets.Select(choices=models.DELEGATED_SCOPES),
            'ci_mgmt_platform': floppyforms.widgets.Input(datalist=mgmt_platforms, attrs={'size': 45}),
            'ci_owned_by_adaptor': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ci_tenant': floppyforms.widgets.Input(datalist=tenants, attrs={'size': 45}),
            'ci_usage_field': forms.widgets.Select(choices=models.USAGES),
            'ci_delegated_member_ipv4_address': floppyforms.widgets.Input(datalist=delegated_member_ipv4s,
                                                                          attrs={'size': 45}),
            'ci_delegated_member_ipv6_address': floppyforms.widgets.Input(datalist=delegated_member_ipv6s,
                                                                          attrs={'size': 45}),
            'ci_delegated_member_name': floppyforms.widgets.Input(datalist=delegated_member_names, attrs={'size': 45}),

            # SNMP3 Credential Information Widgets
            'snmp3_authentication_protocol': forms.widgets.Select(choices=models.AUTHENTICATION_PROTOCOLS),
            'snmp3_privacy_protocol': forms.widgets.Select(choices=models.PRIVACY_PROTOCOLS),
            'snmp3_user': floppyforms.widgets.Input(datalist=snmp3_users, attrs={'size': 45}),

            # SNMP Credential Information Widgets
            'snmp_community_string': floppyforms.widgets.Input(datalist=community_strings, attrs={'size': 45}),

            # AWS RTE53 Record Information
            'aws_alias_target_dns_name': floppyforms.widgets.Input(datalist=alias_target_dns_names, attrs={'size': 45}),
            'aws_alias_target_evaluate_target_health': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'aws_alias_target_hosted_zone_id': floppyforms.widgets.Input(datalist=alias_target_hosted_zone_ids,
                                                                         attrs={'size': 45}),
            'aws_failover': forms.widgets.Select(choices=models.FAILOVERS),
            'aws_geolocation_continent_code': floppyforms.widgets.Input(datalist=geolocation_continent_codes,
                                                                        attrs={'size': 45}),
            'aws_geolocation_subdivision_code': floppyforms.widgets.Input(datalist=geolocation_subdivision_codes,
                                                                          attrs={'size': 45}),
            'aws_geolocation_country_code': floppyforms.widgets.Input(datalist=geolocation_country_codes,
                                                                      attrs={'size': 45}),
            'aws_health_check_id': floppyforms.widgets.Input(datalist=health_check_ids, attrs={'size': 45}),
            'aws_region': floppyforms.widgets.Input(datalist=regions, attrs={'size': 45}),
            'aws_set_identifier': floppyforms.widgets.Input(datalist=set_identifiers, attrs={'size': 45}),
            'aws_type': forms.widgets.Select(choices=models.AWS_TYPES),
            'aws_weight': floppyforms.widgets.Input(datalist=weights, attrs={'size': 45}),

            # Discovered Data Information
            'dd_ap_ip_address': floppyforms.widgets.Input(datalist=ddv['ap_ip_address'], attrs={'size': 45}),
            'dd_ap_name': floppyforms.widgets.Input(datalist=ddv['ap_name'], attrs={'size': 45}),
            'dd_ap_ssid': floppyforms.widgets.Input(datalist=ddv['ap_ssid'], attrs={'size': 45}),
            'dd_bridge_domain': floppyforms.widgets.Input(datalist=ddv['bridge_domain'], attrs={'size': 45}),
            'dd_cisco_ise_endpoint_profile': floppyforms.widgets.Input(datalist=ddv['cisco_ise_endpoint_profile'],
                                                                       attrs={'size': 45}),
            'dd_cisco_ise_security_group': floppyforms.widgets.Input(datalist=ddv['cisco_ise_security_group'],
                                                                     attrs={'size': 45}),
            'dd_cisco_ise_ssid': floppyforms.widgets.Input(datalist=ddv['cisco_ise_ssid'], attrs={'size': 45}),
            'dd_cmp_type': floppyforms.widgets.Input(datalist=ddv['cmp_type'], attrs={'size': 45}),
            'dd_device_contact': floppyforms.widgets.Input(datalist=ddv['device_contact'], attrs={'size': 45}),
            'dd_device_model': floppyforms.widgets.Input(datalist=ddv['device_model'], attrs={'size': 45}),
            'dd_device_location': floppyforms.widgets.Input(datalist=ddv['device_location'], attrs={'size': 45}),
            'dd_device_port_name': floppyforms.widgets.Input(datalist=ddv['device_port_name'], attrs={'size': 45}),
            'dd_device_port_type': floppyforms.widgets.Input(datalist=ddv['port_type'], attrs={'size': 45}),
            'dd_device_type': floppyforms.widgets.Input(datalist=ddv['device_type'], attrs={'size': 45}),
            'dd_device_vendor': floppyforms.widgets.Input(datalist=ddv['device_vendor'], attrs={'size': 45}),
            'dd_discovered_name': floppyforms.widgets.Input(datalist=ddv['discovered_name'], attrs={'size': 45}),
            'dd_discoverer': floppyforms.widgets.Input(datalist=ddv['discoverer'], attrs={'size': 45}),
            'dd_duid': floppyforms.widgets.Input(datalist=ddv['duid'], attrs={'size': 45}),
            'dd_endpoint_groups': floppyforms.widgets.Input(datalist=ddv['endpoint_groups'], attrs={'size': 45}),
            'dd_iprg_no': floppyforms.widgets.Input(datalist=ddv['iprg_no'], attrs={'size': 45}),
            'dd_iprg_state': floppyforms.widgets.Input(datalist=ddv['iprg_state'], attrs={'size': 45}),
            'dd_iprg_type': floppyforms.widgets.Input(datalist=ddv['iprg_type'], attrs={'size': 45}),
            'dd_mac_address': floppyforms.widgets.Input(datalist=ddv['mac_address'], attrs={'size': 45}),
            'dd_mgmt_ip_address': floppyforms.widgets.Input(datalist=ddv['mgmt_ip_address'], attrs={'size': 45}),
            'dd_netbios_name': floppyforms.widgets.Input(datalist=ddv['netbios_name'], attrs={'size': 45}),
            'dd_network_component_contact': floppyforms.widgets.Input(datalist=ddv['network_component_contact'],
                                                                      attrs={'size': 45}),
            'dd_network_component_description': floppyforms.widgets.Input(datalist=ddv['network_component_description'],
                                                                          attrs={'size': 45}),
            'dd_network_component_ip': floppyforms.widgets.Input(datalist=ddv['network_component_ip'],
                                                                 attrs={'size': 45}),
            'dd_network_component_location': floppyforms.widgets.Input(datalist=ddv['network_component_location'],
                                                                       attrs={'size': 45}),
            'dd_network_component_model': floppyforms.widgets.Input(datalist=ddv['network_component_model'],
                                                                    attrs={'size': 45}),
            'dd_network_component_name': floppyforms.widgets.Input(datalist=ddv['network_component_name'],
                                                                   attrs={'size': 45}),
            'dd_network_component_port_description': floppyforms.widgets.Input(
                datalist=ddv['network_component_port_description'], attrs={'size': 45}),
            'dd_network_component_port_name': floppyforms.widgets.Input(datalist=ddv['network_component_name'],
                                                                        attrs={'size': 45}),
            'dd_network_component_port_number': floppyforms.widgets.Input(datalist=ddv['network_component_port_number'],
                                                                          attrs={'size': 45}),
            'dd_network_component_type': floppyforms.widgets.Input(datalist=ddv['network_component_type'],
                                                                   attrs={'size': 45}),
            'dd_network_component_vendor': floppyforms.widgets.Input(datalist=ddv['network_component_vendor'],
                                                                     attrs={'size': 45}),
            'dd_open_ports': floppyforms.widgets.Input(datalist=ddv['open_ports'], attrs={'size': 45}),
            'dd_os': floppyforms.widgets.Input(datalist=ddv['os'], attrs={'size': 45}),
            'dd_port_duplex': floppyforms.widgets.Input(datalist=ddv['port_duplex'], attrs={'size': 45}),
            'dd_port_link_status': floppyforms.widgets.Input(datalist=ddv['port_link_status'], attrs={'size': 45}),
            'dd_port_speed': floppyforms.widgets.Input(datalist=ddv['port_speed'], attrs={'size': 45}),
            'dd_port_status': floppyforms.widgets.Input(datalist=ddv['port_status'], attrs={'size': 45}),
            'dd_port_type': floppyforms.widgets.Input(datalist=ddv['port_type'], attrs={'size': 45}),
            'dd_port_vlan_description': floppyforms.widgets.Input(datalist=ddv['port_vlan_description'],
                                                                  attrs={'size': 45}),
            'dd_port_vlan_name': floppyforms.widgets.Input(datalist=ddv['port_vlan_name'], attrs={'size': 45}),
            'dd_port_vlan_number': floppyforms.widgets.Input(datalist=ddv['port_vlan_number'], attrs={'size': 45}),
            'dd_task_name': floppyforms.widgets.Input(datalist=ddv['task_name'], attrs={'size': 45}),
            'dd_tenant': floppyforms.widgets.Input(datalist=ddv['tenant'], attrs={'size': 45}),
            'dd_v_adapter': floppyforms.widgets.Input(datalist=ddv['v_adapter'], attrs={'size': 45}),
            'dd_v_cluster': floppyforms.widgets.Input(datalist=ddv['v_cluster'], attrs={'size': 45}),
            'dd_v_datacenter': floppyforms.widgets.Input(datalist=ddv['v_datacenter'], attrs={'size': 45}),
            'dd_v_entity_name': floppyforms.widgets.Input(datalist=ddv['v_entity_name'], attrs={'size': 45}),
            'dd_v_entity_type': floppyforms.widgets.Input(datalist=ddv['v_entity_type'], attrs={'size': 45}),
            'dd_v_host': floppyforms.widgets.Input(datalist=ddv['v_host'], attrs={'size': 45}),
            'dd_v_switch': floppyforms.widgets.Input(datalist=ddv['v_switch'], attrs={'size': 45}),
            'dd_vlan_port_group': floppyforms.widgets.Input(datalist=ddv['vlan_port_group'], attrs={'size': 45}),
            'dd_vmhost_ip_address': floppyforms.widgets.Input(datalist=ddv['vmhost_ip_address'], attrs={'size': 45}),
            'dd_vmhost_mac_address': floppyforms.widgets.Input(datalist=ddv['vmhost_mac_address'], attrs={'size': 45}),
            'dd_vmhost_name': floppyforms.widgets.Input(datalist=ddv['vmhost_name'], attrs={'size': 45}),
            'dd_vmhost_nic_names': floppyforms.widgets.Input(datalist=ddv['vmhost_nic_names'], attrs={'size': 45}),
            'dd_vmhost_subnet_cidr': floppyforms.widgets.Input(datalist=ddv['vmhost_subnet_cidr'], attrs={'size': 45}),
            'dd_vmi_id': floppyforms.widgets.Input(datalist=ddv['vmi_id'], attrs={'size': 45}),
            'dd_vmi_ip_type': floppyforms.widgets.Input(datalist=ddv['vmi_ip_type'], attrs={'size': 45}),
            'dd_vmi_name': floppyforms.widgets.Input(datalist=ddv['vmi_name'], attrs={'size': 45}),
            'dd_vmi_private_address': floppyforms.widgets.Input(datalist=ddv['vmi_private_address'],
                                                                attrs={'size': 45}),
            'dd_vmi_tenant_id': floppyforms.widgets.Input(datalist=ddv['vmi_tenant_id'], attrs={'size': 45}),
            'dd_vport_conf_speed': floppyforms.widgets.Input(datalist=ddv['vport_conf_speed'], attrs={'size': 45}),
            'dd_vport_link_status': floppyforms.widgets.Input(datalist=ddv['vport_link_status'], attrs={'size': 45}),
            'dd_vport_mac_address': floppyforms.widgets.Input(datalist=ddv['vport_mac_address'], attrs={'size': 45}),
            'dd_vport_name': floppyforms.widgets.Input(datalist=ddv['vport_name'], attrs={'size': 45}),
            'dd_vport_speed': floppyforms.widgets.Input(datalist=ddv['vport_speed'], attrs={'size': 45}),
            'dd_vswitch_available_ports_count': floppyforms.widgets.Input(datalist=ddv['vswitch_available_ports_count'],
                                                                          attrs={'size': 45}),
            'dd_vswitch_id': floppyforms.widgets.Input(datalist=ddv['vswitch_id'], attrs={'size': 45}),
            'dd_vswitch_name': floppyforms.widgets.Input(datalist=ddv['vswitch_name'], attrs={'size': 45}),
            'dd_vswitch_segment_id': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_id'], attrs={'size': 45}),
            'dd_vswitch_segment_name': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_name'],
                                                                 attrs={'size': 45}),
            'dd_vswitch_segment_port_group': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_port_group'],
                                                                       attrs={'size': 45}),
            'dd_vswitch_segment_type': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_type'],
                                                                 attrs={'size': 45}),
            'dd_vswitch_tep_dhcp_server': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_dhcp_server'],
                                                                    attrs={'size': 45}),
            'dd_vswitch_tep_ip': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_ip'], attrs={'size': 45}),
            'dd_vswitch_tep_multicast': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_multicast'],
                                                                  attrs={'size': 45}),
            'dd_vswitch_tep_port_group': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_port_group'],
                                                                   attrs={'size': 45}),
            'dd_vswitch_tep_type': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_type'], attrs={'size': 45}),
            'dd_vswitch_tep_vlan': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_vlan'], attrs={'size': 45}),

            'dd_cisco_ise_session_state': forms.widgets.Select(choices=models.CISCO_ISE_SESSION_STATES),
            'dd_vswitch_type': forms.widgets.Select(choices=models.VSWITCH_TYPES),
            'dd_vswitch_ipv6_enabled': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'dd_vport_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vport_conf_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vmi_is_public_address': forms.widgets.Select(choices=BOOL_WITH_NULL),

            # #Many-to-one Widgets
            # 'ipv4addr': floppyforms.widgets.Input(datalist=ipv4addrs, attrs={'size': 45}),
            # 'ipv6addr': floppyforms.widgets.Input(datalist=ipv6addrs, attrs={'size': 45}),
            # 'alias': floppyforms.widgets.Input(datalist=aliases, attrs={'size': 45}),
            # 'extensible_attribute_value': floppyforms.widgets.Input(datalist=extensible_attribute_values, attrs={'size': 45}),
            # 'discovered_data': floppyforms.widgets.Input(datalist=discovered_data_values, attrs={'size': 45}),
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
            'record_type': forms.widgets.Select(choices=FILTER_RECORD_TYPES),
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
            'rrset_order': forms.widgets.Select(),
            'use_cli_credentials': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp3_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_snmp_credential': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable_discovery': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'forbid_reclamation': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'ddns_protected': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'disable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'use_ttl': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'reclaimable': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'allow_telnet': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),
            'configure_for_dns': forms.widgets.Select(choices=BOOL_WITH_NULL, attrs={'cols': 5}),

            #Cloud Information Widgets
            'ci_authority_type': forms.widgets.Select(choices=models.AUTHORITY_TYPES, attrs={'cols': 5}),
            'ci_delegated_root': floppyforms.widgets.Input(datalist=delegated_roots, attrs={'size': 45}),
            'ci_delegated_scope': forms.widgets.Select(choices=models.DELEGATED_SCOPES),
            'ci_mgmt_platform': floppyforms.widgets.Input(datalist=mgmt_platforms, attrs={'size': 45}),
            'ci_owned_by_adaptor': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ci_tenant': floppyforms.widgets.Input(datalist=tenants, attrs={'size': 45}),
            'ci_usage_field': forms.widgets.Select(choices=models.USAGES),
            'ci_delegated_member_ipv4_address': floppyforms.widgets.Input(datalist=delegated_member_ipv4s, attrs={'size': 45}),
            'ci_delegated_member_ipv6_address': floppyforms.widgets.Input(datalist=delegated_member_ipv6s, attrs={'size': 45}),
            'ci_delegated_member_name': floppyforms.widgets.Input(datalist=delegated_member_names, attrs={'size': 45}),

            #SNMP3 Credential Information Widgets
            'snmp3_authentication_protocol': forms.widgets.Select(choices=models.AUTHENTICATION_PROTOCOLS),
            'snmp3_privacy_protocol': forms.widgets.Select(choices=models.PRIVACY_PROTOCOLS),
            'snmp3_user': floppyforms.widgets.Input(datalist=snmp3_users, attrs={'size': 45}),

            #SNMP Credential Information Widgets
            'snmp_community_string': floppyforms.widgets.Input(datalist=community_strings, attrs={'size': 45}),

            #AWS RTE53 Record Information
            'aws_alias_target_dns_name': floppyforms.widgets.Input(datalist=alias_target_dns_names, attrs={'size': 45}),
            'aws_alias_target_evaluate_target_health': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'aws_alias_target_hosted_zone_id': floppyforms.widgets.Input(datalist=alias_target_hosted_zone_ids, attrs={'size': 45}),
            'aws_failover': forms.widgets.Select(choices=models.FAILOVERS),
            'aws_geolocation_continent_code': floppyforms.widgets.Input(datalist=geolocation_continent_codes, attrs={'size': 45}),
            'aws_geolocation_subdivision_code': floppyforms.widgets.Input(datalist=geolocation_subdivision_codes, attrs={'size': 45}),
            'aws_geolocation_country_code': floppyforms.widgets.Input(datalist=geolocation_country_codes, attrs={'size': 45}),
            'aws_health_check_id': floppyforms.widgets.Input(datalist=health_check_ids, attrs={'size': 45}),
            'aws_region': floppyforms.widgets.Input(datalist=regions, attrs={'size': 45}),
            'aws_set_identifier': floppyforms.widgets.Input(datalist=set_identifiers, attrs={'size': 45}),
            'aws_type': forms.widgets.Select(choices=models.AWS_TYPES),
            'aws_weight': floppyforms.widgets.Input(datalist=weights, attrs={'size': 45}),

            #Discovered Data Information
            'dd_ap_ip_address': floppyforms.widgets.Input(datalist=ddv['ap_ip_address'], attrs={'size': 45}),
            'dd_ap_name': floppyforms.widgets.Input(datalist=ddv['ap_name'], attrs={'size': 45}),
            'dd_ap_ssid': floppyforms.widgets.Input(datalist=ddv['ap_ssid'], attrs={'size': 45}),
            'dd_bridge_domain': floppyforms.widgets.Input(datalist=ddv['bridge_domain'], attrs={'size': 45}),
            'dd_cisco_ise_endpoint_profile': floppyforms.widgets.Input(datalist=ddv['cisco_ise_endpoint_profile'], attrs={'size': 45}),
            'dd_cisco_ise_security_group': floppyforms.widgets.Input(datalist=ddv['cisco_ise_security_group'], attrs={'size': 45}),
            'dd_cisco_ise_ssid': floppyforms.widgets.Input(datalist=ddv['cisco_ise_ssid'], attrs={'size': 45}),
            'dd_cmp_type': floppyforms.widgets.Input(datalist=ddv['cmp_type'], attrs={'size': 45}),
            'dd_device_contact': floppyforms.widgets.Input(datalist=ddv['device_contact'], attrs={'size': 45}),
            'dd_device_model': floppyforms.widgets.Input(datalist=ddv['device_model'], attrs={'size': 45}),
            'dd_device_location': floppyforms.widgets.Input(datalist=ddv['device_location'], attrs={'size': 45}),
            'dd_device_port_name': floppyforms.widgets.Input(datalist=ddv['device_port_name'], attrs={'size': 45}),
            'dd_device_port_type': floppyforms.widgets.Input(datalist=ddv['port_type'], attrs={'size': 45}),
            'dd_device_type': floppyforms.widgets.Input(datalist=ddv['device_type'], attrs={'size': 45}),
            'dd_device_vendor': floppyforms.widgets.Input(datalist=ddv['device_vendor'], attrs={'size': 45}),
            'dd_discovered_name': floppyforms.widgets.Input(datalist=ddv['discovered_name'], attrs={'size': 45}),
            'dd_discoverer': floppyforms.widgets.Input(datalist=ddv['discoverer'], attrs={'size': 45}),
            'dd_duid': floppyforms.widgets.Input(datalist=ddv['duid'], attrs={'size': 45}),
            'dd_endpoint_groups': floppyforms.widgets.Input(datalist=ddv['endpoint_groups'], attrs={'size': 45}),
            'dd_iprg_no': floppyforms.widgets.Input(datalist=ddv['iprg_no'], attrs={'size': 45}),
            'dd_iprg_state': floppyforms.widgets.Input(datalist=ddv['iprg_state'], attrs={'size': 45}),
            'dd_iprg_type': floppyforms.widgets.Input(datalist=ddv['iprg_type'], attrs={'size': 45}),
            'dd_mac_address': floppyforms.widgets.Input(datalist=ddv['mac_address'], attrs={'size': 45}),
            'dd_mgmt_ip_address': floppyforms.widgets.Input(datalist=ddv['mgmt_ip_address'], attrs={'size': 45}),
            'dd_netbios_name': floppyforms.widgets.Input(datalist=ddv['netbios_name'], attrs={'size': 45}),
            'dd_network_component_contact': floppyforms.widgets.Input(datalist=ddv['network_component_contact'], attrs={'size': 45}),
            'dd_network_component_description': floppyforms.widgets.Input(datalist=ddv['network_component_description'], attrs={'size': 45}),
            'dd_network_component_ip': floppyforms.widgets.Input(datalist=ddv['network_component_ip'], attrs={'size': 45}),
            'dd_network_component_location': floppyforms.widgets.Input(datalist=ddv['network_component_location'], attrs={'size': 45}),
            'dd_network_component_model': floppyforms.widgets.Input(datalist=ddv['network_component_model'], attrs={'size': 45}),
            'dd_network_component_name': floppyforms.widgets.Input(datalist=ddv['network_component_name'], attrs={'size': 45}),
            'dd_network_component_port_description': floppyforms.widgets.Input(datalist=ddv['network_component_port_description'], attrs={'size': 45}),
            'dd_network_component_port_name': floppyforms.widgets.Input(datalist=ddv['network_component_name'], attrs={'size': 45}),
            'dd_network_component_port_number': floppyforms.widgets.Input(datalist=ddv['network_component_port_number'], attrs={'size': 45}),
            'dd_network_component_type': floppyforms.widgets.Input(datalist=ddv['network_component_type'], attrs={'size': 45}),
            'dd_network_component_vendor': floppyforms.widgets.Input(datalist=ddv['network_component_vendor'], attrs={'size': 45}),
            'dd_open_ports': floppyforms.widgets.Input(datalist=ddv['open_ports'], attrs={'size': 45}),
            'dd_os': floppyforms.widgets.Input(datalist=ddv['os'], attrs={'size': 45}),
            'dd_port_duplex': floppyforms.widgets.Input(datalist=ddv['port_duplex'], attrs={'size': 45}),
            'dd_port_link_status': floppyforms.widgets.Input(datalist=ddv['port_link_status'], attrs={'size': 45}),
            'dd_port_speed': floppyforms.widgets.Input(datalist=ddv['port_speed'], attrs={'size': 45}),
            'dd_port_status': floppyforms.widgets.Input(datalist=ddv['port_status'], attrs={'size': 45}),
            'dd_port_type': floppyforms.widgets.Input(datalist=ddv['port_type'], attrs={'size': 45}),
            'dd_port_vlan_description': floppyforms.widgets.Input(datalist=ddv['port_vlan_description'], attrs={'size': 45}),
            'dd_port_vlan_name': floppyforms.widgets.Input(datalist=ddv['port_vlan_name'], attrs={'size': 45}),
            'dd_port_vlan_number': floppyforms.widgets.Input(datalist=ddv['port_vlan_number'], attrs={'size': 45}),
            'dd_task_name': floppyforms.widgets.Input(datalist=ddv['task_name'], attrs={'size': 45}),
            'dd_tenant': floppyforms.widgets.Input(datalist=ddv['tenant'], attrs={'size': 45}),
            'dd_v_adapter': floppyforms.widgets.Input(datalist=ddv['v_adapter'], attrs={'size': 45}),
            'dd_v_cluster': floppyforms.widgets.Input(datalist=ddv['v_cluster'], attrs={'size': 45}),
            'dd_v_datacenter': floppyforms.widgets.Input(datalist=ddv['v_datacenter'], attrs={'size': 45}),
            'dd_v_entity_name': floppyforms.widgets.Input(datalist=ddv['v_entity_name'], attrs={'size': 45}),
            'dd_v_entity_type': floppyforms.widgets.Input(datalist=ddv['v_entity_type'], attrs={'size': 45}),
            'dd_v_host': floppyforms.widgets.Input(datalist=ddv['v_host'], attrs={'size': 45}),
            'dd_v_switch': floppyforms.widgets.Input(datalist=ddv['v_switch'], attrs={'size': 45}),
            'dd_vlan_port_group': floppyforms.widgets.Input(datalist=ddv['vlan_port_group'], attrs={'size': 45}),
            'dd_vmhost_ip_address': floppyforms.widgets.Input(datalist=ddv['vmhost_ip_address'], attrs={'size': 45}),
            'dd_vmhost_mac_address': floppyforms.widgets.Input(datalist=ddv['vmhost_mac_address'], attrs={'size': 45}),
            'dd_vmhost_name': floppyforms.widgets.Input(datalist=ddv['vmhost_name'], attrs={'size': 45}),
            'dd_vmhost_nic_names': floppyforms.widgets.Input(datalist=ddv['vmhost_nic_names'], attrs={'size': 45}),
            'dd_vmhost_subnet_cidr': floppyforms.widgets.Input(datalist=ddv['vmhost_subnet_cidr'], attrs={'size': 45}),
            'dd_vmi_id': floppyforms.widgets.Input(datalist=ddv['vmi_id'], attrs={'size': 45}),
            'dd_vmi_ip_type': floppyforms.widgets.Input(datalist=ddv['vmi_ip_type'], attrs={'size': 45}),
            'dd_vmi_name': floppyforms.widgets.Input(datalist=ddv['vmi_name'], attrs={'size': 45}),
            'dd_vmi_private_address': floppyforms.widgets.Input(datalist=ddv['vmi_private_address'], attrs={'size': 45}),
            'dd_vmi_tenant_id': floppyforms.widgets.Input(datalist=ddv['vmi_tenant_id'], attrs={'size': 45}),
            'dd_vport_conf_speed': floppyforms.widgets.Input(datalist=ddv['vport_conf_speed'], attrs={'size': 45}),
            'dd_vport_link_status': floppyforms.widgets.Input(datalist=ddv['vport_link_status'], attrs={'size': 45}),
            'dd_vport_mac_address': floppyforms.widgets.Input(datalist=ddv['vport_mac_address'], attrs={'size': 45}),
            'dd_vport_name': floppyforms.widgets.Input(datalist=ddv['vport_name'], attrs={'size': 45}),
            'dd_vport_speed': floppyforms.widgets.Input(datalist=ddv['vport_speed'], attrs={'size': 45}),
            'dd_vswitch_available_ports_count': floppyforms.widgets.Input(datalist=ddv['vswitch_available_ports_count'], attrs={'size': 45}),
            'dd_vswitch_id': floppyforms.widgets.Input(datalist=ddv['vswitch_id'], attrs={'size': 45}),
            'dd_vswitch_name': floppyforms.widgets.Input(datalist=ddv['vswitch_name'], attrs={'size': 45}),
            'dd_vswitch_segment_id': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_id'], attrs={'size': 45}),
            'dd_vswitch_segment_name': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_name'], attrs={'size': 45}),
            'dd_vswitch_segment_port_group': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_port_group'], attrs={'size': 45}),
            'dd_vswitch_segment_type': floppyforms.widgets.Input(datalist=ddv['vswitch_segment_type'], attrs={'size': 45}),
            'dd_vswitch_tep_dhcp_server': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_dhcp_server'], attrs={'size': 45}),
            'dd_vswitch_tep_ip': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_ip'], attrs={'size': 45}),
            'dd_vswitch_tep_multicast': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_multicast'], attrs={'size': 45}),
            'dd_vswitch_tep_port_group': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_port_group'], attrs={'size': 45}),
            'dd_vswitch_tep_type': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_type'], attrs={'size': 45}),
            'dd_vswitch_tep_vlan': floppyforms.widgets.Input(datalist=ddv['vswitch_tep_vlan'], attrs={'size': 45}),

            'dd_cisco_ise_session_state': forms.widgets.Select(choices=models.CISCO_ISE_SESSION_STATES),
            'dd_vswitch_type': forms.widgets.Select(choices=models.VSWITCH_TYPES),
            'dd_vswitch_ipv6_enabled': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'dd_vport_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vport_conf_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vmi_is_public_address': forms.widgets.Select(choices=BOOL_WITH_NULL),

            # # #Many-to-one Widgets
            # 'ipv4addr': floppyforms.widgets.Input(datalist=ipv4addrs, attrs={'size': 45}),
            # 'ipv6addr': floppyforms.widgets.Input(datalist=ipv6addrs, attrs={'size': 45}),
            # 'alias': floppyforms.widgets.Input(datalist=aliases, attrs={'size': 45}),
            # 'extensible_attribute_value': floppyforms.widgets.Input(datalist=extensible_attribute_values,attrs={'size': 45}),
            # 'discovered_data': floppyforms.widgets.Input(datalist=discovered_data_values, attrs={'size': 45}),
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
