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
    
    def get_contacts(self, **kwargs):
        """Returns the contacts"""
        return self.netbox_con.get('/tenancy/contacts/', **kwargs)
    
    def get_contact_assignments(self, **kwargs):
        """Returns the contacts"""
        return self.netbox_con.get('/tenancy/contact-assignments/', **kwargs)
    
    def get_contact_roles(self, **kwargs):
        """Returns the roles for contacts"""
        return self.netbox_con.get('/tenancy/contact-roles/', **kwargs)

    def create_tenant(self, name, slug, **kwargs):
        """Create a new tenant

        :param name: Tenant name
        :param slug: slug name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/tenancy/tenants/', required_fields, **kwargs)
    
    def create_contact(self, name: str, **kwargs):
        """Create a new contact

        :param name: Contact name
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name}
        return self.netbox_con.post('/tenancy/contacts/', required_fields, **kwargs)
    
    def create_contact_assignment_tenant(self, contact_id: int, tenant_id: int, role_id: int, **kwargs):
        """Connect a contect to a tenant

        :param contact_display_name: Contact display name
        :param tenant_id: The ID of the tenant
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {
            "content_type": "tenancy.tenant",
            "object_id": tenant_id,
            "contact": contact_id,
            "role": role_id
        }
        return self.netbox_con.post('/tenancy/contact-assignments/', required_fields, **kwargs)

    def delete_tenant(self, tenant_name):
        """Delete tenant

        :param tenant_name: Tenant to delete
        :return: bool True if succesful otherwise delete exception
        """
        try:
            tenant_id = self.get_tenants(name=tenant_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "tenant: {}".format(tenant_name)}) from None
        return self.netbox_con.delete('/tenancy/tenants/', tenant_id)

    def delete_tenant_by_id(self, tenant_id):
        """Delete tenant

        :param tenant_id: Tenant to delete
        :return: bool True if succesful otherwise delete exception
        """
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
            raise exceptions.NotFoundException({"detail": "tenant: {}".format(tenant_name)}) from None
        return self.netbox_con.patch('/tenancy/tenants/', tenant_id, **kwargs)

    def update_tenant_by_id(self, tenant_id, **kwargs):
        """Update tenant

        :param tenant_id: tenant to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
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
        :return: bool True if succesful otherwise delete exception
        """
        try:
            tenant_group_id = self.get_tenant_groups(name=tenant_group_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "tenant: {}".format(tenant_group_name)}) from None
        return self.netbox_con.delete('/tenancy/tenant-groups/', tenant_group_id)

    def delete_tenant_group_id(self, tenant_group_id):
        """Delete tenant

        :param tenant_group_id: Tenant group to delete
        :return: bool True if succesful otherwise delete exception
        """
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
            raise exceptions.NotFoundException({"detail:": "tenant-group: {}".format(tenant_group_name)}) from None
        return self.netbox_con.patch('/tenancy/tenant-groups/', tenant_group_id, **kwargs)

    def update_tenant_group_by_id(self, tenant_group_id, **kwargs):
        """Update tenant group

        :param tenant_group_id: tenant group to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/tenancy/tenant-groups/', tenant_group_id, **kwargs)
