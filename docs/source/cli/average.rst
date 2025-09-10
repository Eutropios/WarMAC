.. _average_usage:

.. program:: warmac average

#########
 Average
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
   be one of median, mean, mode, harmonic, or geometric. By default, the
   calculated statistic is the item's median price.

.. option:: -p, --platform <platform>

   Specifies which platform to fetch the item's orders for. It can be one of pc,
   ps4, xbox, or switch. By default, the platform that the orders are fetched
   for is PC.

.. option:: -S, --same-platform

   Specifies that orders from only the platform given by :option:`--platform`
   will be collected, instead of collecting orders cross-platform. Will be
   ignored if passed without :option:`--platform`.

.. option:: -t, --timerange <days>

   Specifies the number of days to consider for calculating the average. The
   value for <days> indicates how far back to start the statistic calculation.
   The value given must be within the range of 1 to 60. By default, orders up
   to 5 days old are taken into account.

.. option:: -m, --maxrank
   
   Calculates the price statistic of the mod/arcane at its maximum rank instead
   of when it is unranked. This option cannot be used together with the
   :option:`--radiant` option.

.. option:: -r, --radiant

   Calculates the price statistic of the relic at a radiant refinement instead
   of at an intact refinement. This option cannot be used together with the
   :option:`--maxrank` option.

.. option:: -b, --buyers
   
   Calculates the price statistic of the item based on orders from buyers
   instead of orders from sellers.

.. option:: -n, --ndigits

   Specifies the number of decimal places to round the statistic to. Must be in
   range [0, 10). By default, the number of decimals rounded to is 1.

.. option:: -d, --detailed-report

   Prints additional market information about the requested item, along with
   the parameters you have specified. This includes
   * the type of statistic you requested,
   * the average price calculated for the item,
   * the minimum and maximum prices found, and
   * the total number of matching orders found.

.. option:: --porcelain

   Prints the bare detailed report separated with colons. Will be ignored if
   not passed with :option:`--detailed-report`.

.. option:: -h, --help
   
   Prints the command line usage and then exits. If used, WarMAC will ignore
   all other options.

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

   $ warmac average -p ps4 -t 5 -d "bite" | grep "Number of Orders"
   Number of Orders:      93

|  WarMAC output can also be redirected to a file:

.. code-block:: console

   $ warmac average -p PC -t 2 -d "vengeful revenant" > warmacOut.txt
   $ cat warmacOut.txt
   Item:                  Vengeful Revenant
   Time Range:            2 days
   Median Price:          5.0 platinum
   Max Price:             30 platinum
   Min Price:             4 platinum
   Number of Orders:      38

Porcelain Output
----------------

|  Porcelain output is in the form of colon-separated values.
