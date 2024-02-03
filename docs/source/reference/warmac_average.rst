.. _warmac_average:

#################
 Average Command
#################

|  The Average command is the command that handles calculating the statistical
   average of the specified item.

.. note::

   Only global variables and constants that are public are documented. Please
   see the source code for private variable/constant documentation.

.. py:data:: warmac_average.FUNC_MAP
   :type: typing.Dict[str, typing.Callable[[typing.Sequence[int]], float]]
   :value: {'geometric': statistics.geometric_mean, 'mean': statistics.mean, 'median': statistics.median, 'mode': statistics.mode}

   A dictionary that maps user input to its respective function.

.. py:data:: warmac_average.CURR_TIME
   :type: ~datetime.datetime
   :value: datetime.datetime.now(datetime.timezone.utc)

   An ISO8601 timestamp of the current time retrieved on execution.

.. autoclass:: warmac_average._WarMACJSON
   :members:
   :undoc-members:

.. autofunction:: warmac_average._extract_info

.. autofunction:: warmac_average.get_page

.. autofunction:: warmac_average._calc_avg

.. autofunction:: warmac_average._in_time_r

.. autofunction:: warmac_average._comp_val

.. autofunction:: warmac_average._filter_order

.. autofunction:: warmac_average._get_plat_list

.. autofunction:: warmac_average._verbose_out

.. autofunction:: warmac_average.average
