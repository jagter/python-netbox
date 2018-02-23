import netbox.exceptions as exceptions


class Tenancy(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_tenants(self, **kwargs):
        """Returns the tenants"""
        return self.netbox_con.get('/tenancy/tenants/', **kwargs)

    def create_tenant(self, name, slug, **kwargs):
        """Create a new tenant

        :param name: Tenant name
        :param slug: slug name
        :param kwargs: optional fields
        :return: bool True if successful otherwise exception raised
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