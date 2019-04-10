
# -*- coding: utf-8 -*-
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from chaosopenstack import openstack_novaclient
from logzero import logger
from typing import Any, Dict, List, Union
from novaclient import client
import random


__all__ = ["start_instances", "stop_instances"]


def stop_instances(instance_names: List[str] = None,
                   force: bool = False, configuration: Configuration = None):
    """
    Stop multiples instance on Openstack

    You may provide list of instance name or a list with simples regex like:
                my_instance*

    On filters yo can specify list os names that we try to find for stop
    instance(s)
    """
    if not instance_names:
        raise FailedActivity(
            "To stop an Openstack instance, you must specify either the"
            " list of instance name, or a set of filters.")

    nova_client = openstack_novaclient("nova-client", configuration)
    _stop_nova_instances(nova_client, instance_names)

    return "Done"


def start_instances(instance_names: List[str] = None,
                    configuration: Configuration = None):
    """
    Start instances on openstack

    You may provide list of instance name.
    """

    if not instance_names:
        raise FailedActivity(
            "To start an Openstack instance, you must specify either"
            "the instance name, an AV(Availability Zone) to pick a "
            "random instance from, or a set of filters."
        )

    nova_client = openstack_novaclient("nova-client", configuration)

    _start_nova_instances(nova_client, instance_names)

    return "Done"


###############################################################################
# Private functions
###############################################################################


def _stop_nova_instances(nova: client.Client, list_instances: List[str]):

    instances_stopped = []
    servers = _find_nova_object_instances(nova, list_instances)
    if servers:
        for server in servers:
            status = nova.servers.stop(server)
            if status:
                instances_stopped.append(server)
                logger.info(
                    "This is instance is %s stopped." % server
                )
            else:
                logger.info(
                    "This is instance is %s not stopped." % server
                )
        result = str(instances_stopped).strip('[]')
        return "This is the list of stopped instances : %s " % result
    else:
        raise FailedActivity("Not find any instances that you provider")


def _start_nova_instances(nova: client.Client, list_instances: List[str]):
    servers = _find_nova_object_instances(nova, list_instances)
    if servers:
        for server in servers:
            status = nova.servers.start(server)
            if status is not None:
                logger.info(
                    "This instance %s is started." % server
                )
            else:
                logger.info(
                    "This instance %s is not started." % server
                )
    else:
        raise FailedActivity("Not find any instances that you provider")


def _find_nova_object_instances(nova: client.Client,
                                nova_filter: List[str]):
    """
    Function to find instances by name and return a list of server object
    """
    instances_nova = []
    for f in nova_filter:
        for x in nova.servers.list(search_opts={'name': f}):
            instances_nova.append(x)

    return instances_nova
