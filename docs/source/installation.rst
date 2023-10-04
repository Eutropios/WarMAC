.. _installation:

###################
 Installing WarMAC
###################

.. attention::

   WarMAC only supports Python versions 3.8 to 3.12. There are currently no
   plans to add support to Python 3.7

**********
 From pip
**********

|  Currently, the primary method of installing WarMAC is by installing it
   globally through pip. This can be done using the following command:

.. code:: console

   python -m pip install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code:: console

   warmac --version

|  Once you've installed WarMAC, check out :ref:`using_warmac` for how to use
   WarMAC.

**************
 Using Poetry
**************

.. warning::

   Modifying the dependencies of WarMAC could result in errors. It's recommended
   to keep the dependency versions as is to maintain stability.

|  WarMAC can also be installed using `Poetry <https://python-poetry.org/>`_,
   either through the provided ``poetry.lock`` file (recommended), or by
   building a lock of your own.

**************
 Dependencies
**************

|  WarMAC requires at least urllib3 version 2.0.4 to function without errors.
   This is a hard-requirement and cannot be lowered.
