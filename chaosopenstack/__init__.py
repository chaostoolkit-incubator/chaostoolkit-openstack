# -*- coding: utf-8 -*-

from typing import List

from chaoslib.discovery.discover import (
    discover_actions,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.exceptions import InterruptExecution
from chaoslib.types import Configuration, DiscoveredActivities, Discovery, Secrets
from logzero import logger

from chaosopenstack.client import OpenstackClientWrapper

__version__ = "0.1.0"

__all__ = ["discover", "__version__"]


def openstack_client(configuration: Configuration = None, secrets: Secrets = None):
    """
    Create and return an openstack connection.

    Only Config Files are supported, because the same config can be used across tools and languages.
    cf. https://docs.openstack.org/openstacksdk/latest/user/guides/connect_from_config.html
    """  # noqa 508

    cloud = configuration.get("openstack_cloud")
    regions = configuration.get("openstack_regions")

    if not regions:
        raise InterruptExecution("Openstack requires at least one region to be set!")

    return OpenstackClientWrapper(cloud, regions)


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Openstack capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-openstack")

    discovery = initialize_discovery_result(
        "chaostoolkit-openstack", __version__, "openstack"
    )
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosopenstack.compute.actions"))
    activities.extend(discover_probes("chaosopenstack.compute.probes"))

    return activities
