.. _installation:

###################
 Installing WarMAC
###################

.. attention::

   WarMAC only supports Python versions 3.8 to 3.12. There are currently no
   plans to add support to Python 3.7

|  WarMAC's only dependency is urllib3 ≥2.0.4,<3.0.0

|  WarMAC can be installed in a variety of ways, all of which can be found on
   this page. It is recommended that you install WarMAC using `pipx
   <https://pypa.github.io/pipx/>`_, which keeps WarMAC and its dependencies
   separate from your global Python version. However, using pip alone will work
   just as well. The option of building WarMAC yourself using Poetry also
   exists, however it is recommended for this to not be done.

************
 Using pipx
************

|  Installing WarMAC using pipx can be done by running the following command in
   the terminal:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pipx install warmac

.. tab:: Windows

   .. code-block:: console

      $ py -m pipx install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </usage/index>` for details
   on how to use WarMAC.

***********
 Using pip
***********

|  Installing WarMAC using pip can be done by running the following command in
   the terminal:

.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install warmac

.. tab:: Windows

   .. code-block:: console

      $ py -m pip install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </usage/index>` for details
   on how to use WarMAC.

**************
 Using Poetry
**************

.. warning::

   Modifying the dependency pins of WarMAC could result in errors. It's
   recommended to keep the dependency pins as is to maintain stability.

|  WarMAC can also be installed using `Poetry <https://python-poetry.org/>`_
   either through the provided ``poetry.lock`` file (recommended) or by building
   a lock of your own.

|  To obtain the source code, you can either download the latest version from
   `Releases <https://github.com/Eutropios/WarMAC/releases>`_, or by cloning the
   repository using `git <https://git-scm.com/downloads>`_ with the following
   command:

.. code-block:: console

   $ git clone https://github.com/Eutropios/WarMAC.git ./some/directory

|  WarMAC can then be built by navigating to the directory you cloned WarMAC
   into, and running the ``poetry build`` and ``poetry install`` commands.

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </usage/index>` for details
   on how to use WarMAC.
