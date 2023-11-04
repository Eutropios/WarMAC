.. _installation:

###################
 Installing WarMAC
###################

.. attention::

   WarMAC only supports Python versions 3.8 to 3.12. There are currently no
   plans to add support to Python 3.7

|  WarMAC's only dependency is urllib3 ≥2.0.4,<3.0.0

***********
 Using pip
***********

|  Currently, the primary method of installing WarMAC is by installing it
   through pip. This can be done using the following command:

.. tab:: Unix/macOS

   .. code:: console

      python -m pip install warmac

.. tab:: Windows

   .. code:: console

      py -m pip install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code:: console

   warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </cli/index>` for how to
   use WarMAC.

**************
 Using Poetry
**************

.. warning::

   Modifying the dependencies of WarMAC could result in errors. It's recommended
   to keep the dependency versions as is to maintain stability.

|  WarMAC can also be installed using `Poetry <https://python-poetry.org/>`_
   either through the provided ``poetry.lock`` file (recommended), or by
   building a lock of your own.

|  To obtain the source code, you can either download the latest version from
   `Releases <https://github.com/Eutropios/WarMAC/releases>`_, or by cloning the
   repository using `git <https://git-scm.com/downloads>`_ with the following
   command:

.. code:: console

   git clone https://github.com/Eutropios/WarMAC.git ./some/directory

|  WarMAC can then be built by navigating to the directory you cloned WarMAC
   into, and running the ``poetry build`` and ``poetry install`` commands.
