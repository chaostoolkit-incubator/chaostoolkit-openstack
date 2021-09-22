from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets

from chaosopenstack import openstack_client
from chaosopenstack.types import OpenstackResponse

__all__ = ["describe_instances", "count_instances", "instances_state"]


def describe_instances(
    filters: List[Dict[str, Any]],
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[OpenstackResponse]:
    """
    Describe instances following the specified filters.
    """
    client = openstack_client(configuration, secrets)
    instances = client.compute.servers(**filters)

    return [instance.to_dict() for instance in instances]


def count_instances(
    filters: List[Dict[str, Any]],
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> int:
    """
    Return count of instances matching the specified filters.
    """
    client = openstack_client(configuration, secrets)
    instances = client.compute.servers(details=False, **filters)

    return sum(1 for x in instances)


def instances_state(
    state: str,
    filters: List[Dict[str, Any]] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """Determines if compute instances match desired state"""
    client = openstack_client(configuration, secrets)
    instances = client.compute.servers(details=False, **filters)
    for instance in instances:
        if instance.vm_state != state:
            return False

    return True
