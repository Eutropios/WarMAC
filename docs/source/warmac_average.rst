.. _warmac_average:

#################
 Average Command
#################

|  The Average command is the subcommand that handles calculating the
   statistical average of the specified item.

.. note::

   Only global variables and constants that are public are documented. Please
   see the source code for private variable/constant documentation.

.. py:data:: warmac_average.AVG_FUNCS
   :type: typing.Dict[str, typing.Callable[[typing.Sequence[int]], float]]
   :value: {'geometric': statistics.geometric_mean, 'harmonic': statistics.harmonic_mean, 'mean': statistics.mean, 'median': statistics.median, 'mode': statistics.mode}

   A dictionary that maps user input to its respective function.

.. py:data:: warmac_average.CURR_TIME
   :type: ~datetime.datetime
   :value: datetime.datetime.now(datetime.timezone.utc)

   An ISO-8601 timestamp of the current time retrieved on execution.

.. py:data:: warmac_average.headers
   :type: typing.Dict[str, str]
   :value: {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/116.0', 'Content-Type': 'application/json', 'Host': 'api.warframe.market', 'Accept': 'application/json'}

   A dictionary containing the headers to be used in the HTTP request. During execution, another header is added named 'platform', which contains one of ('pc', 'xbox', 'ps4', 'switch') corresponding to the user's platform.

.. autoclass:: warmac_average._WarMACJSON
   :members:
   :undoc-members:
   :private-members:
   :special-members: __init__

.. autofunction:: warmac_average._get_page

.. autofunction:: warmac_average._calc_avg

.. autofunction:: warmac_average._in_time_r

.. autofunction:: warmac_average._comp_val

.. autofunction:: warmac_average._filter_order

.. autofunction:: warmac_average._get_plat_list

.. autofunction:: warmac_average._verbose_out

.. autofunction:: warmac_average.average
