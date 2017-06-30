============================
Python Netbox Client
============================

python-netbox is a client for the Netbox (https://github.com/digitalocean/netbox) API.
It's based on the APIv2 which is released since version 2.0.0. For now only the get/create/delete methods
are implemented. The possibility to modify items will be implementend soon.

The full documentation can be found here_.

.. _here: http://python-netbox.readthedocs.io/en/latest/#

-----------------
Installation
-----------------

To get the latest version from Github:

   $ pip install -e git+https://github.com/jagter/python-netbox.git#egg=python-netbox

-----------------
Usage
-----------------
To start with the module:

    >>> from netbox import NetBox
    >>> netbox = NetBox(host='127.0.0.1', port=32768, use_ssl=False, auth_token='token')


-----------------
Examples
-----------------
Get all devices:

    >>> netbox.dcim.get_devices()

Get devices per rack:

    >>> netbox.dcim.get_devices_per_rack('rack_name')

Get device by name

    >>> netbox.dcim.get_device_by_name('device_name')

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

-----------------
Support
-----------------
If you have questions or comments please send an email to thomas@tjrb.nl
