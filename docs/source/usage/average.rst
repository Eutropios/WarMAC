.. _average:

.. program:: warmac average

#########
 average
#########

*******
 Usage
*******

.. code-block:: console

   $ warmac average [options] item

|  The average command is used to calculate the average platinum price of a
   specific item. It provides the average platinum price for any tradable item.

.. important:: 

   For item names with multiple words, please use one of the following options:

   1. Enclose the item's name within quotation marks. Example: ``"condition overload"``
   2. Replace spaces with underscore characters. Example: ``condition_overload``

.. option:: item

   The item in which to calculate the price statistic for.

*********
 Options
*********

.. tip:: 

   Options that take an argument can be in the form of ``--foo bar`` or
   ``--foo=bar``.

.. option:: -s, --stats <statistic>

   Specifies the type of statistical average to calculate for the item. It can
   be one of median, mean, mode, or geometric. By default, the calculated
   statistic is the item's median price.

.. option:: -p, --platform <platform>

   Specifies which platform to fetch the item's orders for. It can be one of pc,
   ps4, xbox, or switch. By default, the platform that the orders are fetched
   for is PC.

.. option:: -t, --timerange <days>

   Determines the number of days to consider for calculating the average. The
   value for <days> indicates how far back to start the statistic calculation.
   The value given must be within the range of 1 to 60. By default, orders up
   to 10 days old are taken into account.

.. option:: -m, --maxrank
   
   Calculates the price statistic of the mod/arcane at its maximum rank instead
   of when it is unranked. This option cannot be used together with the
   :option:`warmac average --radiant` option.

.. option:: -r, --radiant

   Calculates the price statistic of the relic at a radiant refinement instead
   of at an intact refinement. This option cannot be used together with the
   :option:`warmac average --maxrank` option.

.. option:: -b, --buyers
   
   Calculates the price statistic of the item based on orders from buyers
   instead of orders from sellers.

.. option:: -v, --verbose

   Prints additional market information about the requested item, along with
   the parameters you have specified. This includes:
   
   * The type of statistic you requested
   * The average price calculated for the item
   * The time range you specified for the request
   * The highest and lowest prices found
   * The total number of matching orders found.

.. option:: -h, --help
   
   Prints the command line usage and then exits. If ``-h`` or ``--help`` are
   used, WarMAC will ignore all other options.

**********
 Examples
**********

|  Calculating the median price of the mod "Primed Continuity" on PS4.
   Note that the median is calculated as it's the default.

.. code-block:: console

   $ warmac average -p ps4 "primed continuity"

|  Calculating the mode price of the mod "Bite" when it's at max rank on PC.
   Note that the PC price is calculated as it's the default.

.. code-block:: console

   $ warmac average -s mode -m bite

Handling Output
===============

|  WarMAC accepts outgoing pipes just like any other tool:

.. code-block:: console

   $ warmac average -p ps4 -t 5 -v "bite" | grep "Time Range"
   Time Range Used:             10 days

|  WarMAC output can also be redirected to a file:

.. code-block:: console

   $ warmac average -p PC -t 2 -v "vengeful revenant" > warmacOut.txt
   $ cat warmacOut.txt
   Item:                  Vengeful Revenant
   Statistic Found:       Median
   Time Range Used:       2 days
   Median Price:          5.0 platinum
   Max Price:             30 platinum
   Min Price:             4 platinum
   Number of Orders:      38
