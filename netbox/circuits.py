import netbox.exceptions as exceptions
from netbox.dcim import Dcim


class Circuits(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con
        self.dcim = Dcim(netbox_con)

    def get_circuits(self, **kwargs):
        """Returns the circuits"""
        return self.netbox_con.get('/circuits/circuits/', **kwargs)

    def create_circuit(self, circuit_provider, cid, circuit_type, status_id, **kwargs):
        """Create a new circuits

        :param circuit_provider: provider name
        :param cid: Unique circuit id
        :param circuit_type: circuit type
        :param status_id: see below for the status codes
        :param kwargs: optional fields
        :return: netbox object if successful otherwise exception raised

        circuit status codes:
        0: Deprovisioning
        1: Active
        2: Planned
        3: Provisioning
        4: Offline
        5: Decommissioned

        """
        try:
            provider_id = self.get_providers(name=circuit_provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('cirtcuit provider: {}'.format(circuit_provider)) from None

        try:
            type_id = self.get_types(name=circuit_type)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit type: {}'.format(circuit_type)) from None

        required_fields = {"provider": provider_id, "cid": cid, "type": type_id,
                           "status": status_id}
        return self.netbox_con.post('/circuits/circuits/', required_fields, **kwargs)

    def delete_circuit(self, cid, provider):
        """Delete circuits

        :param cid: circuit id
        :param provider: Name of the provider
        :return: bool True if succesful otherwase delete exception
        """
        try:
            circuits_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('cid: {} with provider: {}'.format(cid, provider)) from None
        return self.netbox_con.delete('/circuits/circuits/', circuits_id)

    def update_circuit(self, cid, provider, **kwargs):
        """Update circuits

        :param cid: circuit id
        :param provider: provider name
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            circuits_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuits {} with provider {}'.format(cid, provider)) from None
        return self.netbox_con.patch('/circuits/circuits/', circuits_id, **kwargs)

    def get_providers(self, **kwargs):
        """Returns the circuit providers"""
        return self.netbox_con.get('/circuits/providers/', **kwargs)

    def create_provider(self, name, slug):
        """Create a new circuit provider

        :param name: provider name
        :param slug: slug name
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/circuits/providers/', required_fields)

    def delete_provider(self, circuit_provider_name):
        """Delete circuit provider

        :param circuit_provider_name: circuit provider to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            circuits_provider_id = self.get_providers(name=circuit_provider_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit provider: {}'.format(circuit_provider_name)) from None
        return self.netbox_con.delete('/circuits/providers/', circuits_provider_id)

    def update_provider(self, circuit_provider_name, **kwargs):
        """Update circuit provider

        :param circuit_provider_name: circuits role to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            circuits_provider_id = self.get_providers(name=circuit_provider_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit provider: {}'.format(circuit_provider_name)) from None
        return self.netbox_con.patch('/circuits/providers/', circuits_provider_id, **kwargs)

    def get_types(self, **kwargs):
        """Returns the circuit types"""
        return self.netbox_con.get('/circuits/circuit-types/', **kwargs)

    def create_type(self, name, slug):
        """Create a new circuit type

        :param name: type name
        :param slug: slug name
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/circuits/circuit-types/', required_fields)

    def delete_type(self, circuit_type_name):
        """Delete circuit type

        :param circuit_type_name: circuit type to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            circuits_type_id = self.get_types(name=circuit_type_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit type: {}'.format(circuit_type_name)) from None
        return self.netbox_con.delete('/circuits/circuit-types/', circuits_type_id)

    def update_type(self, circuit_type_name, **kwargs):
        """Update circuit role

        :param circuit_type_name: circuits type to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            type_id = self.get_types(name=circuit_type_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit type: {}'.format(circuit_type_name)) from None
        return self.netbox_con.patch('/circuits/circuit-types/', type_id, **kwargs)

    def get_terminations(self, **kwargs):
        """Returns the circuits"""
        return self.netbox_con.get('/circuits/circuit-terminations/', **kwargs)

    def create_termination(self, cid, provider, term_side, site, port_speed, **kwargs):
        """Create a new circuit termination

        :param cid: cid
        :param provider: name of the provider
        :param term_side: term side A or Z
        :param site: Site name
        :param port_speed: port speed value
        :return: netbox object if successful otherwise exception raised
        """
        try:
            site_id = self.dcim.get_sites(name=site)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('site: {}'.format(site)) from None

        try:
            circuit_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('cid: {} with provider {}'.format(cid, provider)) from None

        required_fields = {"circuit": circuit_id, "term_side": term_side, "site": site_id, "port_speed": port_speed}
        return self.netbox_con.post('/circuits/circuit-terminations/', required_fields, **kwargs)

    def delete_termination(self, circuit_type_name):
        """Delete circuit termination

        :param circuit_type_name: circuit type to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            circuits_type_id = self.get_types(name=circuit_type_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuit type: {}'.format(circuit_type_name)) from None
        return self.netbox_con.delete('/circuits/circuit-types/', circuits_type_id)

    def update_termination(self, cid, provider, **kwargs):
        """Update circuit termination

        :param cid: cid
        :param provider: name of the provider
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            circuits_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('circuits {} with provider {}'.format(cid, provider)) from None

        try:
            termination_id = self.get_terminations(circuits_id=circuits_id)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException('termination with cid {} and provider {}'.format(cid, provider)) from None

        return self.netbox_con.patch('/circuits/circuit-terminations/', termination_id, **kwargs)
