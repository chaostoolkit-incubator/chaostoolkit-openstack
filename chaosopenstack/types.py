# -*- coding: utf-8 -*-

from typing import Any, Dict

__all__ = ["OpenstackResponse"]

# really dependent on the type of resource called
OpenstackResponse = Dict[str, Any]
