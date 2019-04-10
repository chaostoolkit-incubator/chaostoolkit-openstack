# -*- coding: utf-8 -*-
from chaoslib.discovery.discover import (discover_actions, discover_probes,
                                         initialize_discovery_result)
from chaoslib.exceptions import DiscoveryFailed
from chaoslib.types import (Configuration, DiscoveredActivities,
                            DiscoveredSystemInfo, Discovery, Secrets)
from logzero import logger
import json
import os
import os.path
from typing import List


# openstack
from novaclient import client
from keystoneauth1 import loading, session

__version__ = '0.1.0'
__all__ = ["__version__", "openstack_novaclient", "discover"]


def keystone_session(configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Create a session in keystone
    """
    configuration = configuration or {}
    AUTH_URL = configuration.get("KEYSTONE_AUTH_URL")
    USERNAME = configuration.get("KEYSTONE_USERNAME")
    PASSWORD = configuration.get("KEYSTONE_PASSWORD")
    PROJECT_ID = configuration.get("OPENSTACK_PROJECT_ID")
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=AUTH_URL,
                                    username=USERNAME,
                                    password=PASSWORD,
                                    project_id=PROJECT_ID)

    return session.Session(auth=auth)


def openstack_novaclient(resource_name=str,
                         configuration: Configuration = None,
                         secrets: Secrets = None):
    """
    Create a Nova Client
    """
    configuration = configuration or {}
    VERSION = configuration.get("NOVA_VERSION", configuration)
    sess = keystone_session(configuration)

    return client.Client(VERSION, session=sess)


def discover(discover_system: bool = True) -> Discovery:
    """
    extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-openstack")

    discovery = initialize_discovery_result(
        "chaostoolkit-openstack", __version__, "openstack")
    discovery["activities"].extend(load_exported_activities())
    return discovery


###############################################################################
# Private functions
###############################################################################

def load_exported_activities() -> List[DiscoveredActivities]:
    """
     extension.
    """
    activities = []
    activities.extend(discover_actions("chaosopenstack.nova.actions"))
    activities.extend(discover_probes("chaosopenstack.nova.probes"))

    return activities
