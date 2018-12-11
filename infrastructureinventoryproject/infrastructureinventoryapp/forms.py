from django import forms
from . import models
from .models import ApplicationServer, FilterProfile, FILTER_RECORD_TYPES, RECORD_TYPES, BOOL_WITH_NULL, CliCredential
from.models import CloudInformation, SNMP3Credential, SNMPCredential, AWSRTE53RecordInfo, LogicFilterRule, DHCPOption, DomainNameServer
from .models import IPv6HostAddress, IPv4HostAddress, Alias, ExtensibleAttribute, DiscoveredData, DHCPMember, AuthoritativeZone
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

def get_record_field_values(field):
    return ApplicationServer.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_cloud_information_field_values(field):
    return CloudInformation.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_delegated_member_field_values(field):
    return DHCPMember.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_snmp3_field_values(field):
    return SNMP3Credential.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_snmp_field_values(field):
    return SNMPCredential.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_aws_field_values(field):
    return AWSRTE53RecordInfo.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_discovered_data_values(field):
    return DiscoveredData.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_ipv4_data_values(field):
    return IPv4HostAddress.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_ipv6_data_values(field):
    return IPv6HostAddress.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_logic_filter_data_values(field):
    return LogicFilterRule.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_dhcp_option_data_values(field):
    return DHCPOption.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_dns_data_values(field):
    return DomainNameServer.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_cli_data_values(field):
    return CliCredential.objects.filter(visible=True).values_list(field, flat=True).order_by(field).distinct()


def get_zone_auth_values(field):
    return AuthoritativeZone.objects.all().values_list(field, flat=True).order_by(field).distinct()




def get_aliases():
    return Alias.objects.filter(visible=True).values_list('alias', flat=True).order_by('alias').distinct()


#defines form for importing records from a user-designated zone in infoblox
class InfobloxImportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InfobloxImportForm, self).__init__(*args, **kwargs)
        self.fields['view'] = forms.CharField(min_length=1, max_length=50, required=True, widget=floppyforms.widgets.Input(datalist=get_zone_auth_values('view')))
        self.fields['zone'] = forms.CharField(min_length=1, max_length=50, required=True, widget=floppyforms.widgets.Input(datalist=get_zone_auth_values('zone')))
        self.fields['record_type'] = forms.ChoiceField(choices=RECORD_TYPES, required=True, widget=forms.Select())


class VisibleColumnForm(forms.ModelForm):
    class Meta:
        model = models.VisibleColumns
        exclude = ('user',)



class FilterProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FilterProfileForm, self).__init__(*args, **kwargs)

        #Record Fields
        self.fields['name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('name'), attrs={'size': 45}))
        self.fields['view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('view'), attrs={'size': 45}))
        self.fields['zone'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('zone'), attrs={'size': 45}))
        self.fields['ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ttl'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ttl'), attrs={'size': 45}))
        self.fields['creator'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('creator'), attrs={'size': 45}))
        self.fields['ddns_principal'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ddns_principal'), attrs={'size': 45}))
        self.fields['shared_record_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('shared_record_group'), attrs={'size': 45}))
        self.fields['ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ref'), attrs={'size': 45}))
        self.fields['device_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_location'), attrs={'size': 45}))
        self.fields['device_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_description'), attrs={'size': 45}))
        self.fields['device_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_type'), attrs={'size': 45}))
        self.fields['device_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_vendor'), attrs={'size': 45}))
        self.fields['network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('network_view'), attrs={'size': 45}))
        self.fields['ipv4addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ipv4addr'), attrs={'size': 45}))

        #Cloud Information Fields
        self.fields['ci_delegated_root'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('delegated_root'), attrs={'size': 45}))
        self.fields['ci_mgmt_platform'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('mgmt_platform'), attrs={'size': 45}))
        self.fields['ci_tenant'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('tenant'), attrs={'size': 45}))
        self.fields['ci_delegated_member_ipv4_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('ipv4_address'), attrs={'size': 45}))
        self.fields['ci_delegated_member_ipv6_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('ipv6_address'), attrs={'size': 45}))
        self.fields['ci_delegated_member_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('name'), attrs={'size': 45}))

        #SNMP3 Credential Fields
        self.fields['snmp3_user'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_snmp3_field_values('user'), attrs={'size': 45}))

        #SNMP Credential Fields
        self.fields['snmp_community_string'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_snmp_field_values('community_string'), attrs={'size': 45}))

        #AWS Fields
        self.fields['aws_alias_target_dns_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('alias_target_dns_name'), attrs={'size': 45}))
        self.fields['aws_alias_target_hosted_zone_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('alias_target_hosted_zone_id'), attrs={'size': 45}))
        self.fields['aws_geolocation_continent_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_continent_code'), attrs={'size': 45}))
        self.fields['aws_geolocation_subdivision_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_subdivision_code'), attrs={'size': 45}))
        self.fields['aws_geolocation_country_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_country_code'), attrs={'size': 45}))
        self.fields['aws_health_check_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('health_check_id'), attrs={'size': 45}))
        self.fields['aws_region'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('region'), attrs={'size': 45}))
        self.fields['aws_set_identifier'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('set_identifier'), attrs={'size': 45}))
        self.fields['aws_weight'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('weight'), attrs={'size': 45}))

        #Discovered Data Fields
        self.fields['dd_ap_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_ip_address'), attrs={'size': 45}))
        self.fields['dd_ap_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_name'), attrs={'size': 45}))
        self.fields['dd_ap_ssid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_ssid'), attrs={'size': 45}))
        self.fields['dd_bridge_domain'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('bridge_domain'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_endpoint_profile'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_endpoint_profile'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_security_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_security_group'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_ssid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_ssid'), attrs={'size': 45}))
        self.fields['dd_cmp_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cmp_type'), attrs={'size': 45}))
        self.fields['dd_device_contact'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_contact'), attrs={'size': 45}))
        self.fields['dd_device_model'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_model'), attrs={'size': 45}))
        self.fields['dd_device_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_location'), attrs={'size': 45}))
        self.fields['dd_device_port_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_port_name'), attrs={'size': 45}))
        self.fields['dd_device_port_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_port_type'), attrs={'size': 45}))
        self.fields['dd_device_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_type'), attrs={'size': 45}))
        self.fields['dd_device_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_vendor'), attrs={'size': 45}))
        self.fields['dd_discovered_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('discovered_name'), attrs={'size': 45}))
        self.fields['dd_discoverer'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('discoverer'), attrs={'size': 45}))
        self.fields['dd_duid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('duid'), attrs={'size': 45}))
        self.fields['dd_endpoint_groups'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('endpoint_groups'), attrs={'size': 45}))
        self.fields['dd_iprg_no'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_no'), attrs={'size': 45}))
        self.fields['dd_iprg_state'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_state'), attrs={'size': 45}))
        self.fields['dd_iprg_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_type'), attrs={'size': 45}))
        self.fields['dd_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('mac_address'), attrs={'size': 45}))
        self.fields['dd_mgmt_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('mgmt_ip_address'), attrs={'size': 45}))
        self.fields['dd_netbios_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('netbios_name'), attrs={'size': 45}))
        self.fields['dd_network_component_contact'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_contact'), attrs={'size': 45}))
        self.fields['dd_network_component_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_description'), attrs={'size': 45}))
        self.fields['dd_network_component_ip'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_ip'), attrs={'size': 45}))
        self.fields['dd_network_component_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_location'), attrs={'size': 45}))
        self.fields['dd_network_component_model'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_model'), attrs={'size': 45}))
        self.fields['dd_network_component_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_name'), attrs={'size': 45}))
        self.fields['dd_network_component_port_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_description'), attrs={'size': 45}))
        self.fields['dd_network_component_port_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_name'), attrs={'size': 45}))
        self.fields['dd_network_component_port_number'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_number'), attrs={'size': 45}))
        self.fields['dd_network_component_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_type'), attrs={'size': 45}))
        self.fields['dd_network_component_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_vendor'), attrs={'size': 45}))
        self.fields['dd_open_ports'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('open_ports'), attrs={'size': 45}))
        self.fields['dd_os'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('os'), attrs={'size': 45}))
        self.fields['dd_port_duplex'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_duplex'), attrs={'size': 45}))
        self.fields['dd_port_link_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_link_status'), attrs={'size': 45}))
        self.fields['dd_port_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_speed'), attrs={'size': 45}))
        self.fields['dd_port_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_status'), attrs={'size': 45}))
        self.fields['dd_port_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_type'), attrs={'size': 45}))
        self.fields['dd_port_vlan_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_description'), attrs={'size': 45}))
        self.fields['dd_port_vlan_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_name'), attrs={'size': 45}))
        self.fields['dd_port_vlan_number'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_number'), attrs={'size': 45}))
        self.fields['dd_task_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('task_name'), attrs={'size': 45}))
        self.fields['dd_tenant'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('tenant'), attrs={'size': 45}))
        self.fields['dd_v_adapter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_adapter'), attrs={'size': 45}))
        self.fields['dd_v_cluster'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_cluster'), attrs={'size': 45}))
        self.fields['dd_v_datacenter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_datacenter'), attrs={'size': 45}))
        self.fields['dd_v_entity_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_entity_name'), attrs={'size': 45}))
        self.fields['dd_v_entity_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_entity_type'), attrs={'size': 45}))
        self.fields['dd_v_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_host'), attrs={'size': 45}))
        self.fields['dd_v_switch'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_switch'), attrs={'size': 45}))
        self.fields['dd_vlan_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vlan_port_group'), attrs={'size': 45}))
        self.fields['dd_vmhost_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_ip_address'), attrs={'size': 45}))
        self.fields['dd_vmhost_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_mac_address'), attrs={'size': 45}))
        self.fields['dd_vmhost_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_name'), attrs={'size': 45}))
        self.fields['dd_vmhost_nic_names'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_nic_names'), attrs={'size': 45}))
        self.fields['dd_vmhost_subnet_cidr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_subnet_cidr'), attrs={'size': 45}))
        self.fields['dd_vmi_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_id'), attrs={'size': 45}))
        self.fields['dd_vmi_ip_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_ip_type'), attrs={'size': 45}))
        self.fields['dd_vmi_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_name'), attrs={'size': 45}))
        self.fields['dd_vmi_private_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_private_address'), attrs={'size': 45}))
        self.fields['dd_vmi_tenant_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_tenant_id'), attrs={'size': 45}))
        self.fields['dd_vport_conf_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_conf_speed'), attrs={'size': 45}))
        self.fields['dd_vport_link_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_link_status'), attrs={'size': 45}))
        self.fields['dd_vport_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_mac_address'), attrs={'size': 45}))
        self.fields['dd_vport_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_name'), attrs={'size': 45}))
        self.fields['dd_vport_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_speed'), attrs={'size': 45}))
        self.fields['dd_vswitch_available_ports_count'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_available_ports_count'), attrs={'size': 45}))
        self.fields['dd_vswitch_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_id'), attrs={'size': 45}))
        self.fields['dd_vswitch_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_name'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_id'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_name'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_port_group'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_type'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_dhcp_server'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_dhcp_server'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_ip'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_ip'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_multicast'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_multicast'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_port_group'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_type'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_vlan'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_vlan'), attrs={'size': 45}))

        #IPv4 Address Fields
        self.fields['ipv4_ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ref'), attrs={'size': 45}))
        self.fields['ipv4_bootfile'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('bootfile'), attrs={'size': 45}))
        self.fields['ipv4_bootserver'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('bootserver'), attrs={'size': 45}))
        self.fields['ipv4_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('host'), attrs={'size': 45}))
        self.fields['ipv4_ipv4addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ipv4addr'), attrs={'size': 45}))
        self.fields['ipv4_mac'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('mac'), attrs={'size': 45}))
        self.fields['ipv4_match_client'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('match_client'), attrs={'size': 45}))
        self.fields['ipv4_ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ipv4_network'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('network'), attrs={'size': 45}))
        self.fields['ipv4_network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('network_view'), attrs={'size': 45}))
        self.fields['ipv4_nextserver'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('nextserver'), attrs={'size': 45}))
        self.fields['ipv4_pxe_lease_time'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('pxe_lease_time'), attrs={'size': 45}))
        self.fields['ipv4_reserved_interface'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('reserved_interface'), attrs={'size': 45}))

        #Logic Filter Rule Fields
        self.fields['lfr_filter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_logic_filter_data_values('filter'), attrs={'size': 45}))

        #DHCP Option Fields
        self.fields['dhcp_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('name'), attrs={'size': 45}))
        self.fields['dhcp_num'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('num'), attrs={'size': 45}))
        self.fields['dhcp_value'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('value'), attrs={'size': 45}))
        self.fields['dhcp_vendor_class'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('vendor_class'), attrs={'size': 45}))

        #IPv6 Host Address Fields
        self.fields['ipv6_ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ref'), attrs={'size': 45}))
        self.fields['ipv6_domain_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('domain_name'), attrs={'size': 45}))
        self.fields['ipv6_duid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('duid'), attrs={'size': 45}))
        self.fields['ipv6_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('host'), attrs={'size': 45}))
        self.fields['ipv6_ipv6addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6addr'), attrs={'size': 45}))
        self.fields['ipv6_ipv6prefix'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6prefix'), attrs={'size': 45}))
        self.fields['ipv6_ipv6prefix_bits'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6prefix_bits'), attrs={'size': 45}))
        self.fields['ipv6_match_client'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('match_client'), attrs={'size': 45}))
        self.fields['ipv6_ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ipv6_network'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('network'), attrs={'size': 45}))
        self.fields['ipv6_network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('network_view'), attrs={'size': 45}))
        self.fields['ipv6_preferred_lifetime'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('preferred_lifetime'), attrs={'size': 45}))
        self.fields['ipv6_reserved_interface'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('reserved_interface'), attrs={'size': 45}))
        self.fields['ipv6_valid_lifetime'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('valid_lifetime'), attrs={'size': 45}))

        #DNS Record Fields
        self.fields['dns_record_domain_name_server'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dns_data_values('domain_name_server'), attrs={'size': 45}))

        #CLI Credential Fields
        self.fields['cli_user'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cli_data_values('user'), attrs={'size': 45}))

        #Many-to-One Fields
        self.fields['alias'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aliases(), attrs={'size': 45}))
        self.fields['extensible_attribute_value'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_all_extensible_field_values(), attrs={'size': 45}))
        self.fields['discovered_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_all_discovered_data_values(), attrs={'size': 45}))


    class Meta:
        model = models.FilterProfile
        exclude = []


        widgets = {
            'profile_name': forms.TextInput(attrs={'size': 45, 'required': True}),
            'all_fields': forms.TextInput(attrs={'size': 45}),
            'record_type': forms.widgets.Select(choices=FILTER_RECORD_TYPES),

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
            'ci_delegated_scope': forms.widgets.Select(choices=models.DELEGATED_SCOPES),
            'ci_owned_by_adaptor': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ci_usage_field': forms.widgets.Select(choices=models.USAGES),

            #SNMP3 Credential Information Widgets
            'snmp3_authentication_protocol': forms.widgets.Select(choices=models.AUTHENTICATION_PROTOCOLS),
            'snmp3_privacy_protocol': forms.widgets.Select(choices=models.PRIVACY_PROTOCOLS),

            #AWS RTE53 Record Information
            'aws_alias_target_evaluate_target_health': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'aws_failover': forms.widgets.Select(choices=models.FAILOVERS),
            'aws_type': forms.widgets.Select(choices=models.AWS_TYPES),


            'dd_cisco_ise_session_state': forms.widgets.Select(choices=models.CISCO_ISE_SESSION_STATES),
            'dd_vswitch_type': forms.widgets.Select(choices=models.VSWITCH_TYPES),
            'dd_vswitch_ipv6_enabled': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'dd_vport_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vport_conf_mode': forms.widgets.Select(choices=models.VPORT_MODES),
            'dd_vmi_is_public_address': forms.widgets.Select(choices=BOOL_WITH_NULL),

            #IPv4 Host Address Form Widgets
            'ipv4_configure_for_dhcp': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_deny_bootp': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_discover_now_status': forms.widgets.Select(choices=models.DISCOVER_NOW_STATUSES),
            'ipv4_enable_pxe_lease_time': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_ignore_client_requested_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_is_invalid_mac': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_bootfile': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_deny_bootp': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_for_ea_inheritance': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_ignore_client_requested_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_logic_filter_rules': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_nextserver': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv4_use_pxe_lease_time': forms.widgets.Select(choices=BOOL_WITH_NULL),

            #Logic Filter Rule Widgets
            'lfr_type': forms.widgets.Select(choices=models.LOGIC_FILTER_RULE_TYPES),

            #DHCP Option Filter Rule Widgets
            'dhcp_use_option': forms.widgets.Select(choices=BOOL_WITH_NULL),

            #IPV6 Host Address Widgets
            'ipv6_address_type': forms.widgets.Select(choices=models.ADDRESS_TYPES),
            'ipv6_configure_for_dhcp': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_discover_now_status': forms.widgets.Select(choices=models.DISCOVER_NOW_STATUSES),
            'ipv6_use_domain_name': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_use_domain_name_servers': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_use_for_ea_inheritance': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_use_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_use_preferred_lifetime': forms.widgets.Select(choices=BOOL_WITH_NULL),
            'ipv6_use_valid_lifetime': forms.widgets.Select(choices=BOOL_WITH_NULL),


            #CLI Credential Widgets
            'cli_credential_type': forms.widgets.Select(choices=models.CLI_CREDENTIAL_TYPES),
        }


class AdvancedSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        #Record Fields
        self.fields['name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('name'), attrs={'size': 45}))
        self.fields['view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('view'), attrs={'size': 45}))
        self.fields['zone'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('zone'), attrs={'size': 45}))
        self.fields['ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ttl'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ttl'), attrs={'size': 45}))
        self.fields['creator'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('creator'), attrs={'size': 45}))
        self.fields['ddns_principal'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ddns_principal'), attrs={'size': 45}))
        self.fields['shared_record_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('shared_record_group'), attrs={'size': 45}))
        self.fields['ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ref'), attrs={'size': 45}))
        self.fields['device_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_location'), attrs={'size': 45}))
        self.fields['device_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_description'), attrs={'size': 45}))
        self.fields['device_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_type'), attrs={'size': 45}))
        self.fields['device_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('device_vendor'), attrs={'size': 45}))
        self.fields['network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('network_view'), attrs={'size': 45}))
        self.fields['ipv4addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_record_field_values('ipv4addr'), attrs={'size': 45}))

        #Cloud Information Fields
        self.fields['ci_delegated_root'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('delegated_root'), attrs={'size': 45}))
        self.fields['ci_mgmt_platform'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('mgmt_platform'), attrs={'size': 45}))
        self.fields['ci_tenant'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cloud_information_field_values('tenant'), attrs={'size': 45}))
        self.fields['ci_delegated_member_ipv4_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('ipv4_address'), attrs={'size': 45}))
        self.fields['ci_delegated_member_ipv6_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('ipv6_address'), attrs={'size': 45}))
        self.fields['ci_delegated_member_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_delegated_member_field_values('name'), attrs={'size': 45}))

        #SNMP3 Credential Fields
        self.fields['snmp3_user'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_snmp3_field_values('user'), attrs={'size': 45}))

        #SNMP Credential Fields
        self.fields['snmp_community_string'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_snmp_field_values('community_string'), attrs={'size': 45}))

        #AWS Fields
        self.fields['aws_alias_target_dns_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('alias_target_dns_name'), attrs={'size': 45}))
        self.fields['aws_alias_target_hosted_zone_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('alias_target_hosted_zone_id'), attrs={'size': 45}))
        self.fields['aws_geolocation_continent_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_continent_code'), attrs={'size': 45}))
        self.fields['aws_geolocation_subdivision_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_subdivision_code'), attrs={'size': 45}))
        self.fields['aws_geolocation_country_code'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('geolocation_country_code'), attrs={'size': 45}))
        self.fields['aws_health_check_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('health_check_id'), attrs={'size': 45}))
        self.fields['aws_region'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('region'), attrs={'size': 45}))
        self.fields['aws_set_identifier'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('set_identifier'), attrs={'size': 45}))
        self.fields['aws_weight'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aws_field_values('weight'), attrs={'size': 45}))

        #Discovered Data Fields
        self.fields['dd_ap_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_ip_address'), attrs={'size': 45}))
        self.fields['dd_ap_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_name'), attrs={'size': 45}))
        self.fields['dd_ap_ssid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('ap_ssid'), attrs={'size': 45}))
        self.fields['dd_bridge_domain'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('bridge_domain'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_endpoint_profile'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_endpoint_profile'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_security_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_security_group'), attrs={'size': 45}))
        self.fields['dd_cisco_ise_ssid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cisco_ise_ssid'), attrs={'size': 45}))
        self.fields['dd_cmp_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('cmp_type'), attrs={'size': 45}))
        self.fields['dd_device_contact'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_contact'), attrs={'size': 45}))
        self.fields['dd_device_model'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_model'), attrs={'size': 45}))
        self.fields['dd_device_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_location'), attrs={'size': 45}))
        self.fields['dd_device_port_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_port_name'), attrs={'size': 45}))
        self.fields['dd_device_port_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_port_type'), attrs={'size': 45}))
        self.fields['dd_device_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_type'), attrs={'size': 45}))
        self.fields['dd_device_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('device_vendor'), attrs={'size': 45}))
        self.fields['dd_discovered_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('discovered_name'), attrs={'size': 45}))
        self.fields['dd_discoverer'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('discoverer'), attrs={'size': 45}))
        self.fields['dd_duid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('duid'), attrs={'size': 45}))
        self.fields['dd_endpoint_groups'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('endpoint_groups'), attrs={'size': 45}))
        self.fields['dd_iprg_no'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_no'), attrs={'size': 45}))
        self.fields['dd_iprg_state'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_state'), attrs={'size': 45}))
        self.fields['dd_iprg_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('iprg_type'), attrs={'size': 45}))
        self.fields['dd_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('mac_address'), attrs={'size': 45}))
        self.fields['dd_mgmt_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('mgmt_ip_address'), attrs={'size': 45}))
        self.fields['dd_netbios_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('netbios_name'), attrs={'size': 45}))
        self.fields['dd_network_component_contact'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_contact'), attrs={'size': 45}))
        self.fields['dd_network_component_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_description'), attrs={'size': 45}))
        self.fields['dd_network_component_ip'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_ip'), attrs={'size': 45}))
        self.fields['dd_network_component_location'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_location'), attrs={'size': 45}))
        self.fields['dd_network_component_model'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_model'), attrs={'size': 45}))
        self.fields['dd_network_component_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_name'), attrs={'size': 45}))
        self.fields['dd_network_component_port_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_description'), attrs={'size': 45}))
        self.fields['dd_network_component_port_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_name'), attrs={'size': 45}))
        self.fields['dd_network_component_port_number'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_port_number'), attrs={'size': 45}))
        self.fields['dd_network_component_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_type'), attrs={'size': 45}))
        self.fields['dd_network_component_vendor'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('network_component_vendor'), attrs={'size': 45}))
        self.fields['dd_open_ports'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('open_ports'), attrs={'size': 45}))
        self.fields['dd_os'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('os'), attrs={'size': 45}))
        self.fields['dd_port_duplex'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_duplex'), attrs={'size': 45}))
        self.fields['dd_port_link_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_link_status'), attrs={'size': 45}))
        self.fields['dd_port_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_speed'), attrs={'size': 45}))
        self.fields['dd_port_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_status'), attrs={'size': 45}))
        self.fields['dd_port_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_type'), attrs={'size': 45}))
        self.fields['dd_port_vlan_description'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_description'), attrs={'size': 45}))
        self.fields['dd_port_vlan_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_name'), attrs={'size': 45}))
        self.fields['dd_port_vlan_number'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('port_vlan_number'), attrs={'size': 45}))
        self.fields['dd_task_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('task_name'), attrs={'size': 45}))
        self.fields['dd_tenant'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('tenant'), attrs={'size': 45}))
        self.fields['dd_v_adapter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_adapter'), attrs={'size': 45}))
        self.fields['dd_v_cluster'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_cluster'), attrs={'size': 45}))
        self.fields['dd_v_datacenter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_datacenter'), attrs={'size': 45}))
        self.fields['dd_v_entity_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_entity_name'), attrs={'size': 45}))
        self.fields['dd_v_entity_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_entity_type'), attrs={'size': 45}))
        self.fields['dd_v_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_host'), attrs={'size': 45}))
        self.fields['dd_v_switch'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('v_switch'), attrs={'size': 45}))
        self.fields['dd_vlan_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vlan_port_group'), attrs={'size': 45}))
        self.fields['dd_vmhost_ip_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_ip_address'), attrs={'size': 45}))
        self.fields['dd_vmhost_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_mac_address'), attrs={'size': 45}))
        self.fields['dd_vmhost_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_name'), attrs={'size': 45}))
        self.fields['dd_vmhost_nic_names'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_nic_names'), attrs={'size': 45}))
        self.fields['dd_vmhost_subnet_cidr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmhost_subnet_cidr'), attrs={'size': 45}))
        self.fields['dd_vmi_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_id'), attrs={'size': 45}))
        self.fields['dd_vmi_ip_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_ip_type'), attrs={'size': 45}))
        self.fields['dd_vmi_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_name'), attrs={'size': 45}))
        self.fields['dd_vmi_private_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_private_address'), attrs={'size': 45}))
        self.fields['dd_vmi_tenant_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vmi_tenant_id'), attrs={'size': 45}))
        self.fields['dd_vport_conf_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_conf_speed'), attrs={'size': 45}))
        self.fields['dd_vport_link_status'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_link_status'), attrs={'size': 45}))
        self.fields['dd_vport_mac_address'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_mac_address'), attrs={'size': 45}))
        self.fields['dd_vport_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_name'), attrs={'size': 45}))
        self.fields['dd_vport_speed'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vport_speed'), attrs={'size': 45}))
        self.fields['dd_vswitch_available_ports_count'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_available_ports_count'), attrs={'size': 45}))
        self.fields['dd_vswitch_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_id'), attrs={'size': 45}))
        self.fields['dd_vswitch_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_name'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_id'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_id'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_name'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_port_group'), attrs={'size': 45}))
        self.fields['dd_vswitch_segment_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_segment_type'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_dhcp_server'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_dhcp_server'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_ip'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_ip'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_multicast'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_multicast'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_port_group'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_port_group'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_type'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_type'), attrs={'size': 45}))
        self.fields['dd_vswitch_tep_vlan'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_discovered_data_values('vswitch_tep_vlan'), attrs={'size': 45}))

        #IPv4 Address Fields
        self.fields['ipv4_ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ref'), attrs={'size': 45}))
        self.fields['ipv4_bootfile'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('bootfile'), attrs={'size': 45}))
        self.fields['ipv4_bootserver'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('bootserver'), attrs={'size': 45}))
        self.fields['ipv4_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('host'), attrs={'size': 45}))
        self.fields['ipv4_ipv4addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ipv4addr'), attrs={'size': 45}))
        self.fields['ipv4_mac'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('mac'), attrs={'size': 45}))
        self.fields['ipv4_match_client'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('match_client'), attrs={'size': 45}))
        self.fields['ipv4_ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ipv4_network'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('network'), attrs={'size': 45}))
        self.fields['ipv4_network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('network_view'), attrs={'size': 45}))
        self.fields['ipv4_nextserver'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('nextserver'), attrs={'size': 45}))
        self.fields['ipv4_pxe_lease_time'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('pxe_lease_time'), attrs={'size': 45}))
        self.fields['ipv4_reserved_interface'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv4_data_values('reserved_interface'), attrs={'size': 45}))

        #Logic Filter Rule Fields
        self.fields['lfr_filter'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_logic_filter_data_values('filter'), attrs={'size': 45}))

        #DHCP Option Fields
        self.fields['dhcp_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('name'), attrs={'size': 45}))
        self.fields['dhcp_num'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('num'), attrs={'size': 45}))
        self.fields['dhcp_value'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('value'), attrs={'size': 45}))
        self.fields['dhcp_vendor_class'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dhcp_option_data_values('vendor_class'), attrs={'size': 45}))

        #IPv6 Host Address Fields
        self.fields['ipv6_ref'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ref'), attrs={'size': 45}))
        self.fields['ipv6_domain_name'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('domain_name'), attrs={'size': 45}))
        self.fields['ipv6_duid'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('duid'), attrs={'size': 45}))
        self.fields['ipv6_host'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('host'), attrs={'size': 45}))
        self.fields['ipv6_ipv6addr'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6addr'), attrs={'size': 45}))
        self.fields['ipv6_ipv6prefix'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6prefix'), attrs={'size': 45}))
        self.fields['ipv6_ipv6prefix_bits'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ipv6prefix_bits'), attrs={'size': 45}))
        self.fields['ipv6_match_client'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('match_client'), attrs={'size': 45}))
        self.fields['ipv6_ms_ad_user_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('ms_ad_user_data'), attrs={'size': 45}))
        self.fields['ipv6_network'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('network'), attrs={'size': 45}))
        self.fields['ipv6_network_view'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('network_view'), attrs={'size': 45}))
        self.fields['ipv6_preferred_lifetime'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('preferred_lifetime'), attrs={'size': 45}))
        self.fields['ipv6_reserved_interface'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('reserved_interface'), attrs={'size': 45}))
        self.fields['ipv6_valid_lifetime'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_ipv6_data_values('valid_lifetime'), attrs={'size': 45}))

        #DNS Record Fields
        self.fields['dns_record_domain_name_server'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_dns_data_values('domain_name_server'), attrs={'size': 45}))

        #CLI Credential Fields
        self.fields['cli_user'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_cli_data_values('user'), attrs={'size': 45}))

        #Many-to-One Fields
        self.fields['alias'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_aliases(), attrs={'size': 45}))
        self.fields['extensible_attribute_value'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_all_extensible_field_values(), attrs={'size': 45}))
        self.fields['discovered_data'] = forms.CharField(required=False, widget=floppyforms.widgets.Input(datalist=get_all_discovered_data_values(), attrs={'size': 45}))





    class Meta:
        model = models.FilterProfile
        exclude = []

        widgets = {
            'all_fields': forms.TextInput(attrs={'size': 45}),
                'record_type': forms.widgets.Select(choices=FILTER_RECORD_TYPES),

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
                'ci_delegated_scope': forms.widgets.Select(choices=models.DELEGATED_SCOPES),
                'ci_owned_by_adaptor': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ci_usage_field': forms.widgets.Select(choices=models.USAGES),

                #SNMP3 Credential Information Widgets
                'snmp3_authentication_protocol': forms.widgets.Select(choices=models.AUTHENTICATION_PROTOCOLS),
                'snmp3_privacy_protocol': forms.widgets.Select(choices=models.PRIVACY_PROTOCOLS),

                #AWS RTE53 Record Information
                'aws_alias_target_evaluate_target_health': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'aws_failover': forms.widgets.Select(choices=models.FAILOVERS),
                'aws_type': forms.widgets.Select(choices=models.AWS_TYPES),


                'dd_cisco_ise_session_state': forms.widgets.Select(choices=models.CISCO_ISE_SESSION_STATES),
                'dd_vswitch_type': forms.widgets.Select(choices=models.VSWITCH_TYPES),
                'dd_vswitch_ipv6_enabled': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'dd_vport_mode': forms.widgets.Select(choices=models.VPORT_MODES),
                'dd_vport_conf_mode': forms.widgets.Select(choices=models.VPORT_MODES),
                'dd_vmi_is_public_address': forms.widgets.Select(choices=BOOL_WITH_NULL),

                #IPv4 Host Address Form Widgets
                'ipv4_configure_for_dhcp': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_deny_bootp': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_discover_now_status': forms.widgets.Select(choices=models.DISCOVER_NOW_STATUSES),
                'ipv4_enable_pxe_lease_time': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_ignore_client_requested_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_is_invalid_mac': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_bootfile': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_deny_bootp': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_for_ea_inheritance': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_ignore_client_requested_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_logic_filter_rules': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_nextserver': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv4_use_pxe_lease_time': forms.widgets.Select(choices=BOOL_WITH_NULL),

                #Logic Filter Rule Widgets
                'lfr_type': forms.widgets.Select(choices=models.LOGIC_FILTER_RULE_TYPES),

                #DHCP Option Filter Rule Widgets
                'dhcp_use_option': forms.widgets.Select(choices=BOOL_WITH_NULL),

                #IPV6 Host Address Widgets
                'ipv6_address_type': forms.widgets.Select(choices=models.ADDRESS_TYPES),
                'ipv6_configure_for_dhcp': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_discover_now_status': forms.widgets.Select(choices=models.DISCOVER_NOW_STATUSES),
                'ipv6_use_domain_name': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_use_domain_name_servers': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_use_for_ea_inheritance': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_use_options': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_use_preferred_lifetime': forms.widgets.Select(choices=BOOL_WITH_NULL),
                'ipv6_use_valid_lifetime': forms.widgets.Select(choices=BOOL_WITH_NULL),


                #CLI Credential Widgets
                'cli_credential_type': forms.widgets.Select(choices=models.CLI_CREDENTIAL_TYPES),
        }












































