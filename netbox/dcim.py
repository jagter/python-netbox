class Dcim(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_sites(self):
        """Returns the available sites"""
        return self.netbox_con.get('/dcim/sites/')

    def get_site(self, **kwargs):
        """Get site by filter

        :param kwargs: Filter can be any field.
        :return: site result
        """
        return self.netbox_con.get('/dcim/sites/', **kwargs)

    def create_site(self, name, slug, **kwargs):
        """Create new site

        :param name: Site name
        :param slug: slug name
        :param kwargs: optional fields
        :return: bool True if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/sites/', required_fields, **kwargs)

    def delete_site(self, site_name):
        """Delete site

        :param site_name: Site to delete
        :return: bool True if succesful otherwase delete exception
        """
        site_id = self.get_site(name=site_name)[0]['id']
        return self.netbox_con.delete('/dcim/sites/', site_id)

    def update_site(self, site_name, **kwargs):
        """

        :param site_name: device-type name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        site_id = self.get_site(name=site_name)[0]['id']
        return self.netbox_con.patch('/dcim/sites/', site_id, **kwargs)

    def get_racks(self):
        """Returns the available racks"""
        return self.netbox_con.get('/dcim/racks/')

    def get_rack(self, **kwargs):
        """Return rack id based on name

        :param kwargs:
        :return: Rack
        """
        return self.netbox_con.get('/dcim/racks/', **kwargs)

    def create_rack(self, name, site_name, **kwargs):
        """Create new rack

        :param name: Organizational rack name
        :param site_name: The site at which the rack exists
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise create exception
        """
        site_id = self.get_site(name=site_name)[0]['id']
        required_fields = {"name": name, "site": site_id}
        return self.netbox_con.post('/dcim/racks/', required_fields, **kwargs)

    def delete_rack(self, rack_name):
        """Delete rack

        :param rack_name: Name of the rack to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        rack_id = self.get_rack(facility_id=rack_name)[0]['id']
        return self.netbox_con.delete('/dcim/racks/', rack_id)

    def update_rack(self, rack_name, **kwargs):
        """

        :param rack_name: rack_name name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        rack_id = self.get_rack(facility_id=rack_name)[0]['id']
        return self.netbox_con.patch('/dcim/racks/', rack_id, **kwargs)

    def get_devices(self):
        """Get all devices"""
        return self.netbox_con.get('/dcim/devices/')

    def get_device(self, **kwargs):
        """Get device by filter

        :param kwargs: Filter can be any field.
        :return: device result
        """
        return self.netbox_con.get('/dcim/devices/', **kwargs)

    def get_devices_per_rack(self, rack_name, **kwargs):
        """Get devices which belongs to the given rack

        :param rack_name: Name of the rack
        :return: list of devices otherwise an empty list
        """
        rack_id = self.get_rack(facility_id=rack_name)[0]['id']
        return self.netbox_con.get('/dcim/devices', rack_id=rack_id, **kwargs)

    def create_device(self, name, device_role, site_name, device_type, **kwargs):
        """Create a new device

        :param name: Name of the device
        :param device_role: Device role for the device
        :param site_name: Name of the site where the device is created
        :param device_type: Type for the new device
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name}
        device_role_id = self.get_device_role(name=device_role)[0]['id']
        site_id = self.get_site(name=site_name)[0]['id']
        device_type_id = self.get_device_type(model=device_type)[0]['id']

        if device_role_id:
            required_fields.update({"device_role": device_role_id})
        else:
            err_msg = 'Unable to create device. device role {} not found'.format(device_role)
            raise ValueError(err_msg)

        if site_id:
            required_fields.update({"site": site_id})
        else:
            err_msg = 'Unable to create device. site {} not found'.format(site_name)
            raise ValueError(err_msg)

        if device_type_id:
            required_fields.update({"device_type": device_type_id})
        else:
            err_msg = 'Unable to create device. device_type {} not found'.format(device_type)
            raise ValueError(err_msg)

        return self.netbox_con.post('/dcim/devices/', required_fields, **kwargs)

    def delete_device(self, device_name):
        """

        :param device_name: Device to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        device_id = self.get_device(name=device_name)[0]['id']
        return self.netbox_con.delete('/dcim/devices/', device_id)

    def update_device(self, device, **kwargs):
        """

        :param device: device name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_id = self.get_device(name=device)[0]['id']
        return self.netbox_con.patch('/dcim/devices/', device_id, **kwargs)

    def get_device_types(self):
        """Get devices by device type"""
        return self.netbox_con.get('/dcim/device-types/')

    def get_device_type(self, **kwargs):
        """Get device type by filter

        :param kwargs: Search filter
        :return: device type
        """
        return self.netbox_con.get('/dcim/device-types/', **kwargs)

    def create_device_type(self, model, slug, manufacturer, **kwargs):
        """Create device type

        :param model: Model name
        :param slug: Slug name
        :param manufacturer: Name of the manufacurer
        :param kwargs: optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"model": model, "slug": slug, "manufacturer": manufacturer}
        return self.netbox_con.post('/dcim/device-types/', required_fields, **kwargs)

    def update_device_type(self, device_type, **kwargs):
        """Update device type

        :param device_type: device-type name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_id = self.get_device_type(model=device_type)[0]['id']
        return self.netbox_con.patch('/dcim/device-types/', device_id, **kwargs)

    def delete_device_type(self, model_name):
        """Delete device type

        :param model_name: Name of the model
        :return: bool True if successful otherwise raise DeleteException
        """
        device_type_id = self.get_device_type(model=model_name)[0]['id']
        return self.netbox_con.delete('/dcim/device-types/', device_type_id)

    def get_device_roles(self):
        """Return all the device roles"""
        return self.netbox_con.get('/dcim/device-roles/')

    def get_device_role(self, **kwargs):
        """Get device role by filter

        :param kwargs: Search filter
        :return: device role
        """
        return self.netbox_con.get('/dcim/device-roles/', **kwargs)

    def create_device_role(self, name, color, slug, **kwargs):
        """Create device role

        :param name: Role name
        :param color: HTML color code
        :param slug: Slug name
        :param kwargs: optional arguments
        :return: bool True if successful otherwise CreateException
        """
        required_fields = {"name": name, "color": color, "slug": slug}
        return self.netbox_con.post('/dcim/device-roles/', required_fields, **kwargs)

    def update_device_role(self, device_role, **kwargs):
        """Update device role

        :param device_type: device-type name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_role_id = self.get_device_type(name=device_role)[0]['id']
        return self.netbox_con.patch('/dcim/device-roles/', device_role_id, **kwargs)

    def delete_device_role(self, device_role):
        """Delete device by device role

        :param device_role: name of the role
        :return: bool True if successful otherwise raise DeleteException
        """
        device_role_id = self.get_device_role(name=device_role)[0]['id']
        return self.netbox_con.delete('/dcim/device-roles/', device_role_id)

    def get_manufactures(self):
        """Return all manufactures"""
        return self.netbox_con.get('/dcim/manufacturers/')

    def get_manufacturer(self, **kwargs):
        """Get manufacturer by filter

        :param kwargs: Search filter
        :return: manufacturer
        """
        return self.netbox_con.get('/dcim/manufacturers/', **kwargs)

    def create_manufacturer(self, name, slug, **kwargs):
        """Create new manufacturer

        :param name: Name of manufacturer
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/manufacturers/', required_fields, **kwargs)

    def update_manufacturer(self, manufacturer, **kwargs):
        """Update manufacturer

        :param manufacturer: manufacturer name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_role_id = self.get_manufacturer(name=manufacturer)[0]['id']
        return self.netbox_con.patch('/dcim/manufacturer/', device_role_id, **kwargs)

    def delete_manufacturer(self, manufacturer_name):
        """Delete manufacturer

        :param manufacturer_name: Name of manufacturer to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        manufacturer_id = self.get_manufacturer(name=manufacturer_name)[0]['id']
        return self.netbox_con.delete('/dcim/manufacturers/', manufacturer_id)

    def get_platforms(self):
        """Return all platforms"""
        return self.netbox_con.get('/dcim/platforms')

    def get_platform(self, **kwargs):
        """Get platform by filter

        :param kwargs: Search filter
        :return: platform
        """
        return self.netbox_con.get('/dcim/platform/', **kwargs)

    def create_platform(self, name, slug, **kwargs):
        """Create new platform

        :param name: Name of platform
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return:
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/platforms/', required_fields, **kwargs)

    def update_platform(self, platform, **kwargs):
        """Update platform

        :param platform: device name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_role_id = self.get_manufacturer(name=platform)[0]['id']
        return self.netbox_con.patch('/dcim/platforms/', device_role_id, **kwargs)

    def delete_platform(self, platform_name):
        """Delete platform

        :param platform_name: Name of platform to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        platform_id = self.get_platform(name=platform_name)[0]['id']
        return self.netbox_con.delete('/dcim/platforms/', platform_id)

    def get_interfaces(self):
        """Return interfaces"""
        return self.netbox_con.get('/dcim/interfaces')

    def get_interface(self, **kwargs):
        """Get interface by filter

        :param kwargs: Search filter
        :return: interface
        """
        return self.netbox_con.get('/dcim/interfaces/', **kwargs)

    def get_interfaces_by_device(self, device_name):
        """Get all interfaces by device

        :param device_name: Name of device to get interfaces off
        :return: list of interfaces
        """
        return self.netbox_con.get('/dcim/interfaces', device=device_name)

    def create_interface(self, name, form_facter, device, **kwargs):
        """Create a new interface

        :param name: name of the interface
        :param form_facter: interface type. It is not possible to get the list of form factors from the api. Search
        in the netbox code for the correct form factor number.
        :param kwargs: optional arguments
        :param device: name of the device to associate interface with
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "form_factor": form_facter, "device": device}
        return self.netbox_con.post('/dcim/interfaces/', required_fields, **kwargs)

    def update_interface(self, interface, **kwargs):
        """Update interface

        :param interface: interface to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_role_id = self.get_manufacturer(name=interface)[0]['id']
        return self.netbox_con.patch('/dcim/platforms/', device_role_id, **kwargs)

    def delete_interface_by_id(self, interface_id):
        """Delete interface by id

        :param interface_id: id of interface to remove
        :return:
        """
        return self.netbox_con.delete('/dcim/interfaces/', interface_id)

    def get_interface_connections(self, **kwargs):
        """Get interface connections

        :param kwargs: Filter arguments
        :return: list of interface connections
        """
        return self.netbox_con.get('/dcim/interface-connections/', **kwargs)

    def create_interface_connection(self, interface_a, interface_b, **kwargs):
        """Create a new interface-connection

        :param interface_a: id of the source interface
        :param interface_b: id of the destination interface
        :param kwargs:
        :return:
        """
        required_fields = {"interface_a": interface_a, "interface_b": interface_b}
        return self.netbox_con.post('/dcim/interface-connections/', required_fields, **kwargs)

