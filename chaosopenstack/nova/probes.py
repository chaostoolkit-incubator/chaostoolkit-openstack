# -*- coding: utf-8 -*-
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from typing import Any, Dict, List
from chaosopenstack import openstack_novaclient
from logzero import logger
from typing import Any, Dict, List, Union
from novaclient import client


__all__ = ["check_status_instances"]


def demo(instance_names: List[str] = None,
         filters: List[str] = None,
         secrets: Secrets = None,
         force: bool = False,
         status: str = None,
         configuration: Configuration = None):
    return True


def check_status_instances(instance_names: List[str] = None,
                           filters: List[str] = None,
                           secrets: Secrets = None,
                           force: bool = False,
                           status: str = None,
                           configuration: Configuration = None):
    """
    demo
    """
    if status is None:
        raise FailedActivity(
            "You need to tell us what status: Active or Shutoff")

    list_found = []
    list_not_found = []
    nova_client = openstack_novaclient("nova-client", configuration, secrets)

    for instance in instance_names:
        server = nova_client.servers.list(
            search_opts={'status': status, 'name': instance})
        if server:
            list_found.append(instance)
        else:
            list_not_found.append(instance)

    if status == 'Active':
        if len(list_found) == len(instance_names):
            return True
        else:
            return False

    if status == 'Shutoff':
        if len(list_not_found) == len(instance_names):
            return True
        else:
            return False
