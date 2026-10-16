:no-search:

############
 Fetch Data
############

|  Makes HTTP requests given a particular WarMAC schema.

.. py:type:: fetch_data.ResponseType
   :canonical: ~typing.TypeVar(ResponseType, schema.OrderResponse, schema.ItemResponse)

   Invariant TypeVar constrained to ``schema.OrderResponse`` and ``schema.ItemResponse``.

.. autofunction:: fetch_data.item_url

.. autofunction:: fetch_data.http_code_check

.. autofunction:: fetch_data.get_page

.. autofunction:: fetch_data.get_data
