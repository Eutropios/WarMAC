.. _warmac_parser:

###############
 WarMAC Parser
###############

|  WarMAC's parser is built with Python's argparse module. The appearance of the
   command-line interface has been substantially modified to appear in a clean
   and organized manner.

.. note::

   Only global variables and constants that are public are documented. Please
   see the source code for private variable/constant documentation.

.. py:data:: warmac_parser.DEFAULT_TIME
   :type: int
   :value: 10

   The default time that will be used for calculating listing ages.

.. autoclass:: warmac_parser.CustomHelpFormat
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__

.. autoclass:: warmac_parser.WarMACParser
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__

.. autofunction:: warmac_parser._int_checking

.. autofunction:: warmac_parser._create_parser

.. autofunction:: warmac_parser.handle_input
