# Chaos Toolkit Extension for OpenStack.

[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-openstack.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.6+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-openstack
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
  "title": "bastion-stop-start",
  "description": "Stop/Start a bastion instance randomly",
  "tags": [],
  "configuration": {
    "openstack_cloud": "prd",
    "openstack_regions": ["REGION1", "REGION2"]
  },
  "method": [
    {
      "type": "action",
      "name": "terminate-bastion-instance",
      "provider": {
        "type": "python",
        "module": "chaosopenstack.compute.actions",
        "func": "stop_instances",
        "arguments": {
          "rand": true,
          "filters": {
            "name": "prd-bastion-*"
          }
        }
      },
      "pauses": {
        "after": 120
      }
    }
  ],
  "rollbacks": [
    {
      "type": "action",
      "name": "start-bastion-instance",
      "provider": {
        "type": "python",
        "module": "chaosopenstack.compute.actions",
        "func": "start_instances",
        "arguments": {
          "filters": {
            "name": "prd-bastion-*"
          }
        }
      }
    }
  ]
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

This extension uses the [openstacksdk][] library under the hood. This library expects
that you have properly [configured][config] your environment to connect and
authenticate with the Openstack APIs.

[openstacksdk]: https://docs.openstack.org/openstacksdk/latest/index.html
[config]: https://docs.openstack.org/openstacksdk/latest/user/guides/connect_from_config.html

### Use default profile from `~/.config/openstack/clouds.yml` or `/etc/openstack`

This is the most basic case, assuming your `default` profile is properly
configured in `~/.config/openstack/clouds.yml` (or `/etc/openstack`),
then you do not need to pass any specific credentials to the experiment.

### Use profile from a custom path

You can export the `OS_CLIENT_CONFIG_FILE` to target a specific Config File, in this case
also you do not need to pass any specific credentials to the experiment.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
