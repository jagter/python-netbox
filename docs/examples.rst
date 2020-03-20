##############################################
Examples
##############################################

To start with python-netbox client:

    >>> from netbox import NetBox
    >>> netbox = NetBox(host='127.0.0.1', port=32768, use_ssl=False, auth_token='token')


Get all devices:

    >>> netbox.dcim.get_devices()

Get devices per rack:

    >>> netbox.dcim.get_devices(rack_id=1)

Get device by name

    >>> netbox.dcim.get_devices(name='device_name')

Get per device the primary ip and mac address:

    >>> output = []
    >>> for item in a.dcim.get_devices():
    >>>    device_name = item['name']
    >>>
    >>>    if item['primary_ip'] is not None:
    >>>        primary_ip_id = item['primary_ip']['id']
    >>>        get_ips = a.ipam.get_ip_by_id(primary_ip_id)
    >>>
    >>>        output.append({'name': device_name, 'ip': get_ips['address'], 'mac': get_ips['interface']['mac_address']})
    >>>    else:
    >>>         print('{} has no primary_ip'.format(item['name']))
    >>>
    >>>    print(output)

Create a site:

    >>> netbox.dcim.create_site('site1', 'site1')

Delete a site:

    >>> netbox.dcim.delete_site('site1')