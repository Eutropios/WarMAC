.. program:: warmac

##############
 Using WarMAC
##############

|  WarMAC has a variety of commands for users to select from. Each command has
   its own unique options and arguments. Wherever possible, options that
   perform similar functions for different commands will share the same name.

.. note::

   WarMAC currently only has the Average command. More commands will be added
   in the future.

****************
 Running WarMAC
****************

|  Every WarMAC command is preceded by ``warmac``. The general help section of
   the program can be viewed by running :option:`warmac --help`.

|  The general help section describes each command's function, as well as
   describing the available flags and options.

.. code-block:: console

   $ warmac <command> [options]

*********
 Options
*********

|  When determining whether to display the program's help or to display the
   current program's version, WarMAC will use whichever of the two options is given first.

.. option:: -h, --help

   Prints the command line usage and exits. WarMAC will ignore all other
   options if ``-h`` or ``--help`` is given. To remove color from the help
   text, please set the environment variable NO_COLOR to 1 like so:
   ``export NO_COLOR=1``

.. option:: -V, --version

   Prints the current version of WarMAC and exits. WarMAC will ignore all other
   options if ``-V`` or ``--version`` is given.

*************
 Subcommands
*************

|  The following is a list of commands that WarMAC can run:

.. option:: average

   Calculates the average platinum price of an item. It can find the median,
   mean, mode, geometric mean, or harmonic mean of the specified item. It's
   also able to target specific platforms, use buyer listings instead of
   seller listings, and filter out older orders.
