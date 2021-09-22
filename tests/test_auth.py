from unittest.mock import patch

import pytest
from chaoslib.exceptions import InterruptExecution

from chaosopenstack import openstack_client

SECRETS = {}

CONFIGURATION = {
    "openstack_cloud": "myproject",
    "openstack_regions": ["REGION1", "REGION2"],
}


@patch("chaosopenstack.OpenstackClientWrapper", autospec=True)
def test_create_client(OpenstackClientWrapper: object):
    openstack_client(configuration=CONFIGURATION, secrets=SECRETS)
    OpenstackClientWrapper.assert_called_with("myproject", ["REGION1", "REGION2"])


@patch("chaosopenstack.OpenstackClientWrapper", autospec=True)
def test_create_client_without_regions(OpenstackClientWrapper: object):
    with pytest.raises(InterruptExecution):
        openstack_client(
            configuration={"openstack_cloud": "myproject"}, secrets=SECRETS
        )
