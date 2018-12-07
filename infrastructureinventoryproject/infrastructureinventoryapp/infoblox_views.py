from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from .models import ApplicationServer, DHCPMember, CloudInformation, HOST_FIELDS, IPV4_FIELDS, IPV6_FIELDS, A_FIELDS
from .models import SNMP3Credential, SNMPCredential, ExtensibleAttribute, DiscoveredData, IPv4HostAddress
from .models import IPv6HostAddress, DomainNameServer, LogicFilterRule, Alias, CliCredential, DHCPOption
from .models import AWSRTE53RecordInfo, CNAME_FIELDS, AuthoritativeZone
from .forms import InfobloxImportForm
import requests
import json
import urllib3



#Helper functions


def nullifyAsNeeded(date):
    if date == 0 or "00:00":
        return None
    else:
        return date


def clearAllInvisible():
    application_servers = ApplicationServer.objects.filter(visible=False)
    for application_server in application_servers:
        application_server.deleteWithForeign()



def setAllVisible():
    cli_creds = CliCredential.objects.filter(visible=False)
    setVisible(cli_creds)

    aliases = Alias.objects.filter(visible=False)
    setVisible(aliases)

    ext_attrs = ExtensibleAttribute.objects.filter(visible=False)
    setVisible(ext_attrs)

    dhcp_options = DHCPOption.objects.filter(visible=False)
    setVisible(dhcp_options)

    domain_name_servers = DomainNameServer.objects.filter(visible=False)
    setVisible(domain_name_servers)

    logic_filter_rules = LogicFilterRule.objects.filter(visible=False)
    setVisible(logic_filter_rules)

    ipv6_host_addresses = IPv6HostAddress.objects.filter(visible=False)
    setVisible(ipv6_host_addresses)

    ipv4_host_addresses = IPv4HostAddress.objects.filter(visible=False)
    setVisible(ipv4_host_addresses)

    discovered_datas = DiscoveredData.objects.filter(visible=False)
    setVisible(discovered_datas)

    aws_record_infos = AWSRTE53RecordInfo.objects.filter(visible=False)
    setVisible(aws_record_infos)

    snmp3_credentials = SNMP3Credential.objects.filter(visible=False)
    setVisible(snmp3_credentials)

    snmp_credentials = SNMPCredential.objects.filter(visible=False)
    setVisible(snmp_credentials)

    cloud_informations = CloudInformation.objects.filter(visible=False)
    setVisible(cloud_informations)

    dhcp_members = DHCPMember.objects.filter(visible=False)
    setVisible(dhcp_members)

    app_servers = ApplicationServer.objects.filter(visible=False)
    setVisible(app_servers)



def setVisible(items):
    for item in items:
        item.visible = True
        item.save()



def applicationServerDiff(c, n):
    #TODO: This function does not actually work. Will get it working after basic functionality is achieved
    #TODO: For now not taking diff. Just updating
    #c is the current application server to be updated
    #n is the new application server pulled from infoblox to update from

    c.comment = n.comment
    c.ddns_protected = n.ddns_protected
    c.disable = n.disable
    c.last_queried = n.last_queried
    c.ms_ad_user_data = n.ms_ad_user_data
    c.name = n.name
    c.ttl = n.ttl
    c.use_ttl = n.use_ttl
    c.view = n.view
    c.zone = n.zone
    c.allow_telnet = n.allow_telnet
    c.configure_for_dns = n.configure_for_dns
    c.device_description = n.device_description
    c.device_type = n.device_type
    c.device_vendor = n.device_vendor
    c.disable_discover = n.disable_discovery
    c.network_view = n.network_view
    c.rrset_order = n.rrset_order
    c.use_cli_credentials = n.use_cli_credentials
    c.use_snmp3_credential = n.use_snmp3_credential
    c.use_snmp_credential = n.use_snmp3_credential
    c.creation_time = n.creation_time
    c.creator = n.creator
    c.ddns_principal = n.ddns_principal
    c.forbid_reclamation = n.forbid_reclamation
    c.ipv4addr = n.ipv4addr
    c.reclaimable = n.reclaimable
    c.shared_record_group = n.shared_record_group

    #Handling one-to-one models

    c.snmp_credential = n.snmp3_credential

    #Handling many-to-one models
    curr_ipv4hosts = c.ipv4hostaddress_set.all()
    curr_ipv4hosts.delete()
    new_ipv4hosts = n.ipv4hostaddress_set.all()
    for new_ipv4host in new_ipv4hosts:
        new_ipv4host.application_server = c

    curr_ipv6hosts = c.ipv6hostaddress_set.all()
    curr_ipv6hosts.delete()
    new_ipv6hosts = n.ipv6hostaddress_set.all()
    for new_ipv6host in new_ipv6hosts:
        new_ipv6host.application_server = c

    curr_ext_attrs = c.extensibleattribute_set.all()
    curr_ext_attrs.delete()
    new_ext_attrs = n.extensibleattribute_set.all()
    for new_ext_attr in new_ext_attrs:
        new_ext_attr.application_server = c

    curr_aliases = c.alias_set.all()
    curr_aliases.delete()
    new_aliases = n.alias_set.all()
    for new_alias in new_aliases:
        new_alias.application_server = c

    curr_cli_creds = c.clicredential_set.all()
    curr_cli_creds.delete()
    new_cli_creds = n.clicredential_set.all()
    for new_cli_cred in new_cli_creds:
        new_cli_cred.application_server = c

    c.save()
    n.delete()













def databaseDiff():

    currAppServers = ApplicationServer.objects.filter(visible=True)
    newAppServers = ApplicationServer.objects.filter(visible=False)

    for newAppServer in newAppServers:
        if currAppServers.filter(ref=newAppServer.ref).count() == 1:
            currAppServer = currAppServers.get(ref=newAppServer.ref)
            currAppServer.deleteWithForeign()



def saveCNAMERecord(record):
    curr_rec = ApplicationServer(
        ref=record.get('_ref'),
        canonical=record.get('canonical'),
        comment=record.get('comment'),
        creation_time=nullifyAsNeeded(record.get('creation_time')),
        creator=record.get('creator'),
        ddns_principal=record.get('ddns_principal'),
        ddns_protected=record.get('ddns_protected'),
        disable=record.get('disable'),
        forbid_reclamation=record.get('forbid_reclamation'),
        last_queried=nullifyAsNeeded(record.get('last_queried')),
        name=record.get('name'),
        reclaimable=record.get('reclaimable'),
        shared_record_group=record.get('shared_record_group'),
        ttl=record.get('ttl'),
        use_ttl=record.get('use_ttl'),
        view=record.get('view'),
        zone=record.get('zone'),
        last_pulled=timezone.now(),
        record_type="CNAME Record",
        visible=False,
    )
    curr_rec.save()
    return curr_rec




def saveARecord(record):
    if record.get('ms_ad_user_data') is None:
        ms_ad_user_data=None
    else:
        ms_ad_user_data = record.get('ms_ad_user_data').get('active_users_count')
    curr_rec = ApplicationServer(
        ref=record.get('_ref'),
        comment=record.get('comment'),
        creation_time=nullifyAsNeeded(record.get('creation_time')),
        creator=record.get('creator'),
        ddns_principal=record.get('ddns_principal'),
        ddns_protected=record.get('ddns_protected'),
        disable=record.get('disable'),
        forbid_reclamation=record.get('forbid_reclamation'),
        ipv4addr=record.get('ipv4addr'),
        last_queried=nullifyAsNeeded(record.get('last_queried')),
        ms_ad_user_data=ms_ad_user_data,
        name=record.get('name'),
        reclaimable=record.get('reclaimable'),
        shared_record_group=record.get('shared_record_group'),
        ttl=record.get('ttl'),
        use_ttl=record.get('use_ttl'),
        view=record.get('view'),
        zone=record.get('zone'),
        last_pulled=timezone.now(),
        record_type="A Record",
        visible=False,
    )
    curr_rec.save()
    return curr_rec


def saveAWSRTE53RecordInfo(record, currRecord):
    aws_info = record.get('aws_rte53_record_info')
    if aws_info is None: return
    
    new_aws_info = AWSRTE53RecordInfo(
        alias_target_dns_name=aws_info.get('alias_target_dns_name'),
        alias_target_evaluate_target_health=aws_info.get('alias_target_evaluate_target_health'),
        alias_target_hosted_zone_id=aws_info.get('alias_target_hosted_zone_id'),
        failover=aws_info.get('failover'),
        geolocation_continent_code=aws_info.get('geolocation_continent_code'),
        health_check_id=aws_info.get('health_check_id'),
        region=aws_info.get('region'),
        set_identifier=aws_info.get('set_identifier'),
        type=aws_info.get('type'),
        weight=aws_info.get('weight')
    )
    aws_info.save()
    currRecord.aws_rte53_record_info = new_aws_info
    currRecord.save()




def saveHostRecord(host):
    if host.get('ms_ad_user_data') is None:
        ms_ad_user_data = None
    else:
        ms_ad_user_data = host.get('ms_ad_user_data').get('active_users_count')

    # Adding current host to database
    currHost = ApplicationServer(
        ref=host.get('_ref'),
        name=host.get('name'),
        allow_telnet=host.get('allow_telnet'),
        comment=host.get('comment'),
        configure_for_dns=host.get('configure_for_dns'),
        ddns_protected=host.get('ddns_protected'),
        device_description=host.get('device_description'),
        device_location=host.get('device_location'),
        device_type=host.get('device_type'),
        device_vendor=host.get('device_vendor'),
        disable=host.get('disable'),
        disable_discovery=host.get('disable_discovery'),
        last_queried=nullifyAsNeeded(host.get('last_queried')),
        ms_ad_user_data=ms_ad_user_data,
        network_view=host.get('network_view'),
        rrset_order=host.get('rrset_order'),
        ttl=host.get('ttl'),
        use_cli_credentials=host.get('use_cli_credentials'),
        use_snmp3_credential=host.get('use_snmp3_credential'),
        use_snmp_credential=host.get('use_snmp_credential'),
        use_ttl=host.get('use_ttl'),
        view=host.get('view'),
        zone=host.get('zone'),
        last_pulled=timezone.now(),
        record_type="Host Record",
        visible=False,
    )
    currHost.save()
    return currHost



# Adding aliases from current host record to database
def saveAliases(host, currHost):
    aliases = host.get('aliases')
    if aliases is not None:
        for alias in aliases:
            currAlias = Alias(
                application_server=currHost,
                alias=alias,
            )
            currAlias.save()


# Adding CLI Credentials from current host to database
def saveCLICredentials(host, currHost):
    cli_credentials = host.get('cli_credentials')
    if cli_credentials is not None:
        for cli_credential in cli_credentials:
            curr_cli_credential = CliCredential(
                application_server=currHost,
                comment=cli_credential.get('comment'),
                credential_type=cli_credential.get('credential_type'),
                user=cli_credential.get('user')
            )
            curr_cli_credential.save()


# Adding Cloud Info from current host to database
def saveCloudInfo(host, currHost):
    cloud_info = host.get('cloud_info')
    if cloud_info is not None:
        new_cloud_info = CloudInformation(
            authority_type=cloud_info.get('authority_type'),
            delegated_root=cloud_info.get('delegated_root'),
            delegated_scope=cloud_info.get('delegated_scope'),
            mgmt_platform=cloud_info.get('mgmt_platform'),
            owned_by_adaptor=cloud_info.get('owned_by_adaptor'),
            tenant=cloud_info.get('tenant'),
            usage_field=cloud_info.get('usage'),
        )
        new_cloud_info.save()

        delegated_member = cloud_info.get('delegated_member')
        new_dm = DHCPMember(
            ipv4_address=delegated_member.get('ipv4_address'),
            ipv6_address=delegated_member.get('ipv6_address'),
            name=delegated_member.get('name'),
        )
        new_dm.save()
        new_cloud_info.delegated_member = new_dm
        new_cloud_info.save()
        currHost.cloud_information = new_cloud_info
        currHost.save()


# Adding Discovered Data from current ipv6host to database
def saveDiscoveredData(ipaddr, iphost):
    dd = ipaddr.get('discovered_data')
    if dd is not None:

        discovered_data = DiscoveredData()

        fields = DiscoveredData._meta.get_all_field_names()
        for field in fields:
            if field == "first_discovered" or field == "last_discovered" or dd.get(field) is None:
                continue
            setattr(discovered_data, field, dd.get(field))

        discovered_data.first_discovered = nullifyAsNeeded(dd.get('first_discovered'))
        discovered_data.last_discovered = nullifyAsNeeded(dd.get('last_discovered'))
        discovered_data.save()
        iphost.discovered_data = discovered_data
        iphost.save()



#Adding logic filter rules from current ipv4address to the database
def saveLogicFilterRules(ipv4addr, ipv4host):

    filter_rules = ipv4addr.get('logic_filter_rules')
    if filter_rules is None: return
    for filter_rule in filter_rules:
        new_rule = LogicFilterRule(
            ipv4_host_address=ipv4host,
            filter=filter_rule.get('filter'),
            type=filter_rule.get('type')
        )
        new_rule.save()


def saveIPv4Options(ipv4addr, ipv4host):
    options = ipv4addr.get('options')
    if options is not None:

        for option in options:
            new_option = DHCPOption(
                ipv4_host_address=ipv4host,
                name=option.get('name'),
                num=option.get('num'),
                use_option=option.get('use_option'),
                value=option.get('value'),
                vendor_class=option.get('vendor_class')
            )
            new_option.save()






# Adding ipv4addresses from current host to database
def saveIPv4HostAddresses(host, currHost):

    ipv4addrs = host.get('ipv4addrs')


    base_url = 'https://infoblox.net.tfayd.com/wapi/v2.7/'
    ipv4_fields = '?_return_fields%2b='
    for field in IPV4_FIELDS:
        ipv4_fields += field[0] + ','




    if ipv4addrs is not None:
        for ipv4addr in ipv4addrs:

            get_url = base_url + ipv4addr.get('_ref') + ipv4_fields
            r = requests.get(get_url, auth=('206582055', 'miketysonpunchout'), verify=False)
            ipv4addr = r.json()

            if ipv4addr.get('ms_ad_user_data') is None:
                ms_ad_user_data = None
            else:
                ms_ad_user_data = ipv4addr.get('ms_ad_user_data').get('active_users_count')

            ipv4host = IPv4HostAddress(
                application_server=currHost,
                ref=ipv4addr.get('_ref'),
                bootfile=ipv4addr.get('bootfile'),
                bootserver=ipv4addr.get('bootserver'),
                configure_for_dhcp=ipv4addr.get('configure_for_dhcp'),
                deny_bootp=ipv4addr.get('deny_bootp'),
                discover_now_status=ipv4addr.get('discover_now_status'),
                enable_pxe_lease_time=ipv4addr.get('enable_pxe_lease_time'),
                host=ipv4addr.get('host'),
                ignore_client_requested_options=ipv4addr.get('ignore_client_requested_options'),
                ipv4addr=ipv4addr.get('ipv4addr'),
                is_invalid_mac=ipv4addr.get('is_invalid_mac'),
                last_queried=nullifyAsNeeded(ipv4addr.get('last_queried')),
                mac=ipv4addr.get('mac'),
                match_client=ipv4addr.get('match_client'),
                ms_ad_user_data=ms_ad_user_data,
                network=ipv4addr.get('network'),
                network_view=ipv4addr.get('network_view'),
                nextserver=ipv4addr.get('nextserver'),
                pxe_lease_time=ipv4addr.get('pxe_lease_time'),
                reserved_interface=ipv4addr.get('reserved_interface'),
                use_bootfile=ipv4addr.get('use_bootfile'),
                use_deny_bootp=ipv4addr.get('use_deny_bootp'),
                use_for_ea_inheritance=ipv4addr.get('use_for_ea_inheritance'),
                use_ignore_client_requested_options=ipv4addr.get('use_ignore_client_requested_options'),
                use_logic_filter_rules=ipv4addr.get('use_logic_filter_rules'),
                use_nextserver=ipv4addr.get('use_nextserver'),
                use_options=ipv4addr.get('use_options'),
                use_pxe_lease_time=ipv4addr.get('use_pxe_lease_time'),
            )
            ipv4host.save()
            #Handling additional structs that are within the fields of this ipv4host
            saveDiscoveredData(ipv4addr, ipv4host)
            saveLogicFilterRules(ipv4addr, ipv4host)
            saveIPv4Options(ipv4addr, ipv4host)



# Adding domain name servers from current ipv6host to database
def saveDomainNameServers(ipv6addr, ipv6host):
    domain_name_servers = ipv6addr.get('domain_name_servers')
    if domain_name_servers is not None:
        for domain_name_server in domain_name_servers:
            new_domain = DomainNameServer(
                ipv6_host_address=ipv6host,
                domain_name_server=domain_name_server
            )
            new_domain.save()


# Adding Options from current ipv6host to database
def saveIPv6Options(ipv6addr, ipv6host):
    options = ipv6addr.get('options')
    if options is not None:
        for option in options:
            new_option = DHCPOption(
                ipv6_host_address=ipv6host,
                name=option.get('name'),
                num=option.get('num'),
                use_option=option.get('use_option'),
                value=option.get('value'),
                vendor_class=option.get('vendor_class')
            )
            new_option.save()


# Adding ipv6addresses from current host to database
def saveIPv6HostAddresses(host, currHost):
    # TODO: Do a GET request for the full data of the ipv6addrs struct

    ipv6addrs = host.get('ipv6addrs')
    base_url = 'https://infoblox.net.tfayd.com/wapi/v2.7/'
    ipv6_fields = '?_return_fields%2b='
    for field in IPV6_FIELDS:
        ipv6_fields += field[0] + ','



    if ipv6addrs is not None:
        for ipv6addr in ipv6addrs:

            get_url = base_url + ipv6addr.get('_ref') + ipv6_fields
            r = requests.get(get_url, auth=('206582055', 'miketysonpunchout'), verify=False)
            ipv6addr = r.json()


            if ipv6addr.get('ms_ad_user_data') is None:
                ms_ad_user_data = None
            else:
                ms_ad_user_data = ipv6addr.get('ms_ad_user_data').get('active_users_count')

            ipv6host = IPv6HostAddress(
                application_server=currHost,
                ref=ipv6addr.get('_ref'),
                address_type=ipv6addr.get('address_type'),
                configure_for_dhcp=ipv6addr.get('configure_for_dhcp'),
                discover_now_status=ipv6addr.get('discover_now_status'),
                domain_name=ipv6addr.get('domain_name'),
                duid=ipv6addr.get('duid'),
                host=ipv6addr.get('host'),
                ipv6addr=ipv6addr.get('ipv6addr'),
                ipv6prefix_bits=ipv6addr.get('ipv6prefix_bits'),
                last_queried=nullifyAsNeeded(ipv6addr.get('last_queried')),
                match_client=ipv6addr.get('match_client'),
                ms_ad_user_data=ms_ad_user_data,
                network=ipv6addr.get('network'),
                network_view=ipv6addr.get('network_view'),
                preferred_lifetime=ipv6addr.get('preferred_lifetime'),
                reserved_interface=ipv6addr.get('reserved_interface'),
                use_domain_name=ipv6addr.get('use_domain_name'),
                use_for_ea_inheritance=ipv6addr.get('use_for_ea_inheritance'),
                use_options=ipv6addr.get('use_options'),
                use_preferred_lifetime=ipv6addr.get('use_preferred_lifetime'),
                use_valid_lifetime=ipv6addr.get('use_valid_lifetime'),
                valid_lifetime=ipv6addr.get('valid_lifetime')
            )
            ipv6host.save()
            saveDiscoveredData(ipv6addr, ipv6host)
            saveDomainNameServers(ipv6addr, ipv6host)
            saveIPv6Options(ipv6addr, ipv6host)


# Adding snmp3 cred from current host to database
def saveSNMP3Credential(host, currHost):
    snmp3_credential = host.get('snmp3_credential')
    if snmp3_credential is not None:
        new_credential = SNMP3Credential(
            authentication_protocol=snmp3_credential.get('authentication_protocol'),
            comment=snmp3_credential.get('comment'),
            privacy_protocol=snmp3_credential.get('privacy_protocol'),
            user=snmp3_credential.get('user')
        )
        new_credential.save()
        currHost.snmp3_credential = new_credential
        currHost.save()


# Adding snmp_cred from current host to database
def saveSNMPCredential(host, currHost):
    snmp_credential = host.get('snmp_credential')
    if snmp_credential is not None:
        new_credential = SNMPCredential(
            comment=snmp_credential.get('comment'),
            community_string=snmp_credential.get('community_string')
        )
        new_credential.save()
        currHost.snmp_credential = new_credential
        currHost.save()


def saveExtAttributes(host, currHost):
    ext_attrs = host.get('extattrs')
    if ext_attrs is None: return
    for ext_attr in ext_attrs:
        ext_attr_value = ext_attrs.get(ext_attr).get('value')
        new_ext_attr = ExtensibleAttribute(
            application_server=currHost,
            attribute_name=ext_attr,
            attribute_value=ext_attr_value
        )
        new_ext_attr.save()









@login_required()
def infoblox(request):
    urllib3.disable_warnings()

    r = requests.get('https://infoblox.net.tfayd.com/wapi/v2.7/zone_auth', auth=('206582055', 'miketysonpunchout'), verify=False)
    auth_zones_json = json.loads(r.content)
    AuthoritativeZone.objects.all().delete()
    for auth_zone in auth_zones_json:
        new_zone = AuthoritativeZone(view = auth_zone.get('view'), zone=auth_zone.get('fqdn'))
        new_zone.save()

    if request.method == "POST":
        if request.POST.get('confirmed') == "true":


            databaseDiff()
            setAllVisible()
            return redirect('/infrastructureinventory/applicationserver')

        form = InfobloxImportForm(request.POST)
        if form.is_valid and len(request.POST.get('view')) > 0 and len(request.POST.get('zone')) > 0:


            clearAllInvisible()


            #do infoblox stuff here
            view = request.POST.get('view')
            zone = request.POST.get('zone')
            record_type = request.POST.get('record_type')

            base_url = 'https://infoblox.net.tfayd.com/wapi/v2.7/' + record_type + '?view=' + view + '&zone=' + zone
            static_args = '&_max_results=25&_paging=1&_return_as_object=1'
            additional_fields = '&_return_fields='

            if record_type == 'record:host':
                fields = HOST_FIELDS

            if record_type == 'record:a':
                fields = A_FIELDS

            if record_type == 'record:cname':
                fields = CNAME_FIELDS

            for field in fields:
                additional_fields += field + ','

            get_url = base_url + static_args + additional_fields


            r = requests.get(get_url, auth=('206582055', 'miketysonpunchout'), verify=False)
            result = r.json()
            #Error handling: if API returned an error
            if result.get('Error') is not None:
                error = result.get('Error')
                error = "Infoblox Error: " + error.split(": ", 1)[1]
                return render(request, "infoblox.html", {"form": form, "error": error})

            #Error handling: if API returned nothing
            if len(result.get('result')) == 0:
                error = "Infoblox returned no records for this query"
                return render(request, "infoblox.html", {"form": form, "error": error})

            records = result.get('result')
            next_page_id = result.get('next_page_id')



            #"Infinite" loop which ends when no pages to query remain
            while True:
                for record in records:


                    if record_type == "record:host":
                        currHost = saveHostRecord(record)
                        saveAliases(record, currHost)
                        saveCLICredentials(record, currHost)
                        saveCloudInfo(record, currHost)
                        saveIPv4HostAddresses(record, currHost)
                        saveIPv6HostAddresses(record, currHost)
                        saveSNMP3Credential(record, currHost)
                        saveSNMPCredential(record, currHost)
                        saveExtAttributes(record, currHost)



                    if record_type == "record:a":
                        currRecord = saveARecord(record)
                        saveAWSRTE53RecordInfo(record, currRecord)
                        saveCloudInfo(record, currRecord)
                        saveDiscoveredData(record, currRecord)
                        saveExtAttributes(record, currRecord)



                    if record_type == "record:cname":
                        currRecord = saveCNAMERecord(record)
                        saveAWSRTE53RecordInfo(record, currRecord)
                        saveCloudInfo(record, currRecord)
                        saveExtAttributes(record, currRecord)


                    #TODO: Deal with extattrs



                #If no next_page_id (ie. no more hosts to pull), time to break loop
                if next_page_id is None:
                    break

                # Get the next page of results from the infoblox WAPI
                get_url = base_url + static_args + '&_page_id=' + next_page_id + additional_fields
                r = requests.get(get_url, auth=('206582055', 'miketysonpunchout'), verify=False)
                result = r.json()
                records = result.get('result')
                next_page_id = result.get('next_page_id')

            records = ApplicationServer.objects.filter(visible=False)
            record_type = records.first().record_type
            return render(request, "infoblox.html", {"form": form, "records": records, "record_type": record_type})
    else:
        form = InfobloxImportForm()
    return render(request, "infoblox.html", {"form": form})



















































