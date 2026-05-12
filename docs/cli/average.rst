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

.. option:: -s, --stat <stat>

   Specifies the type of statistical average to calculate for the item. It can
   be one of median, mean, mode, or geometric. By default, the calculated
   statistic is the item's median price.

.. option:: -p, --platform <platform>

   Specifies which platform to fetch the item's orders for. It can be one of pc,
   ps4, xbox, or switch. Cross-play orders are enabled by default. To restrict
   orders to the specified platform only, use the --same-platform option. By
   default, the platform that the orders are fetched for is PC.

.. option:: -S, --same-platform

   Specifies that orders from only the platform given by :option:`--platform`
   will be collected, instead of collecting cross-platform orders. If passed
   without :option:`--platform`, this option will be ignored, and
   cross-platform orders will be collected.

.. option:: -t, --timerange <days>

   Specifies the number of days to consider for calculating the average. The
   value passed indicates how far back to start the statistic calculation. The
   value given must be within the range of 1 to 60. By default, only orders up
   to 5 days old are taken into account.

.. option:: -m, --maxrank

   Calculates the price statistic of the mod/arcane at its maximum rank instead
   of when it is unranked. This option does nothing if it is used with an item
   that is not a mod. This option cannot be used together with the
   :option:`--radiant` option.

.. option:: -r, --radiant

   Calculates the price statistic of the relic at a radiant refinement instead
   of at an intact refinement. This option does nothing if it used with an item
   that is not a relic. This option cannot be used together with the
   :option:`--maxrank` option.

.. option:: -b, --buyers

   Calculates the price statistic of the item based on orders from buyers
   instead of orders from sellers.

.. option:: -n, --ndigits <ndigits>

   Specifies the number of decimal places to round the statistic to. Must be in
   range [0, 10), that is, inclusive of 0 but exclusive of 10. By default, the
   number of decimals that the statistic is rounded to is 1.

.. option:: -d, --detailed-report

   Prints additional market information about the requested item, along with
   the parameters you have specified. This includes
   * the timerange for the orders,
   * the type of statistic calculated,
   * the statistic price calculated for the item,
   * the minimum and maximum prices found, and
   * the total number of matching orders found.

.. option:: --porcelain

   Prints the bare detailed report separated with colons. Will be ignored if
   not passed with :option:`--detailed-report`. Details on the structure of the
   formatted output can be found in the :ref:`Porcelain Output<porcelain-output>` section.

.. option:: -h, --help

   Prints the command line usage and then exits. If used, WarMAC will ignore
   all other options.

***********
 Examples
***********

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
   Number of Orders:      38 orders

.. _porcelain-output:

Porcelain Output
----------------

|  Porcelain output is in the form of colon-separated values adhering together
   to the following form :

|  <name of item>:<timerange>:<price calculated>:<min price in list>:<max price in list>:<number of orders>

|  For example:

.. code-block:: console

   $ warmac average -p PC -t 2 -d --porcelain "vengeful revenant"
   Vengeful Revenant:2:5.0:3:20:42

|  In this example, an inquiry is made about the median price of Vengeful
   Revenant over the past two days on PC. With 42 matching orders identified,
   it is shown to have a median price of 5.0 platinum, have a minimum price of 3
   platinum, and a maximum price of 20 platinum.
