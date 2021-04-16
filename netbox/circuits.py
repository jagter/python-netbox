import netbox.exceptions as exceptions
from netbox.dcim import Dcim


class Circuits(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con
        self.dcim = Dcim(self.netbox_con)

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
            raise exceptions.NotFoundException({"detail": "cirtcuit provider: {}".format(circuit_provider)}) from None

        try:
            type_id = self.get_types(name=circuit_type)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "circuit type: {}".format(circuit_type)}) from None

        required_fields = {"provider": provider_id, "circuit": cid, "type": type_id,
                           "status": status_id}
        return self.netbox_con.post('/circuits/circuits/', required_fields, **kwargs)

    def delete_circuit(self, cid, provider):
        """Delete circuits

        :param cid: circuit
        :param provider: Name of the provider
        :return: bool True if successful otherwise delete exception
        """
        try:
            circuits_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "Circuit with circuit: {} and provider: {}".format(cid, provider)}) from None
        return self.netbox_con.delete('/circuits/circuits/', circuits_id)

    def update_circuit(self, cid, provider, **kwargs):
        """Update circuit

        :param cid: circuit
        :param provider: provider name
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            circuits_id = self.get_circuits(cid=cid, provider=provider)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "Circuit with circuit: {} and provider {}".format(cid, provider)}) from None
        return self.netbox_con.patch('/circuits/circuits/', circuits_id, **kwargs)

    def get_providers(self, **kwargs):
        """Returns circuit providers"""
        return self.netbox_con.get('/circuits/providers/', **kwargs)

    def create_provider(self, name, slug):
        """Create a new circuit provider

        :param name: provider name
        :param slug: slug name
        :return: netbox object if successful otherwise exception raised
        """
        required_fields = {"name": name, "slug": slug}
        return self.netbox_con.post('/circuits/providers/', required_fields)

    def delete_provider(self, provider_name):
        """Delete circuit provider

        :param provider_name: circuit provider to delete
        :return: bool True if successful otherwise delete exception
        """
        try:
            circuits_provider_id = self.get_providers(name=provider_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "circuit provider: {}".format(provider_name)}) from None
        return self.netbox_con.delete('/circuits/providers/', circuits_provider_id)

    def update_provider(self, provider_name, **kwargs):
        """Update circuit provider

        :param provider_name: circuits role to update
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            circuits_provider_id = self.get_providers(name=provider_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "circuit provider: {}".format(provider_name)}) from None
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

    def delete_type(self, type_name):
        """Delete circuit type

        :param type_name: circuit type to delete
        :return: bool True if succesful otherwase delete exception
        """
        try:
            circuits_type_id = self.get_types(name=type_name)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "circuit type: {}".format(type_name)}) from None
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
            raise exceptions.NotFoundException({"detail": "circuit type: {}".format(circuit_type_name)}) from None
        return self.netbox_con.patch('/circuits/circuit-types/', type_id, **kwargs)

    def get_terminations(self, **kwargs):
        """Returns the circuits"""
        return self.netbox_con.get('/circuits/circuit-terminations/', **kwargs)

    def create_termination(self, circuit, term_side, site, port_speed, **kwargs):
        """Create a new circuit termination

        :param circuit: circuit id
        :param term_side: term side A or Z
        :param site: Site name
        :param port_speed: port speed value
        :return: netbox object if successful otherwise exception raised
        """
        try:
            site_id = self.dcim.get_sites(name=site)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "site: {}".format(site)}) from None

        required_fields = {"circuit": circuit, "term_side": term_side, "site": site_id, "port_speed": port_speed}
        return self.netbox_con.post('/circuits/circuit-terminations/', required_fields, **kwargs)

    def delete_termination(self, circuit, term_side, site, port_speed):
        """Delete circuit termination

        :param circuit: circuit id
        :param term_side: term side A or Z
        :param site: Site name
        :param port_speed: port speed value
        :return: bool True if successful otherwise delete exception
        """
        try:
            site_id = self.dcim.get_sites(name=site)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "site: {}".format(site)}) from None

        try:
            circuit_termination = self.get_terminations(circuit_id=circuit, term_side=term_side, site_id=site_id,
                                                        port_speed=port_speed)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "circuit termination with given arguments"}) from None

        return self.netbox_con.delete('/circuits/circuit-terminations/', circuit_termination)

    def update_termination(self, circuit, term_side, site, port_speed, **kwargs):
        """Update circuit termination

        :param circuit: circuit id
        :param term_side: Termination side
        :param site: Dcim Site
        :param port_speed: Port speed (Kbps). maximum: 2147483647
        :param kwargs: requests body dict
        :return: bool True if successful otherwise raise UpdateException
        """
        try:
            site_id = self.dcim.get_sites(name=site)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail": "site: {}".format(site)}) from None

        try:
            circuit_termination_id = self.get_terminations(circuit_id=circuit, term_side=term_side, site_id=site_id,
                                                           port_speed=port_speed)[0]['id']
        except IndexError:
            raise exceptions.NotFoundException({"detail" "circuit termination with given arguments"}) from None

        return self.netbox_con.patch('/circuits/circuit-terminations/', circuit_termination_id, **kwargs)
