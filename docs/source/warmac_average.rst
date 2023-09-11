.. _warmac_average:

Average Command
===============

.. py:data:: warmac_average.AVG_FUNCS
   :type: typing.Dict[str, typing.Callable[[typing.Sequence[int]], float]]

.. py:data:: warmac_average.CURR_TIME
   :type: datetime.datetime
   :value: datetime.datetime.now(datetime.timezone.utc)

.. data:: warmac_average.headers

.. autoclass:: warmac_average._WarMACJSON
   :members:
   :undoc-members:
   :show-inheritance:
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
