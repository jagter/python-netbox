from netbox import exceptions


class Dcim(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_sites(self):
        """Returns the available sites"""
        return self.netbox_con.get('/dcim/sites/')

    def create_site(self, name, slug, **kwargs):
        """Create new site

        :param name: Site name
        :param slug: slug name
        :param kwargs: optional fields
        :return: bool True if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}

        resp_ok, resp_data = self.netbox_con.post('/dcim/sites/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_site(self, site_name):
        """Delete site

        :param site_name: Site to delete
        :return: bool True if succesful otherwase delete exception
        """
        site_id = self.__convert_site(site_name)

        if not self.netbox_con.delete('/dcim/sites/', site_id):
            err_msg = 'Unable to delete site {}'.format(site_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_site(self, site_name):
        """Convert site name to site id

        :param site_name: name of the site to convert
        :return: if site found site_id otherwise bool False
        """
        for item in self.get_sites()['results']:
            if item['name'] == site_name:
                return item['id']

        return False

    def get_racks(self):
        """Returns the available racks"""
        return self.netbox_con.get('/dcim/racks/')

    def create_rack(self, name, site_name, **kwargs):
        """Create new rack

        :param name: Name of the rack
        :param site: Site to add rack to
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise create exception
        """
        site_id = self.__convert_site(site_name)
        required_fields = {"name": name, "site": site_id}
        resp_ok, resp_data = self.netbox_con.post('/dcim/racks/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_rack(self, rack_name):
        """Delete rack

        :param rack_name: Name of the rack to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        rack_id = self.__convert_rack(rack_name)

        if not self.netbox_con.delete('/dcim/racks/', rack_id):
            err_msg = 'Unable to delete rack: {}'.format(rack_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_rack(self, rack_name):
        """Convert rack_name to rack_id

        :param rack_name: Name of the rack to convert
        :return: if rack_name found rack_id otherwise bool False
        """
        for item in self.get_racks()['results']:
            if item['name'] == rack_name:
                return item['id']

        return False

    def get_devices(self):
        """Get all devices"""
        return self.netbox_con.get('/dcim/devices/')

    def get_device_by_name(self, name):
        """Get devices by name

        :param name: Name of the device
        :return: device otherwise NotFoundException
        """
        req = self.get_devices()['results']

        for item in req:
            if item['display_name'] == name:
                return item

        raise exceptions.NotFoundException(name)

    def get_device_by_serial(self, name):
        """Get device by serial

        :param name: serial
        :return: device otherwise raise NotFoundException
        """
        req = self.get_devices()

        for item in req:
            if item['serial'] == name:
                return item

        raise exceptions.NotFoundException(name)

    def get_interfaces_by_device(self, device_name):
        """Get all interfaces by device

        :param device_name: Name of device to get interfaces off
        :return: list of interfaces
        """
        device_id = self.get_device_by_name(device_name)['id']
        param = '/dcim/interfaces/?device_id={}'.format(device_id)

        return self.netbox_con.get(param)['results']

    def get_devices_per_rack(self, name):
        """Get devices which belongs to the given rack

        :param name: Name of the rack
        :return: list of devices otherwise an empty list
        """
        output = []

        for item in self.get_devices()['results']:
            if item['rack'] is not None:
                if item['rack']['name'] == name:
                    output.append(item)

        return output

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
        device_role_id = self.__convert_device_role(device_role)
        site_id = self.__convert_site(site_name)
        device_type_id = self.__convert_device_type(device_type)

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

        resp_ok, resp_data = self.netbox_con.post('/dcim/devices/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_device(self, device_name):
        """

        :param device_name: Device to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        device_id = self.__convert_device(device_name)

        if not self.netbox_con.delete('/dcim/devices/', device_id):
            err_msg = 'Unable to delete device {}'.format(device_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_device(self, device_name):
        """Convert device_name to device_id

        :param device_name: Name of device
        :return: device_id otherwise bool False
        """
        for item in self.get_devices()['results']:
            if item['name'] == device_name:
                return item['id']

        return False

    def get_device_types(self):
        """Get devices by device type"""
        return self.netbox_con.get('/dcim/device-types/')

    def create_device_type(self, model, slug, manufacturer, **kwargs):
        """Create device type

        :param model: Model name
        :param slug: Slug name
        :param manufacturer: Name of the manufacurer
        :param kwargs: optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"model": model, "slug": slug, "manufacturer": manufacturer}
        resp_ok, resp_data = self.netbox_con.post('/dcim/device-types/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_device_type(self, model_name):
        """Delete device type

        :param model_name: Name of the model
        :return: bool True if successful otherwise raise DeleteException
        """
        device_type_id = self.__convert_device_type(model_name)

        if not self.netbox_con.delete('/dcim/device-types/', device_type_id):
            err_msg = 'Unable to delete device-type {}'.format(model_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_device_type(self, model_name):
        """Convert device type model_name to model_id

        :param model_name:
        :return: model_id otherwise bool False
        """
        for item in self.get_device_types()['results']:
            print(item)
            if item['model'] == model_name:
                return item['id']
        return False

    def get_device_roles(self):
        """Return all the device roles"""
        return self.netbox_con.get('/dcim/device-roles/')

    def create_device_role(self, name, color, slug, **kwargs):
        """Create device role

        :param name: Role name
        :param color: HTML color code
        :param slug: Slug name
        :param kwargs: optional arguments
        :return: bool True if successful otherwise CreateException
        """
        required_fields = {"name": name, "color": color, "slug": slug}
        resp_ok, resp_data = self.netbox_con.post('/dcim/device-roles/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_device_role(self, device_role):
        """Delete device by device role

        :param device_role: name of the role
        :return: bool True if successful otherwise raise DeleteException
        """
        device_role_id = self.__convert_device_role(device_role)

        if not self.netbox_con.delete('/dcim/device-roles/', device_role_id):
            err_msg = 'Unable to delete device-role {}'.format(device_role)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_device_role(self, device_role):
        """Convert device role name to id

        :param device_role: Name of device_role
        :return: device_role_id if successful otherwise bool False
        """
        for item in self.get_device_roles()['results']:
            if item['name'] == device_role:
                return item['id']
        return False

    def get_manufactures(self):
        """Return all manufactures"""
        return self.netbox_con.get('/dcim/manufacturers/')['results']

    def create_manufacture(self, name, slug, **kwargs):
        """Create new manufacture

        :param name: Name of manufacture
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        resp_ok, resp_data = self.netbox_con.post('/dcim/manufacturers/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_manufacture(self, manufacture_name):
        """Delete manufacture

        :param manufacture_name: Name of manufacture to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        manufacture_id = self.__convert_manufacture(manufacture_name)

        if not self.netbox_con.delete('/dcim/manufacturers/', manufacture_id):
            err_msg = 'Unable to delete manufacturer: {}'.format(manufacture_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_manufacture(self, manufacture_name):
        """Convert manufacture name to manufacture id

        :param manufacture_name: Name of manufacture
        :return: manufacture id if found otherwise bool False
        """
        for item in self.get_manufactures()['results']:
            if item['name'] == manufacture_name:
                return item['id']
        return False

    def get_platforms(self):
        """Return all platforms"""
        return self.netbox_con.get('/dcim/platforms')

    def create_platform(self, name, slug, **kwargs):
        """Create new platform

        :param name: Name of platform
        :param slug: Name of slug
        :param kwargs: Optional arguments
        :return:
        """
        required_fields = {"name": name, "slug": slug}
        resp_ok, resp_data = self.netbox_con.post('/dcim/platforms/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_platform(self, platform_name):
        """Delete platform

        :param platform_name: Name of platform to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        platform_id = self.__convert_platform(platform_name)

        if not self.netbox_con.delete('/dcim/platforms/', platform_id):
            err_msg = 'Unable to delete platform: {}'.format(platform_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_platform(self, platform_name):
        """Convert platform name to platform id

        :param platform_name: Name of platform
        :return: platform id if found otherwise bool False
        """
        for item in self.get_platforms()['results']:
            if item['name'] == platform_name:
                return item['id']
        return False

