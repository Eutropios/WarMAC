.. _config:

########
 Config
########


.. py:type:: config.AverageType
   :canonical: Literal["geometric", "mean", "median", "mode"]

   A type alias representing the union of average statistic types.

.. py:data:: config.DEFAULT_TIME
   :type: int
   :value: 5

   The default time that will be used for calculating listing ages.

.. py:data:: config.DEFAULT_NDIGITS
   :type: int
   :value: 1

   The default number of digits to round to when calculating an average.

.. py:data:: config.VERSION
   :type: str
   :value: "0.0.5"

   The current version of WarMAC.

.. py:data:: config.AVERAGE_FUNCTIONS
   :type: ~collections.abc.Mapping[str, ~collections.abc.Callable[[~collections.abc.Sequence[int]], float]]
   :value: {'geometric': statistics.geometric_mean, 'harmonic': statistics.harmonic_mean, 'mean': statistics.mean, 'median': statistics.median, 'mode': statistics.mode}

   A dictionary that maps strings to their respective statistics function.
