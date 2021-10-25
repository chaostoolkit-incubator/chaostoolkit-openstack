from unittest.mock import MagicMock, patch

from chaosopenstack.compute.actions import start_instances, stop_instances


@patch("chaosopenstack.compute.actions.openstack_client", autospec=True)
def test_stop_instances(openstack_client):
    client = MagicMock()

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

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    stop_instances({"name": "staging-bastion-*"})

    client.compute.stop_server.assert_called_once_with(instances[1])


@patch("chaosopenstack.compute.actions.openstack_client", autospec=True)
def test_stop_instances_randomly(openstack_client):
    client = MagicMock()

    instances = [
        {
            "status": "ACTIVE",
            "vm_state": "active",
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

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    with patch("chaosopenstack.compute.actions.random.choice") as choice:
        choice.return_value = instances[1]
        stop_instances(filters={"name": "staging-bastion-*"}, rand=True)
        choice.assert_called_once_with(instances)

    client.compute.stop_server.assert_called_once_with(instances[1])


@patch("chaosopenstack.compute.actions.openstack_client", autospec=True)
def test_start_instances(openstack_client):
    client = MagicMock()

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

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    start_instances({"name": "staging-bastion-*"})

    client.compute.start_server.assert_called_once_with(instances[0])
