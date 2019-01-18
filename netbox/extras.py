import netbox.exceptions as exceptions


class Extras(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_config_contexts(self, **kwargs):
        """Returns all config-contexts"""
        return self.netbox_con.get('/extras/config-contexts/', **kwargs)

    def create_config_context(self, name, data, **kwargs):
        """Create a config-context

        :param name: config-context name
        :param data: data in json format
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "data": data}
        return self.netbox_con.post('/extras/config-contexts/', required_fields, **kwargs)

    def delete_config_context(self, name):
        """Delete config-context

        :param name: Name of the config-context to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            config_context_id = self.get_config_contexts(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('config-context: {}'.format(name)) from None
        return self.netbox_con.delete('/extras/config-contexts/', config_context_id)

    def update_config_context(self, name, **kwargs):
        """Update config-context

        :param name: config-context to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            config_context_id = self.get_config_contexts(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('config-context: {}'.format(name)) from None

        return self.netbox_con.patch('/extras/config-contexts/', config_context_id, **kwargs)

    def get_tags(self, **kwargs):
        """Returns all tags"""
        return self.netbox_con.get('/extras/tags/', **kwargs)

    def create_tag(self, name, slug, **kwargs):
        """Create a tag

        :param name: tag name
        :param slug: tag slug
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/extras/tags/', required_fields, **kwargs)

    def delete_tag(self, name):
        """Delete tag

        :param name: Name of the tag to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            tag_id = self.get_tags(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tag: {}'.format(name)) from None
        return self.netbox_con.delete('/extras/tags/', tag_id)

    def update_tag(self, name, **kwargs):
        """Update tag

        :param name: tag name
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            tag_id = self.get_tags(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('tag: {}'.format(name)) from None

        return self.netbox_con.patch('/extras/tags/', tag_id, **kwargs)

    def get_object_changes(self, **kwargs):
        """Returns all object changes"""
        return self.netbox_con.get('/extras/object-changes/', **kwargs)

    def get_reports(self):
        """Returns all reports"""
        return self.netbox_con.get('/extras/reports/')
