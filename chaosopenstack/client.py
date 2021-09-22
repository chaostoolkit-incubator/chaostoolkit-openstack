from collections import OrderedDict

import openstack


class OpenstackComputeWrapper:
    """
    OpenstackComputeWrapper provides some of the compute API methods over
    multiple Openstack regions.

    https://docs.openstack.org/openstacksdk/latest/user/guides/compute.html
    """

    def __init__(self, conns):
        self._conns = conns

    def servers(self, **filters):
        instances = []
        for region in self._conns.keys():
            instances.extend(list(self._conns[region].compute.servers(**filters)))

        return [instance.to_dict() for instance in instances]

    def stop_server(self, instance):
        self._conns[instance["location"]["region_name"]].compute.stop_server(instance)

    def start_server(self, instance):
        self._conns[instance["location"]["region_name"]].compute.start_server(instance)


class OpenstackClientWrapper:
    """
    OpenstackClientWrapper provides a single interface to manage openstack APIs
    over multiple regions.

    https://docs.openstack.org/openstacksdk/latest/user/guides/connect.html
    """

    def __init__(self, cloud, regions):

        # TODO activate this when --verbose flag is set
        # openstack.enable_logging(debug=True)

        self._conns = OrderedDict()

        for region in regions:
            self._conns[region] = openstack.connect(cloud=cloud, region_name=region)

        self.compute = OpenstackComputeWrapper(self._conns)
