.. _warmac_usage:

.. program:: warmac

##############
 Using WarMAC
##############

|  WarMAC has a variety of subcommands for users to select from. Each subcommand
   has its own unique options and arguments. Wherever possible, options that
   perform similar functions for different subcommands will share the same name.

.. note::

   WarMAC currently only has the Average subcommand. More subcommands will be
   added in the future.

****************
 Running WarMAC
****************

|  Every WarMAC subcommand is preceded by ``warmac``. The general help section
   of the program can be viewed by running :option:`warmac --help`.

|  The general help section describes each subcommand's function, as well as
   describing the available flags and options.

.. code:: console

   $ warmac <command> [options]

*********
 Options
*********

|  When determining whether to display the program's help or to display the
   current program's version, WarMAC will use whichever of the two options is given first.

.. option:: -h, --help

   Print the command line usage and then exit. Providing this option is
   identical to calling ``warmac`` without any subcommand. WarMAC will ignore
   all other options if ``-h`` or ``--help`` is given.


.. option:: -V, --version

   Print the current version of WarMAC and exit. WarMAC will ignore all other
   options if ``-V`` or ``--version`` is given.
