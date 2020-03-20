============================
Python Netbox Client
============================

python-netbox is a client for the Netbox (https://github.com/digitalocean/netbox) API.
It's based on the APIv2 which is released since version 2.0.0. It requires python 3.

The full documentation can be found here_.

.. _here: http://python-netbox.readthedocs.io/en/latest/#

-----------------
Installation
-----------------

To get the latest version from Github:

   $ pip3 install python-netbox

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

    >>> netbox.dcim.get_devices(rack_id=1)

Get device by name

    >>> netbox.dcim.get_devices(name='device_name')

Create a site:

    >>> netbox.dcim.create_site('site1', 'site1')

Delete a site:

    >>> netbox.dcim.delete_site('site1')

Get IP address object:

    >>> netbox.ipam.get_ip_addresses(address='10.0.0.1/16')

-----------------
Support
-----------------
If you have questions or comments please send an email to thomas@tjrb.nl
