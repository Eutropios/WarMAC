..
   WarMAC documentation master file, created by
   sphinx-quickstart on Tue Aug 22 17:40:25 2023.

########
 WarMAC
########

.. container:: badges

   |pypiver| |pythonver| |license|

|  Warframe Market Average Calculator, or WarMAC (/'wɔr'mæk/) for short, is a
   command-line Python script that can calculate the average market price of any
   tradeable item in Warframe. It does this by retrieving orders of a specific
   item from the fan website `Warframe Market <https://warframe.market/>`_, and
   then calculates then average buy or sell price of that item.

|  WarMAC currently supports all Python versions 3.8 to 3.12 inclusive.

.. important::

   This project is under active development.

*****************
 Getting Started
*****************

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: User Guide

   installation
   usage/index

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Development

   reference/warmac_main
   reference/warmac_average
   reference/cli_parser
   reference/warmac_errors

.. toctree::
   :hidden:
   :titlesonly:
   :caption: Project Links

   GitHub <https://github.com/Eutropios/WarMAC>
   PyPI <https://pypi.org/project/WarMAC/>

|  Ready to install WarMAC?
|  :doc:`Installation Guide </installation>`

|  Need help using WarMAC?
|  :doc:`Using WarMAC <usage/index>`

Indices and tables
==================

-  :ref:`genindex`
-  :ref:`search`

Acknowledgements
================

|  In addition to the tools listed in `.pre-commit-config.yaml
   <https://github.com/Eutropios/WarMAC/blob/main/.pre-commit-config.yaml>`_ and
   `pyproject.toml
   <https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml>`_, this
   project uses the following tools in its development:

-  `autoDocstring <https://github.com/NilsJPWerner/autoDocstring>`_
-  `Taplo <https://github.com/tamasfe/taplo>`_
-  `markdownlint <https://github.com/DavidAnson/vscode-markdownlint>`_
-  `vermin <https://github.com/netromdk/vermin>`_

|  WarMAC is packaged using `Poetry <https://github.com/python-poetry/poetry>`_.

Licensing
=========

|  **This project is NOT affiliated with Warframe, Digital Extremes, or Warframe
   Market.**

|  Copyright (c) 2023 Noah Jenner under MIT License

|  For additional licensing information, please see `LICENSE.txt
   <https://github.com/Eutropios/WarMAC/blob/main/LICENSE.txt>`_
|  For licensing regarding urllib3, please see `LICENSE-urllib3.txt
   <https://github.com/Eutropios/WarMAC/blob/main/LICENSE-urllib3.txt>`_

Authors
=======

|  WarMAC is authored by `Eutropios <https://www.github.com/Eutropios>`_.

.. |pypiver| image:: https://img.shields.io/pypi/v/warmac
   :alt: PyPI - Package Version
   :target: https://pypi.org/project/warmac/

.. |pythonver| image:: https://img.shields.io/pypi/pyversions/warmac
   :alt: PyPI - Python Version
   :target: https://pypi.org/project/warmac/

.. |license| image:: https://img.shields.io/github/license/Eutropios/WarMAC
   :alt: MIT License
   :target: https://github.com/Eutropios/WarMAC
