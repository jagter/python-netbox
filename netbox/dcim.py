import netbox.exceptions as exceptions


class Dcim(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_choices(self, choice_id=None):
        """Return choices for all fields if choice_id is not defined

        :param choice_id: Optional model:field tuple
        """
        return self.netbox_con.get('/dcim/_choices/', choice_id)

    def get_regions(self, **kwargs):
        """Returns the available regions"""
        return self.netbox_con.get('/dcim/regions/', **kwargs)

    def create_region(self, name, slug, **kwargs):
        """Create a new region

        :param name: Region name
        :param slug: slug name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/regions/', required_fields, **kwargs)

    def delete_region(self, region_name):
        """Delete region

        :param region_name: Region to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            region_id = self.get_regions(name=region_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('region: {}'.format(region_name)) from None
        return self.netbox_con.delete('/dcim/regions/', region_id)

    def update_region(self, region_name, **kwargs):
        """

        :param region_name: Region to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            region_id = self.get_regions(name=region_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('region: {}'.format(region_name)) from None
        return self.netbox_con.patch('/dcim/regions/', region_id, **kwargs)

    def get_sites(self, **kwargs):
        """Returns all available sites"""
        return self.netbox_con.get('/dcim/sites/', **kwargs)

    def create_site(self, name, slug, **kwargs):
        """Create a new site

        :param name: Site name
        :param slug: slug name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/sites/', required_fields, **kwargs)

    def delete_site(self, site_name):
        """Delete site

        :param site_name: Site to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            site_id = self.get_sites(name=site_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site_name)) from None
        return self.netbox_con.delete('/dcim/sites/', site_id)

    def update_site(self, site_name, **kwargs):
        """

        :param site_name: Site to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            site_id = self.get_sites(name=site_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site_name)) from None
        return self.netbox_con.patch('/dcim/sites/', site_id, **kwargs)

    def get_racks(self, **kwargs):
        """Returns all available racks"""
        return self.netbox_con.get('/dcim/racks/', **kwargs)

    def create_rack(self, name, site_name, **kwargs):
        """Create new rack

        :param name: Organizational rack name
        :param site_name: The site at which the rack exists
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise create exception
        """
        try:
            site_id = self.get_sites(name=site_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site_name)) from None
        required_fields = {"name": name, "site": site_id}
        return self.netbox_con.post('/dcim/racks/', required_fields, **kwargs)

    def delete_rack(self, rack_name):
        """Delete rack

        :param rack_name: Name of the rack to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            rack_id = self.get_racks(name=rack_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rack: {}'.format(rack_name)) from None
        return self.netbox_con.delete('/dcim/racks/', rack_id)

    def update_rack(self, rack_name, **kwargs):
        """

        :param rack_name: rack_name name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            rack_id = self.get_racks(facility_id=rack_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rack: {}'.format(rack_name)) from None
        return self.netbox_con.patch('/dcim/racks/', rack_id, **kwargs)

    def get_rack_groups(self, **kwargs):
        """Returns all available rack groups"""
        return self.netbox_con.get('/dcim/rack-groups/', **kwargs)

    def create_rack_group(self, name, slug, site_name, **kwargs):
        """Create new rack group

        :param name: Rack group name
        :param slug: slug name
        :param site_name: The site at which the rack exists
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise create exception
        """
        try:
            site_id = self.get_sites(name=site_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site_name)) from None
        required_fields = {"name": name, "slug": slug, "site": site_id}
        return self.netbox_con.post('/dcim/rack-groups/', required_fields, **kwargs)

    def delete_rack_group(self, name):
        """Delete rack group

        :param name: Name of the rack group to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            rack_group_id = self.get_rack_groups(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rack-group: {}'.format(name)) from None
        return self.netbox_con.delete('/dcim/rack-groups/', rack_group_id)

    def update_rack_group(self, name, **kwargs):
        """

        :param name: Rack group name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            rack_group_id = self.get_rack_groups(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rack group: {}'.format(name)) from None
        return self.netbox_con.patch('/dcim/rack-groups/', rack_group_id, **kwargs)

    def get_devices(self, **kwargs):
        """Get all devices"""
        return self.netbox_con.get('/dcim/devices/', **kwargs)

    def get_devices_per_rack(self, rack_name, **kwargs):
        """Get devices which belongs to the given rack

        :param rack_name: Name of the rack
        :return: list of devices otherwise an empty list
        """
        try:
            rack_id = self.get_racks(name=rack_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('rack: {}'.format(rack_name)) from None
        return self.netbox_con.get('/dcim/devices', rack_id=rack_id, **kwargs)

    def create_device(self, name, device_role, site_name, device_type, **kwargs):
        """Create a new device

        :param name: Name of the device
        :param device_role: Device role for the device
        :param site_name: Name of the site where the device is created
        :param device_type: Type for the new device
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name}
        try:
            device_role_id = self.get_device_roles(name=device_role)[0]['id']
            required_fields.update({"device_role": device_role_id})
        except IndexError:
            raise exceptions.NotFoundException('device-role: {}'.format(device_role)) from None

        try:
            site_id = self.get_sites(name=site_name)[0]['id']
            required_fields.update({"site": site_id})
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site_name)) from None

        try:
            device_type_id = self.get_device_types(model=device_type)[0]['id']
            required_fields.update({"device_type": device_type_id})
        except IndexError:
            raise exceptions.NotFoundException('device-type: {}'.format(device_type)) from None

        return self.netbox_con.post('/dcim/devices/', required_fields, **kwargs)

    def delete_device(self, device_name):
        """Delete device by name

        :param device_name: Device to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            device_id = self.get_devices(name=device_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device: {}'.format(device_name)) from None
        return self.netbox_con.delete('/dcim/devices/', device_id)

    def update_device(self, device_name, **kwargs):
        """Update device by device name

        :param device_name: device name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        device_id = self.get_devices(name=device_name)[0]['id']
        return self.netbox_con.patch('/dcim/devices/', device_id, **kwargs)

    def get_device_types(self, **kwargs):
        """Get devices by device type"""
        return self.netbox_con.get('/dcim/device-types/', **kwargs)

    def create_device_type(self, model, slug, manufacturer, **kwargs):
        """Create device type

        :param model: Model name
        :param slug: Slug name
        :param manufacturer: Name of the manufacurer
        :param kwargs: optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"model": model, "slug": slug, "manufacturer": manufacturer}
        return self.netbox_con.post('/dcim/device-types/', required_fields, **kwargs)

    def update_device_type(self, device_type, **kwargs):
        """Update device type

        :param device_type: device-type name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            device_type_id = self.get_device_types(model=device_type)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device-type: {}'.format(device_type)) from None
        return self.netbox_con.patch('/dcim/device-types/', device_type_id, **kwargs)

    def delete_device_type(self, model_name):
        """Delete device type

        :param model_name: Name of the model
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            device_type_id = self.get_device_types(model=model_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device-type: {}'.format(model_name)) from None
        return self.netbox_con.delete('/dcim/device-types/', device_type_id)

    def get_device_roles(self, **kwargs):
        """Return all the device roles"""
        return self.netbox_con.get('/dcim/device-roles/', **kwargs)

    def create_device_role(self, name, color, slug, **kwargs):
        """Create device role

        :param name: Role name
        :param color: HTML color code
        :param slug: Slug name
        :param kwargs: optional arguments
        :return: netbox object if successful otherwise CreateException
        """
        required_fields = {"name": name, "color": color, "slug": slug}
        return self.netbox_con.post('/dcim/device-roles/', required_fields, **kwargs)

    def update_device_role(self, device_role, **kwargs):
        """Update device role

        :param device_role: device-type name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            device_role_id = self.get_device_roles(name=device_role)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device-role: {}'.format(device_role)) from None
        return self.netbox_con.patch('/dcim/device-roles/', device_role_id, **kwargs)

    def delete_device_role(self, device_role):
        """Delete device by device role

        :param device_role: name of the role
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            device_role_id = self.get_device_roles(name=device_role)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device-role: {}'.format(device_role)) from None
        return self.netbox_con.delete('/dcim/device-roles/', device_role_id)

    def get_manufacturers(self, **kwargs):
        """Return all manufactures"""
        return self.netbox_con.get('/dcim/manufacturers/', **kwargs)

    def create_manufacturer(self, name, slug, **kwargs):
        """Create new manufacturer

        :param name: Name of manufacturer
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/manufacturers/', required_fields, **kwargs)

    def update_manufacturer(self, manufacturer_name, **kwargs):
        """Update manufacturer

        :param manufacturer_name: manufacturer name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            manufacturer_id = self.get_manufacturers(name=manufacturer_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('manufacturer: {}'.format(manufacturer_name)) from None
        return self.netbox_con.patch('/dcim/manufacturer/', manufacturer_id, **kwargs)

    def delete_manufacturer(self, manufacturer_name):
        """Delete manufacturer

        :param manufacturer_name: Name of manufacturer to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            manufacturer_id = self.get_manufacturers(name=manufacturer_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('manufacturer: {}'.format(manufacturer_name)) from None
        return self.netbox_con.delete('/dcim/manufacturers/', manufacturer_id)

    def get_platforms(self, **kwargs):
        """Return all platforms"""
        return self.netbox_con.get('/dcim/platforms', **kwargs)

    def create_platform(self, name, slug, **kwargs):
        """Create new platform

        :param name: Name of platform
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return:
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/dcim/platforms/', required_fields, **kwargs)

    def update_platform(self, platform_name, **kwargs):
        """Update platform

        :param platform_name: device name to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            platform_id = self.get_platforms(name=platform_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('platform: {}'.format(platform_name)) from None
        return self.netbox_con.patch('/dcim/platforms/', platform_id, **kwargs)

    def delete_platform(self, platform_name):
        """Delete platform

        :param platform_name: Name of platform to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            platform_id = self.get_platforms(name=platform_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('platform: {}'.format(platform_name)) from None
        return self.netbox_con.delete('/dcim/platforms/', platform_id)

    def get_interfaces(self, **kwargs):
        """Return interfaces"""
        return self.netbox_con.get('/dcim/interfaces', **kwargs)

    def create_interface(self, name, interface_type, device_id, **kwargs):
        """Create a new interface

        :param name: name of the interface
        :param interface_type: interface type. It is not possible to get the list of types from the api. Search in the netbox code for the correct type number.
        :param kwargs: optional arguments
        :param device_id: ID of the device to associate interface with
        :return: netbox object if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "type": interface_type, "device": device_id}
        return self.netbox_con.post('/dcim/interfaces/', required_fields, **kwargs)

    def update_interface(self, interface, device, **kwargs):
        """Update interface

        :param interface: interface to update
        :param device: name of the device
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            interface_id = self.get_interfaces(name=interface, device=device)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('interface: {}'.format(interface)) from None
        return self.netbox_con.patch('/dcim/interfaces/', interface_id, **kwargs)

    def delete_interface(self, interface_name, device):
        """Delete interface

        :param interface_name: Name of interface to delete
        :param device: Device to which the interface belongs
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            interface_id = self.get_interfaces(name=interface_name, device=device)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('interface: {}'.format(interface_name)) from None
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

    def delete_interface_connection(self, interface_connection_id):
        """Delete interface-connection by id

        :param interface_connection_id: id of interface-connection to remove
        :return: bool True if successful otherwise raise DeleteException
        """
        return self.netbox_con.delete('/dcim/interface-connections/', interface_connection_id)

    def update_interface_connection(self, interface_connection_id, **kwargs):
        """Update interface

        :param interface_connection_id: interface_connection to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/dcim/interface-connections/', interface_connection_id, **kwargs)

    def get_interface_templates(self, **kwargs):
        """Return interface templates"""
        return self.netbox_con.get('/dcim/interface-templates', **kwargs)

    def create_interface_template(self, name, device_type, **kwargs):
        """Create a new interface template

        :param name: name of the interface
        :param kwargs: optional arguments
        :param device_type: name of the device_type to associate template with
        :return: netbox object if successful otherwise raise CreateException
        """
        try:
            device_type_id = self.get_device_types(model=device_type)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device-type: {}'.format(device_type)) from None
        required_fields = {"name": name, "device_type": device_type_id}
        return self.netbox_con.post('/dcim/interface-templates/', required_fields, **kwargs)

    def update_interface_template(self, interface_template_name, **kwargs):
        """Update interface template

        :param interface_template_name: interface template to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            interface_template_id = self.get_interface_templates(name=interface_template_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('interface: {}'.format(interface_template_name)) from None
        return self.netbox_con.patch('/dcim/interface-templates/', interface_template_id, **kwargs)

    def delete_interface_template(self, interface_template_name):
        """Delete interface template

        :param interface_template_name: Name of interface template to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            interface_template_id = self.get_interface_templates(name=interface_template_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('interface-template: {}'.format(interface_template_name)) from None
        return self.netbox_con.delete('/dcim/interface-templates/', interface_template_id)

    def get_inventory_items(self, **kwargs):
        """Return inventory items"""
        return self.netbox_con.get('/dcim/inventory-items/', **kwargs)

    def create_inventory_item(self, name, device_name, **kwargs):
        """Create inventory item

        :param name: Inventory item name
        :param device_name: Name of device
        :param kwargs: Extra inventory parameters
        :return: netbox object if successful otherwise raise CreateException
        """
        try:
            device_id = self.get_devices(name=device_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('device: {}'.format(device_name)) from None
        required_fields = {"name": name, "device": device_id}
        return self.netbox_con.post('/dcim/inventory-items/', required_fields, **kwargs)

    def update_inventory_item(self, name, device_name, **kwargs):
        """Update inventory item

        :param name: Inventory item name
        :param device_name: Name of device
        :param kwargs: Extra inventory items to update
        :return bool True if successful otherwise raise UpdateException
        """
        try:
            inventory_item_id = self.get_inventory_items(name=name, device=device_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('inventory item: {}'.format(name)) from None
        return self.netbox_con.patch('/dcim/inventory-items/', inventory_item_id, **kwargs)

    def delete_inventory_item(self, name, device_name):
        """Delete inventory item

        :param name: Name of inventory item to delete
        :param device_name: Name of the device to remove inventory item from
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            inventory_item_id = self.get_inventory_items(name=name, device=device_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('inventory item: {}'.format(name)) from None
        return self.netbox_con.delete('/dcim/inventory-items/', inventory_item_id)
