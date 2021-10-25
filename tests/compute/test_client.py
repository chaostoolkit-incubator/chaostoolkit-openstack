from unittest.mock import MagicMock, call, patch

from chaosopenstack.client import OpenstackClientWrapper, OpenstackComputeWrapper


@patch("chaosopenstack.client.openstack", autospec=True)
def test_OpenstackClientWrapper_connect(openstack: object):
    OpenstackClientWrapper("myproject", ["REGION1", "REGION2"])

    openstack.connect.assert_has_calls(
        [
            call(cloud="myproject", region_name="REGION1"),
            call(cloud="myproject", region_name="REGION2"),
        ]
    )


@patch("chaosopenstack.client.openstack", autospec=True)
def test_OpenstackComputeWrapper_servers(openstack: object):
    instances = [
        {
            "status": "SHUTOFF",
            "vm_state": "stopped",
            "id": "0b7a8371-24cf-4855-b3d2-e30f2cb13ddc",
            "name": "staging-bastion-region1-01",
            "location": {"cloud": "staging", "region_name": "REGION1"},
        },
        {
            "status": "ACTIVE",
            "vm_state": "active",
            "id": "93746749-331d-4ec4-b536-4ce73889e78f",
            "name": "staging-bastion-region2-02",
            "location": {
                "cloud": "staging",
                "region_name": "REGION2",
            },
        },
    ]

    instance1 = MagicMock()
    instance1.to_dict.return_value = instances[0]

    instance2 = MagicMock()
    instance2.to_dict.return_value = instances[1]

    client_region1 = MagicMock()
    client_region1.compute.servers.return_value = [instance1]
    client_region2 = MagicMock()
    client_region2.compute.servers.return_value = [instance2]
    conns = {"REGION1": client_region1, "REGION2": client_region2}

    compute = OpenstackComputeWrapper(conns)
    response = compute.servers()

    assert instances == response


@patch("chaosopenstack.client.openstack", autospec=True)
def test_OpenstackComputeWrapper_stop_server(openstack: object):
    instance = {
        "status": "ACTIVE",
        "vm_state": "active",
        "id": "0b7a8371-24cf-4855-b3d2-e30f2cb13ddc",
        "name": "staging-bastion-region1-01",
        "location": {"cloud": "staging", "region_name": "REGION1"},
    }

    client_region1 = MagicMock()
    client_region2 = MagicMock()
    conns = {"REGION1": client_region1, "REGION2": client_region2}

    compute = OpenstackComputeWrapper(conns)
    compute.stop_server(instance)

    client_region1.compute.stop_server.assert_called_once_with(instance)
    assert client_region2.compute.stop_server.call_count == 0


@patch("chaosopenstack.client.openstack", autospec=True)
def test_OpenstackComputeWrapper_start_server(openstack: object):
    instance = {
        "status": "SHUTOFF",
        "vm_state": "stopped",
        "id": "93746749-331d-4ec4-b536-4ce73889e78f",
        "name": "staging-bastion-region2-02",
        "location": {"cloud": "staging", "region_name": "REGION2"},
    }

    client_region1 = MagicMock()
    client_region1.compute.servers.return_value = instance

    client_region1 = MagicMock()
    client_region2 = MagicMock()
    conns = {"REGION1": client_region1, "REGION2": client_region2}

    compute = OpenstackComputeWrapper(conns)
    compute.start_server(instance)

    assert client_region1.compute.start_server.call_count == 0
    client_region2.compute.start_server.assert_called_once_with(instance)
