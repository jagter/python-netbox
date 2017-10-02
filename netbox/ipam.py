import ipaddress
from netbox import exceptions

class Ipam(object):

    def __init__(self, netbox_con):

        self.netbox_con = netbox_con

    def get_ip_addresses(self):
        """Return all ip addresses"""
        return self.netbox_con.get('/ipam/ip-addresses/')

    def get_ip(self, **kwargs):
        """Return query results"""
        return self.netbox_con.get('/ipam/ip-addresses/', **kwargs)

    def get_ip_by_device(self, device_name):
        """Get IPs which are associated to a device

        :param device_name: Name of the device
        :return: ip address information
        """
        return self.netbox_con.get('/ipam/ip-addresses', device_name=device_name)

    def create_ip_address(self, address, **kwargs):
        """Create a new ip address

        :param address: IP address
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"address": address}
        return self.netbox_con.post('/ipam/ip-addresses/', required_fields, **kwargs)

    def delete_ip_address(self, address):
        """Delete IP address

        :param address: IP address to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_address_id = self.get_ip(address)
        return self.netbox_con.delete('/ipam/ip-addresses/', ip_address_id)

    def __convert_ip_address(self, ip_address):
        """Convert IP address to id

        :param ip_address: The IP address
        :return: ip address id if found otherwise bool False
        """
        for item in self.get_ip_addresses()['results']:
            if item['address'] == ip_address:
                return item['id']
        return False

    def get_ip_prefixes(self):
        """Return all ip prefixes"""
        return self.netbox_con.get('/ipam/prefixes/')

    def get_ip_prefix(self, **kwargs):
        """Get prefix based on filter values

        :param kwargs: filter values
        :return: prefix
        """
        return self.netbox_con.get('/ipam/prefixes/', **kwargs)

    def create_ip_prefix(self, prefix, **kwargs):
        """Create a new ip prefix

        :param prefix: A valid ip prefix format. The syntax will be checked with the ipaddress module
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"prefix": prefix}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/prefixes/', required_fields, **kwargs)

    def delete_ip_prefix(self, **kwargs):
        """Delete IP prefix

        :param kwargs: Delete prefix based on filter values
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_prefix_id = self.get_ip_prefix(**kwargs)[0]['id']
        return self.netbox_con.delete('/ipam/prefixes/', ip_prefix_id)

    def get_next_available_ip(self, **kwargs):
        """Return next available ip in prefix

        :param kwargs: filter for prefix
        :return: next available ip
        """
        prefix_id =  self.get_ip_prefix(**kwargs)[0]['id']
        param = '/ipam/prefixes/{}/available-ips/'.format(prefix_id)
        return self.netbox_con.get(param, limit=1)[0]['address']

    def get_vrfs(self):
        """Get all vrfs"""
        return self.netbox_con.get('/ipam/vrfs/')

    def get_vrf(self, **kwargs):
        """Get vrf based on filter values

        :param kwargs: Filter values
        :return: vrf
        """
        return self.netbox_con.get('/ipam/vrfs/', **kwargs)

    def create_vrf(self, name, rd, **kwargs):
        """Create a new vrf

        :param name: Name of the vrf
        :param rd: Route distinguisher in any format
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "rd": rd}
        return self.netbox_con.post('/ipam/vrfs/', required_fields, **kwargs)

    def delete_vrf(self, vrf):
        """Delete vrf

        :param vrf: Name of vrf to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vrf_id = self.get_vrf(name=vrf)[0]['id']
        return self.netbox_con.delete('/ipam/vrfs/', vrf_id)

    def get_aggregates(self):
        """Return all aggregates"""
        return self.netbox_con.get('/ipam/aggregates/')

    def create_aggregate(self, prefix, rir, **kwargs):
        """Creates a new aggregate

        :param prefix: IP Prefix
        :param rir: Name of the RIR
        :param kwargs: Optional Arguments
        :return:
        """
        rir_id = self.get_rir(name=rir)[0]['id']
        required_fields = {"prefix": prefix, "rir": rir_id}

        if ipaddress.ip_network(prefix, strict=True):
            return self.netbox_con.post('/ipam/aggregates/', required_fields, **kwargs)

    def get_rirs(self):
        """Return all rirs"""
        return self.netbox_con.get('/ipam/rirs/')

    def get_rir(self, **kwargs):
        """Get rir based on filter values

        :param kwargs: Filter values
        :return: rir
        """
        return self.netbox_con.get('/ipam/rirs', **kwargs)

    def create_rir(self, name, slug):
        """Create new rir

        :param name: Name of the rir
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/rirs/', required_fields)

    def delete_rir(self, rir_name):
        """Delete rir

        :param rir_name: rir name to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        rir_id = self.get_rir(name=rir_name)[0]['id']
        return self.netbox_con.delete('/ipam/rirs/', rir_id)

    def get_prefix_roles(self):
        """Return all roles"""
        return self.netbox_con.get('/ipam/roles/')

    def get_prefix_role(self, **kwargs):
        """Return prefix role based on filter

        :param kwargs: filter options
        :return: prefix role
        """
        return self.netbox_con.get('/ipam/roles/', **kwargs)

    def create_prefix_role(self, name, slug):
        """Create new prefix role

        :param name: Name of the prefix role
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/ipam/roles/', required_fields)

    def delete_prefix_role(self, prefix_role):
        """Delete prefix role

        :param prefix_role: prefix role to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        prefix_role_id = self.get_prefix_role(name=prefix_role)[0]['id']
        return self.netbox_con.delete('/ipam/role/', prefix_role_id)



    def get_vlans(self):
        """Return all vlans"""
        return self.netbox_con.get('/ipam/vlans/')

    def get_vlan(self, **kwargs):
        """Get vlan by filter

        :param kwargs: Filter values
        :return: vlan
        """
        return self.netbox_con.get('/ipam/vlans/', **kwargs)

    def create_vlan(self, vid, vlan_name):
        """Create new vlan

        :param vid: ID of the new vlan
        :param vlan_name: Name of the vlan
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"vid": vid, "name": vlan_name}
        return self.netbox_con.post('/ipam/vlans/', required_fields)

    def delete_vlan(self, vid):
        """Delete VLAN based on VLAN ID

        :param vid: vlan id to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vid_id = self.get_vlan(vid=vid)[0]['id']
        return self.netbox_con.delete('/ipam/vlans/', vid_id)


