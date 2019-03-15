import netbox.exceptions as exceptions


class Tenancy(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_choices(self, choice_id=None):
        """Return choices for all fields if choice_id is not defined

        :param choice_id: Optional model:field tuple
        """
        return self.netbox_con.get('/tenancy/_choices/', choice_id)

    def get_tenants(self, **kwargs):
        """Returns the tenants"""
        return self.netbox_con.get('/tenancy/tenants/', **kwargs)

    def create_tenant(self, name, slug, **kwargs):
        """Create a new tenant

        :param name: Tenant name
        :param slug: slug name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/tenancy/tenants/', required_fields, **kwargs)

    def delete_tenant(self, tenant_name):
        """Delete tenant

        :param tenant_name: Tenant to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            tenant_id = self.get_tenants(name=tenant_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tenant: {}'.format(tenant_name)) from None
        return self.netbox_con.delete('/tenancy/tenants/', tenant_id)

    def update_tenant(self, tenant_name, **kwargs):
        """Update tenant

        :param tenant_name: tenant to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            tenant_id = self.get_tenants(name=tenant_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tenant: {}'.format(tenant_name)) from None
        return self.netbox_con.patch('/tenancy/tenants/', tenant_id, **kwargs)

    def get_tenant_groups(self, **kwargs):
        """Returns the tenant groups"""
        return self.netbox_con.get('/tenancy/tenant-groups/', **kwargs)

    def create_tenant_group(self, name, slug, **kwargs):
        """Create a new tenant-group

        :param name: Tenant-group name
        :param slug: slug name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/tenancy/tenant-groups/', required_fields, **kwargs)

    def delete_tenant_group(self, tenant_group_name):
        """Delete tenant

        :param tenant_group_name: Tenant group to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            tenant_group_id = self.get_tenant_groups(name=tenant_group_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tenant: {}'.format(tenant_group_name)) from None
        return self.netbox_con.delete('/tenancy/tenant-groups/', tenant_group_id)

    def update_tenant_group(self, tenant_group_name, **kwargs):
        """Update tenant group

        :param tenant_group_name: tenant group to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            tenant_group_id = self.get_tenant_groups(name=tenant_group_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tenant-group: {}'.format(tenant_group_name)) from None
        return self.netbox_con.patch('/tenancy/tenant-groups/', tenant_group_id, **kwargs)
