.. _warmac_main:

#############
 WarMAC Main
#############

|  The ``__init__.py`` file is the file that is called when WarMAC is executed.
   It pulls together all of the necessary modules and functions and executes
   them.

.. py:data:: warmac.SUBCMD_TO_FUNC
   :type: dict[str, ~collections.abc.Callable[[~argparse.Namespace], None]]
   :value: average.average()

   A dictionary of all commands that can be executed by the user.

.. autofunction:: main.process_cli_command

.. autofunction:: main.main
