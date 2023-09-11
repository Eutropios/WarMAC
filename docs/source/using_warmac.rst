.. _using_warmac:

Using WarMAC
============

| The command-line usage for warmac is as follows:

CHANGE THIS TO HAVE HEADERS FOR EACH PARAMETER AND EXPLAIN MORE THOROUGHLY.
.. code-block:: none

   usage: warmac <command> [options]

   A program to fetch the average market cost of an item in Warframe.

   commands:
      average        Calculate the average platinum price of an item.

   options:
      -h, --help     Show this message and exit.
      -V, --version  Show the program's version number and exit.

Average
-------

| Average is currently the only subcommand available in WarMAC.
| Its command-line usage is as follows:

.. code-block:: none

   usage: warmac average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r] [-b] item

   Calculate the average platinum price of an item. Able to find the median, mean, mode,
   geometric mean, and harmonic mean of the specified item.

   positional arguments:
   item                       Item to find the statistic of. If the item spans multiple words,
                              please enclose the item within quotation marks.

   options:
   -s, --stats <stat>         Specifies which statistic to return; Can be one of [median, mean, mode, harmonic, geometric]. (Default: median)
   -p, --platform <platform>  Specifies which platform to fetch orders for; Can be one of [pc, ps4, xbox, switch]. (Default: pc)
   -t, --timerange <days>     Specifies in days how old the orders can be. Must be in range [1, 60]. (Default: 10)
   -m, --maxrank              Get price statistic of the mod/arcane at max rank instead of at unranked. (Default: False)
   -r, --radiant              Get price statistic of the relic at radiant refinement instead of at intact. (Default: False)
   -b, --buyers               Take the average platinum price from buyer orders instead of from seller orders. (Default: False)
   -v, --verbose              Prints additional information about the program.
   -h, --help                 Show this message and exit.
