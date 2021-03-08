# Nvidia CUDA Layer

Installs the configured CUDA version with Nvidia drivers when supported GPU
hardware is detected.


# States

The following states are set by this layer:

* `cuda.supported`

  This state is set when supported GPU hardware is detected.

* `cuda.installed`

  This state is set once CUDA-related packages are installed and configured.


# Usage

To use this layer, include it in the `layer.yaml` of a charm:

    includes:
      - 'layer:nvidia-cuda'

Build and deploy the charm to a machine with Nvidia GPUs, e.g.
`instance-type=p2.xlarge` on AWS or `instance-type=Standard_NC6` on Azure.


# Configuration

The following runtime configuration options are available in this layer:

* `cuda-version`

  The `cuda-repo` package version to install. Defaults to `9.1.85-1`.

      juju config <charm> cuda-version=9.1.85-1

  >**Note**: This layer constructs a `major-minor` string from this value and
  installs the corresponding `cuda-x-y` meta package (`cuda-9-1` by default).
  This package will install the latest available dependencies in this series.

* `install-cuda`

  When `True` (the default), install and configure CUDA if capable hardware is
  present. Set this to `False` to prevent installation regardless of hardware
  support.

      juju config <charm> install-cuda=True


# Caveats

## Disk Space

The packages installed by this layer require approximately 4GB of disk space.
Specify a `root-disk` constraint if needed to ensure the machine has
adequate disk space for installation.  For example:

    juju deploy <charm> --constraints "instance-type=p2.xlarge root-disk=16G"

## Removing CUDA

When the `install-cuda` configuration option is set to `True`, required
packages will be installed and the system will be configured to include
CUDA paths. If `install-cuda` is subsequently set to `False`, the system
configuration files created by this layer will be removed; however, the
packages installed by this layer will remain on the system.

## Restricted Networks

This layer installs packages from http://developer.download.nvidia.com/.
Configure proxies for Juju models in restricted network environments as needed.
See [Configuring Models][] for information about available proxy options.

[Configuring Models]: https://jujucharms.com/docs/stable/models-config
