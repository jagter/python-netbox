import netbox.connection as connection
import netbox.dcim as dcim
import netbox.ipam as ipam


class NetBox(object):
    def __init__(self, host, **kwargs):
        self.connection = connection.NetboxConnection(host=host, **kwargs)
        self.ipam = ipam.Ipam(self.connection)
        self.dcim = dcim.Dcim(self.connection)
