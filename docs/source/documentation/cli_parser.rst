.. _cli_parser:

############
 CLI Parser
############

|  WarMAC's parser is built with Python's argparse module. The appearance of the
   command-line interface has been substantially modified to appear in a clean
   and organized manner.

.. autoclass:: cli_parser.CustomHelpFormat
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__

.. autofunction:: cli_parser.str_to_int_bounds_check

.. autoclass:: cli_parser.WarMACParser
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__

.. autofunction:: cli_parser.create_parser

.. autofunction:: cli_parser.handle_input
