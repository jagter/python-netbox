class Status(object):

    def __init__(self, netbox_con):
        self.netbox_con = netbox_con

    def get_status(self):
        """Returns the Netbox status"""
        return self.netbox_con.get('/status/')
