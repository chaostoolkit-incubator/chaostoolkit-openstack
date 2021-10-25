from unittest.mock import MagicMock, patch

from chaosopenstack.compute.probes import (
    count_instances,
    describe_instances,
    instances_state,
)


@patch("chaosopenstack.compute.probes.openstack_client", autospec=True)
def test_describe_instances(openstack_client):
    client, instance1, instance2 = MagicMock(), MagicMock(), MagicMock()
    instances = [instance1, instance2]

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    describe_instances({"name": "*"})

    instance1.to_dict.assert_called_once()
    instance2.to_dict.assert_called_once()


@patch("chaosopenstack.compute.probes.openstack_client", autospec=True)
def test_count_instances(openstack_client):
    client, instance1, instance2 = MagicMock(), MagicMock(), MagicMock()
    instances = [instance1, instance2]

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    count = count_instances({"name": "*"})

    assert count == 2


@patch("chaosopenstack.compute.probes.openstack_client", autospec=True)
def test_instances_state_true(openstack_client):
    client = MagicMock()

    instances = [
        MagicMock(
            status="ACTIVE",
            vm_state="active",
            id="0b7a8371-24cf-4855-b3d2-e30f2cb13ddc",
            name="staging-bastion-region1-01",
            location=MagicMock(
                cloud="staging",
                region_name="REGION1",
            ),
        ),
        MagicMock(
            status="ACTIVE",
            vm_state="active",
            id="93746749-331d-4ec4-b536-4ce73889e78f",
            name="staging-bastion-region2-02",
            location=MagicMock(
                cloud="staging",
                region_name="REGION2",
            ),
        ),
    ]

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    response = instances_state("active", {"name": "staging-bastion-*"})

    assert response is True


@patch("chaosopenstack.compute.probes.openstack_client", autospec=True)
def test_instances_state_false(openstack_client):
    client = MagicMock()

    instances = [
        MagicMock(
            status="ACTIVE",
            vm_state="active",
            id="0b7a8371-24cf-4855-b3d2-e30f2cb13ddc",
            name="staging-bastion-region1-01",
            location=MagicMock(
                cloud="staging",
                region_name="REGION1",
            ),
        ),
        MagicMock(
            status="SHUTOFF",
            vm_state="stopped",
            id="93746749-331d-4ec4-b536-4ce73889e78f",
            name="staging-bastion-region2-02",
            location=MagicMock(
                cloud="staging",
                region_name="REGION2",
            ),
        ),
    ]

    client.compute.servers.return_value = instances
    openstack_client.return_value = client

    response = instances_state("ACTIVE", {"name": "staging-bastion-*"})

    assert response is False
