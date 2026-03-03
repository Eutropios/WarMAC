.. _installation:

###################
 Installing WarMAC
###################

.. attention::

   WarMAC supports Python versions 3.10 to 3.14.


|  The primary method of installing WarMAC is by installing it through `uv
   <https://docs.astral.sh/uv/guides/tools/>`_, though `pipx
   <https://pypa.github.io/pipx/>`_ may be used as well. This keeps WarMAC and
   its dependencies separate from your global Python packages. The option of
   building WarMAC yourself using uv also exists, however this is only
   recommended for development.

*******************
 Using uv (or uvx)
*******************

|  The most basic method of installation is by installing as a uv tool like so:

.. code-block:: console

   $ uv tool install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </cli/index>` for details
   on how to use WarMAC.

************
 Using pipx
************

|  An alternative to installing with uv is pipx:

.. code-block:: console

   $ pipx install warmac

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </cli/index>` for details
   on how to use WarMAC.

***********
 Using pip
***********

|  Using pip alone to install WarMAC will work just as well, though dependencies
   will not be isolated. Installation can be done using the following command:


.. tab:: Unix/macOS

   .. code-block:: console

      $ python -m pip install warmac

.. tab:: Windows

   .. code-block:: console

      $ py -m pip install warmac

|  If you're getting an error that `python` is not recognized as a command, try
   using the following instead:
   ``python3 -m pip install warmac``

|  You can ensure that you've installed WarMAC correctly by calling its help
   page like so:

.. code-block:: console

   $ warmac --version

|  Once you've installed WarMAC, check out :doc:`Usage </cli/index>` for details
   on how to use WarMAC.
