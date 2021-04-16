import netbox.exceptions as exceptions


class Virtualization(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_choices(self, choice_id=None):
        """Return choices for all fields if choice_id is not defined

        :param choice_id: Optional model:field tuple
        """
        return self.netbox_con.get('/virtualization/_choices/', choice_id)

    def get_clusters(self, **kwargs):
        """Return all clusters"""
        return self.netbox_con.get('/virtualization/clusters/', **kwargs)

    def create_cluster(self, name, type, **kwargs):
        """Create a new cluster

        :param name: name of the cluster
        :param type: cluster type
        :param kwargs: optional arguments
        :return: netbox object if successful otherwise exception raised
        """
        try:
            cluster_type_id = self.get_cluster_types(name=type)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster-type: {}".format(name)}) from None

        required_fields = {"name": name, "type": cluster_type_id}
        return self.netbox_con.post('/virtualization/clusters/', required_fields, **kwargs)

    def delete_cluster(self, name):
        """Delete a cluster

        :param name: name of the cluster to delete
        :return: netbox object if succesful otherwase delete exception
        """
        try:
            cluster_id = self.get_clusters(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster {}".format(name)}) from None
        return self.netbox_con.delete('/virtualization/clusters/', cluster_id)

    def delete_cluster_by_id(self, cluster_id):
        """Delete a cluster

        :param cluster_id: cluster to delete
        :return: netbox object if succesful otherwase delete exception
        """
        return self.netbox_con.delete('/virtualization/clusters/', cluster_id)

    def update_cluster(self, name, **kwargs):
        """Update cluster

        :param kwargs: filter arguments
        :param name: cluster name to update
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            cluster_id = self.get_clusters(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster: {}".format(name)}) from None
        return self.netbox_con.patch('/virtualization/clusters/', cluster_id, **kwargs)

    def update_cluster_by_id(self, cluster_id, **kwargs):
        """Update cluster

        :param kwargs: filter arguments
        :param cluster_id: cluster to update
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/virtualization/clusters/', cluster_id, **kwargs)

    def get_cluster_types(self, **kwargs):
        """Return all cluster types"""
        return self.netbox_con.get('/virtualization/cluster-types/', **kwargs)

    def create_cluster_type(self, name, slug):
        """Create a new cluster type

        :param name: name of the cluster
        :param slug: slug name
        :return:  netbox object if successful otherwise create exception
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/virtualization/cluster-types/', required_fields)

    def update_cluster_type(self, name, **kwargs):
        """Update cluster type

        :param name: name of the cluster type
        :param kwargs: fields to update
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            type_id = self.get_cluster_types(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster-type: {}".format(name)}) from None
        return self.netbox_con.patch('/virtualization/cluster-types/', type_id, **kwargs)

    def update_cluster_type_by_id(self, cluster_type_id, **kwargs):
        """Update cluster type

        :param cluster_type_id: ID of the cluster type
        :param kwargs: fields to update
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/virtualization/cluster-types/', cluster_type_id, **kwargs)

    def delete_cluster_type(self, name):
        """Delete a cluster type

        :param name: name of the cluster type to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            cluster_type_id = self.get_cluster_types(name=name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster-type: {}".format(name)}) from None
        return self.netbox_con.delete('/virtualization/cluster-types/', cluster_type_id)

    def delete_cluster_type_by_id(self, cluster_type_id):
        """Delete a cluster type

        :param cluster_type_id: cluster type to delete
        :return: bool True if succesful otherwase delete exception
        """
        return self.netbox_con.delete('/virtualization/cluster-types/', cluster_type_id)

    def get_interfaces(self, **kwargs):
        """Return all interfaces"""
        return self.netbox_con.get('/virtualization/interfaces/', **kwargs)

    def get_interface(self, **kwargs):
        """Return interface by filter"""
        return self.netbox_con.get('/virtualization/interfaces/', **kwargs)

    def create_interface(self, name, virtual_machine, **kwargs):
        """Create an interface for a virtual machine

        :param name: name of the interface
        :param virtual_machine: name of virtual machine to attach interface
        :return: netbox object if successful otherwise raise CreateException
        """
        try:
            virtual_machine_id = self.get_virtual_machine(name=virtual_machine)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "virtual-machine: {}".format(virtual_machine)}) from None
        required_fields = {"name": name, "virtual_machine": virtual_machine_id}
        return self.netbox_con.post('/virtualization/interfaces/', required_fields, **kwargs)

    def update_interface(self, name, virtual_machine, **kwargs):
        """Update virtual_machine interface

        :param name: name of the interface to update
        :param virtual_machine: name of the virtual-machine to update
        :param kwargs: update data
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            interface_id = self.get_interface(name=name, virtual_machine=virtual_machine)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "interface: {} or virtual_machine: {}"
                                               .format(name, virtual_machine)}) from None
        return self.netbox_con.patch('/virtualization/interfaces/', interface_id, **kwargs)

    def update_interface_by_id(self, interface_id, **kwargs):
        """Update virtual_machine interface

        :param interface_id: id the interface to update
        :param kwargs: update data
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/virtualization/interfaces/', interface_id, **kwargs)

    def delete_interface(self, name, virtual_machine):
        """Delete interface from virtual_machine

        :param name: interface name to delete
        :param virtual_machine: machine to delete interface from
        :return: bool True if successful otherwise raise DeleteException
        """
        try:
            interface_id = self.get_interface(name=name, virtual_machine=virtual_machine)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "interface: {} or virtual_machine {}"
                                               .format(name, virtual_machine)}) from None

        return self.netbox_con.delete('/virtualization/interfaces/', interface_id)

    def delete_interface_by_id(self, interface_id):
        """Delete interface from virtual_machine

        :param interface_id: interface to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        return self.netbox_con.delete('/virtualization/interfaces/', interface_id)

    def get_virtual_machines(self, **kwargs):
        """Return all virtual-machines"""
        return self.netbox_con.get('/virtualization/virtual-machines/', **kwargs)

    def get_virtual_machine(self, **kwargs):
        """Return virtual-machine based on filter"""
        return self.netbox_con.get('/virtualization/virtual-machines/', **kwargs)

    def create_virtual_machine(self, name, cluster_name, **kwargs):
        """Create a virtual machine
    
        :param name: name of the virtual machine
        :param cluster_name: Name of existing cluster
        :return: netbox object if successful otherwise raise CreateException
        """
        try:
            cluster_id = self.get_clusters(name=cluster_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "cluster-name: {}".format(cluster_name)}) from None

        required_fields = {"name": name, "cluster": cluster_id}
        return self.netbox_con.post('/virtualization/virtual-machines/', required_fields, **kwargs)

    def delete_virtual_machine(self, virtual_machine_name):
        """Delete virtual machine

        :param virtual_machine_name: name of the virtual machine to delete
        :return: bool True if successful otherwise raise exception
        """
        try:
            virtual_machine_id = self.get_virtual_machines(name=virtual_machine_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "virtual-machine: {}".format(virtual_machine_name)}) from None
        return self.netbox_con.delete('/virtualization/virtual-machines/', virtual_machine_id)

    def delete_virtual_machine_by_id(self, virtual_machine_id):
        """Delete virtual machine

        :param virtual_machine_id: virtual machine to delete
        :return: bool True if successful otherwise raise exception
        """
        return self.netbox_con.delete('/virtualization/virtual-machines/', virtual_machine_id)

    def update_virtual_machine(self, virtual_machine_name, **kwargs):
        """Update virtual-machine

        :param virtual_machine_name: name of the virtual-machine to update
        :param kwargs: update data
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            virtual_machine_id = self.get_virtual_machines(name=virtual_machine_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "virtual-machine: {}"
                                               .format(virtual_machine_name)}) from None
        return self.netbox_con.patch('/virtualization/virtual-machines/', virtual_machine_id, **kwargs)

    def update_virtual_machine_by_id(self, virtual_machine_id, **kwargs):
        """Update virtual-machine

        :param virtual_machine_id: virtual-machine to update
        :param kwargs: update data
        :return: bool True if successful otherwise raise UpdateException
        """
        return self.netbox_con.patch('/virtualization/virtual-machines/', virtual_machine_id, **kwargs)
