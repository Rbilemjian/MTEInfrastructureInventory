from django.shortcuts import render, redirect, get_object_or_404, HttpResponse


from django.contrib.auth.decorators import login_required
from .models import ApplicationServer, DHCPMember, CloudInformation, HOST_FIELDS, IPV4_FIELDS, IPV6_FIELDS, A_FIELDS
from .models import SNMP3Credential, SNMPCredential, ExtensibleAttribute, DiscoveredData, IPv4HostAddress
from .models import IPv6HostAddress, DomainNameServer, LogicFilterRule, Alias, CliCredential, DHCPOption
from .models import AWSRTE53RecordInfo
from .forms import InfobloxImportForm
import requests
import json
import urllib3

#TODO: Double check all of the table populating logic


#Helper functions


def nullifyAsNeeded(date):
    if date == 0 or "00:00":
        return None
    else:
        return date


def clearAllInvisible():
    CliCredential.objects.filter(visible=False).delete()
    Alias.objects.filter(visible=False).delete()
    ExtensibleAttribute.objects.filter(visible=False).delete()
    DHCPOption.objects.filter(visible=False).delete()
    DomainNameServer.objects.filter(visible=False).delete()
    LogicFilterRule.objects.filter(visible=False).delete()
    IPv6HostAddress.objects.filter(visible=False).delete()
    IPv4HostAddress.objects.filter(visible=False).delete()
    DiscoveredData.objects.filter(visible=False).delete()
    AWSRTE53RecordInfo.objects.filter(visible=False).delete()
    SNMP3Credential.objects.filter(visible=False).delete()
    SNMPCredential.objects.filter(visible=False).delete()
    CloudInformation.objects.filter(visible=False).delete()
    DHCPMember.objects.filter(visible=False).delete()
    ApplicationServer.objects.filter(visible=False).delete()





def saveARecord(record):
    #TODO: deal with aws_rte53_record_info, cloud_finfo, discovered_data, ms_ad_user_data, , lastqueried
    if record.get('ms_ad_user_data') is None:
        ms_ad_user_data=None
    else:
        ms_ad_user_data=record.get('ms_ad_user_data').get('active_users_count')
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
        visible=False
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
        location=host.get('device_location'),
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
        visible=False
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
            usage=cloud_info.get('usage'),
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
        ipv4_fields += field + ','




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
        ipv6_fields += field + ','



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












@login_required()
def infoblox(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get('confirmed') == "true":


            #TODO: NEED TO HANDLE DIFF, MAKE EVERYTHING VISIBLE HERE

            applicationServers = ApplicationServer.objects.filter(visible=True)
            return render(request, "application_server_list.html", {"applicationServers": applicationServers})

        form = InfobloxImportForm(request.POST)
        if form.is_valid and len(request.POST.get('view')) > 0 and len(request.POST.get('zone')) > 0:


            clearAllInvisible()


            #do infoblox stuff here
            view = request.POST.get('view')
            zone = request.POST.get('zone')
            record_type = request.POST.get('record_type')

            base_url = 'https://infoblox.net.tfayd.com/wapi/v2.7/' + record_type + '?view=' + view + '&zone=' + zone
            static_args = '&_max_results=25&_paging=1&_return_as_object=1'
            # static_args = '&_max_results=100000000000'
            additional_fields = '&_return_fields='

            if record_type == 'record:host':
                for field in HOST_FIELDS:
                    additional_fields += field + ','

            if record_type == 'record:a':
                for field in A_FIELDS:
                    additional_fields += field + ','

            get_url = base_url + static_args + additional_fields

            urllib3.disable_warnings()

            r = requests.get(get_url, auth=('206582055', 'miketysonpunchout'), verify=False)
            records = r.json()
            result = r.json()
            records = result.get('result')
            # print(records)
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


                    if record_type == "record:a":
                        currRecord = saveARecord(record)
                        saveAWSRTE53RecordInfo(record, currRecord)
                        saveCloudInfo(record, currRecord)
                        saveDiscoveredData(record, currRecord)


                    #TODO: Deal with this extattrs nightmare
                    # extattrs = host.get('extattrs')
                    # if len(extattrs) > 0:
                    #     if extattrs.get('Owner') is not None:
                    #         print(extattrs.get('Owner').get('value'))



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
            return render(request, "infoblox.html", {"form": form, "records": records})
    else:
        form = InfobloxImportForm()
    return render(request, "infoblox.html", {"form": form})



















































