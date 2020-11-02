# VirtualMODI
<div align="center">

[![Python Versions](https://img.shields.io/pypi/pyversions/virtual-modi.svg?style=flat-square)](https://pypi.python.org/pypi/virtual-modi)
[![Release (PyPI)](https://img.shields.io/pypi/v/virtual-modi?color=blue&label=release&style=flat-square)](https://pypi.python.org/pypi/virtual-modi)
[![Build Workflow Status (Github Actions)](https://img.shields.io/github/workflow/status/LUXROBO/virtual-modi/Build%20Status/main?style=flat-square)](https://github.com/LUXROBO/virtual-modi/actions)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/LUXROBO/virtual-modi/main?style=flat-square)](https://www.codefactor.io/repository/github/luxrobo/virtual-modi/overview/main)
[![GitHub LICENSE](https://img.shields.io/github/license/LUXROBO/virtual-modi?style=flat-square&color=blue)](https://github.com/LUXROBO/virtual-modi/blob/main/LICENSE)
[![Lines of Code](https://img.shields.io/tokei/lines/github/LUXROBO/virtual-modi?style=flat-square)](https://github.com/LUXROBO/virtual-modi/tree/main/virtual_modi)

</div>

## Description
> Implementation of virtual MODI modules, written in Python.

## Features
> VirtualMODI mimics the operation of MODI HW modules.
* Performs message generation and destruction for MODI1 and 2 modules
* Provides MPI through various connections including serial and TCP

## How to Install
> When installing VirtualMODI package, we highly recommend you to use Anaconda to manage the distribution.
> With Anaconda, you can use an isolated virtual environment, solely for VirtualMODI.

[Optional] Once you install [Anaconda](https://docs.anaconda.com/anaconda/install/), then:
```commandline
# Install new python environment for VirtualMODI package, choose python version >= 3.6
conda create --name virtual-modi python=3.6

# After you properly install the python environment, activate it
conda activate virtual-modi

# Make sure that your python version is compatible with VirtualMODI
python --version
```

Install the latest version of VirtualMODI:
```commandline
python -m pip install virtual-modi --user
```

## How to Use
Import virtual-modi package and create VirtualBundle object.
```python
from virtual_modi import VirtualBundle
vb = VirtualBundle()
```

When creating the bundle object, you can optionally pass configuration parameters.
```python
vb = VirtualBundle(conn_type='ser', modi_version=1)
```
