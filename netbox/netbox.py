import netbox.connection as connection
import netbox.dcim as dcim
import netbox.ipam as ipam
import netbox.virtualization as virtualization
import netbox.exceptions as exceptions
import netbox.tenancy as tenancy
import netbox.extras as extras


class NetBox(object):
    def __init__(self, host, **kwargs):
        self.connection = connection.NetboxConnection(host=host, **kwargs)
        self.ipam = ipam.Ipam(self.connection)
        self.dcim = dcim.Dcim(self.connection)
        self.virtualization = virtualization.Virtualization(self.connection)
        self.tenancy = tenancy.Tenancy(self.connection)
        self.extras = extras.Extras(self.connection)
        self.exceptions = exceptions
