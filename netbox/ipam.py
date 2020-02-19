import ipaddress
from netbox import exceptions


class Ipam(object):

    def __init__(self, netbox_con):

        self.netbox_con = netbox_con

    def get_choices(self, choice_id=None):
        """Return choices for all fields if choice_id is not defined

        :param choice_id: Optional model:field tuple
        """
        return self.netbox_con.get('/ipam/_choices/', choice_id)

    def get_services(self, **kwargs):
        """Return all services"""
        return self.netbox_con.get('/ipam/services/', **kwargs)

    def create_service(self, name, port, protocol, **kwargs):
        """Create a new service definition

        :param name: Name of the provided service
        :param port: Service listening port
        :param protocol: Service used protocol 6 is used to TCP and 17 for UDP 
        :param kwargs: Optional arguments (need to attach service to a 'virtual_machine: id' or 'device: id' )
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "port": port, "protocol": protocol }
        return self.netbox_con.post('/ipam/services/', required_fields, **kwargs)

    def get_ip_addresses(self, **kwargs):
        """Return all ip addresses"""
        return self.netbox_con.get('/ipam/ip-addresses/', **kwargs)

    def get_ip_by_device(self, device_name):
        """Get IPs which are associated to a device

        :param device_name: Name of the device
        :return: ip address information
        """
        return self.netbox_con.get('/ipam/ip-addresses', device=device_name)

    def get_ip_by_virtual_machine(self, vm_name):
        """Get IPs which are associated to a virtual-machine

        :param vm_name: Name of the virtual machine
        :return: ip address information
        """
        return self.netbox_con.get('/ipam/ip-addresses', virtual_machine=vm_name)

    def create_ip_address(self, address, **kwargs):
        """Create a new ip address

        :param address: IP address
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"address": address}
        return self.netbox_con.post('/ipam/ip-addresses/', required_fields, **kwargs)

    def update_ip(self, ip_address, **kwargs):
        """Update ip address

        :param ip_address: ip address with prefix. Format: 1.1.1.1/32
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            ip_id = self.get_ip_addresses(address=ip_address)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('ip: {}'.format(ip_address)) from None
        return self.netbox_con.patch('/ipam/ip-addresses/', ip_id, **kwargs)

    def delete_ip_address(self, ip_address):
        """Delete IP address

        :param ip_address: IP address to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            ip_id = self.get_ip_addresses(address=ip_address)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('ip: {}'.format(ip_address)) from None
        return self.netbox_con.delete('/ipam/ip-addresses/', ip_id)

    def delete_ip_by_id(self, ip_id):
        """Delete IP address

        :param ip_id: ID of ip address to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        return self.netbox_con.delete('/ipam/ip-addresses/', ip_id)

    def get_ip_prefixes(self, **kwargs):
        """Return all ip prefixes"""
        return self.netbox_con.get('/ipam/prefixes/', **kwargs)

    def create_ip_prefix(self, prefix, **kwargs):
        """Create a new ip prefix

        :param prefix: A valid ip prefix format. The syntax will be checked with the ipaddress module
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"prefix": prefix}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/prefixes/', required_fields, **kwargs)

    def delete_ip_prefix(self, **kwargs):
        """Delete IP prefix

        :param kwargs: Delete prefix based on filter values
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            ip_prefix_id = self.get_ip_prefixes(**kwargs)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('ip-prefix') from None
        return self.netbox_con.delete('/ipam/prefixes/', ip_prefix_id)

    def update_ip_prefix(self, ip_prefix, **kwargs):
        """Update ip address

        :param ip_prefix: ip prefix to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            ip_prefix_id = self.get_ip_prefixes(prefix=ip_prefix)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('ip-prefix: {}'.format(ip_prefix)) from None
        return self.netbox_con.patch('/ipam/prefixes/', ip_prefix_id, **kwargs)

    def get_next_available_ip(self, **kwargs):
        """Return next available ip in prefix

        :param kwargs: Use the filter fields from the get_prefixes call
        :return: next available ip
        """
        try:
            prefix_id = self.get_ip_prefixes(**kwargs)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('ip-prefix') from None

        param = '/ipam/prefixes/{}/available-ips/'.format(prefix_id)
        return self.netbox_con.get(param, limit=1)[0]['address']

    def get_vrfs(self, **kwargs):
        """Get all vrfs"""
        return self.netbox_con.get('/ipam/vrfs/', **kwargs)

    def create_vrf(self, name, rd, **kwargs):
        """Create a new vrf

        :param name: Name of the vrf
        :param rd: Route distinguisher in any format
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "rd": rd}
        return self.netbox_con.post('/ipam/vrfs/', required_fields, **kwargs)

    def delete_vrf(self, vrf_name):
        """Delete vrf

        :param vrf_name: Name of vrf to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            vrf_id = self.get_vrfs(name=vrf_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('vrf: {}'.format(vrf_name)) from None
        return self.netbox_con.delete('/ipam/vrfs/', vrf_id)

    def update_vrf(self, vrf_name, **kwargs):
        """Update vrf

        :param vrf_name: name of the vrf to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            vrf_id = self.get_vrfs(name=vrf_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('vrf: {}'.format(vrf_name)) from None
        return self.netbox_con.patch('/ipam/vrfs/', vrf_id, **kwargs)

    def get_aggregates(self, **kwargs):
        """Return all aggregates"""
        return self.netbox_con.get('/ipam/aggregates/', **kwargs)

    def create_aggregate(self, prefix, rir, **kwargs):
        """Creates a new aggregate

        :param prefix: IP Prefix
        :param rir: Name of the RIR
        :param kwargs: Optional Arguments
        :return:
        """
        rir_id = self.get_rirs(name=rir)[0]['id']
        required_fields = {"prefix": prefix, "rir": rir_id}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/aggregates/', required_fields, **kwargs)

    def update_aggregate(self, prefix, **kwargs):
        """Update aggregate

        :param prefix: Prefix of the aggregate
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            aggregate_id = self.get_aggregates(prefix=prefix)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('aggregate: {}'.format(prefix)) from None
        return self.netbox_con.patch('/ipam/aggregates/', aggregate_id, **kwargs)

    def get_rirs(self, **kwargs):
        """Return all rirs"""
        return self.netbox_con.get('/ipam/rirs/', **kwargs)

    def create_rir(self, name, slug):
        """Create new rir

        :param name: Name of the rir
        :param slug: Name of the slug
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/rirs/', required_fields)

    def delete_rir(self, rir_name):
        """Delete rir

        :param rir_name: rir name to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            rir_id = self.get_rirs(name=rir_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rir: {}'.format(rir_name)) from None
        return self.netbox_con.delete('/ipam/rirs/', rir_id)

    def update_rir(self, rir_name, **kwargs):
        """Update rir

        :param rir_name: Name of the rir
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            rir_id = self.get_rirs(name=rir_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rir: {}'.format(rir_name)) from None
        return self.netbox_con.patch('/ipam/rirs/', rir_id, **kwargs)

    def get_roles(self, **kwargs):
        """Return all roles"""
        return self.netbox_con.get('/ipam/roles/', **kwargs)

    def create_role(self, name, slug, **kwargs):
        """Create new prefix/vlan role

        :param name: Name of the prefix/vlan role
        :param slug: Name of the slug
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/roles/', required_fields, **kwargs)

    def delete_role(self, role_name):
        """Delete prefix/vlan role

        :param role_name: prefix/vlan role to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            role_id = self.get_roles(name=role_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('prefix/vlan role: {}'.format(role_name)) from None
        return self.netbox_con.delete('/ipam/role/', role_id)

    def update_role(self, role_name, **kwargs):
        """Update prefix role

        :param role_name: Name of the prefix/vlan role
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            prefix_role_id = self.get_roles(name=role_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('prefix/vlan role: {}'.format(role_name)) from None
        return self.netbox_con.patch('/ipam/roles/', prefix_role_id, **kwargs)

    def get_vlans(self, **kwargs):
        """Return all vlans"""
        return self.netbox_con.get('/ipam/vlans/', **kwargs)

    def create_vlan(self, vid, vlan_name, **kwargs):
        """Create new vlan

        :param vid: ID of the new vlan
        :param vlan_name: Name of the vlan
        :param kwargs: Optional Arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"vid": vid, "name": vlan_name}
        return self.netbox_con.post('/ipam/vlans/', required_fields, **kwargs)

    def delete_vlan(self, vid):
        """Delete VLAN based on VLAN ID

        :param vid: vlan id to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            vid_id = self.get_vlans(vid=vid)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('vlan: {}'.format(vid)) from None
        return self.netbox_con.delete('/ipam/vlans/', vid_id)

    def update_vlan(self, vlan_name, **kwargs):
        """Update vlan

        :param vlan_name: Name of the vlan
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            vlan_id = self.get_vlans(name=vlan_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('vlan: {}'.format(vlan_name)) from None
        return self.netbox_con.patch('/ipam/vlans/', vlan_id, **kwargs)

    def get_vlan_groups(self, **kwargs):
        """Return all vlan groups"""
        return self.netbox_con.get('/ipam/vlan-groups/', **kwargs)

    def create_vlan_group(self, name, slug, **kwargs):
        """Create new vlan-group

        :param name: name of the vlan group
        :param slug: slug
        :param kwargs: Optional Arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/vlan-groups/', required_fields, **kwargs)

    def delete_vlan_group(self, name):
        """Delete VLAN group

        :param name: name of the vlan-group to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            vgrp_id = self.get_vlan_groups(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('vlan: {}'.format(name)) from None
        return self.netbox_con.delete('/ipam/vlan-groups/', vgrp_id)

    def update_vlan_group(self, name, **kwargs):
        """Update vlan-group

        :param name: name of the vlan-group
        :param kwargs: arguments
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            vgrp_ip = self.get_vlan_groups(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('name: {}'.format(name)) from None
        return self.netbox_con.patch('/ipam/vlan-groups/', vgrp_ip, **kwargs)
