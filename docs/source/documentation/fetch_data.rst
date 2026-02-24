.. _fetch_data:

############
 Fetch Data
############

|  Makes HTTP requests given a particular WarMAC schema.

.. py:type:: fetch_data.ResponseKind

   A type alias representing the union of :doc:`"-Response" structs </schema>`.

.. py:data:: fetch_data.T
   :value: TypeVar(T, OrderResponse, ItemResponse)

   Invariant :py:class:`~typing.TypeVar` constrained to :py:class:`schema.OrderResponse` and :py:class:`schema.ItemResponse`.

.. py:data:: fetch_data.HTTP_ERROR_DICT
   :type: typing.Final[~collections.abc.Mapping[int, type[errors.WarMACHTTPError]]] 
   :value: {401: errors.UnauthorizedAccessError, 403: errors.ForbiddenRequestError, 404: errors.MalformedURLError, 405: errors.MethodNotAllowedError, 500: errors.InternalServerError}

   A dictionary that maps integers to HTTP-related errors.

.. py:data:: fetch_data.API_ROOT
   :type: str
   :value: "https://api.warframe.market/v2/"

   warframe.market API root.

.. py:data:: fetch_data.SCHEMA_TO_URL
   :type: ~collections.abc.Mapping[ResponseKind, str]
   :value: {schema.OrderResponse: "orders/item/", schema.ItemResponse: "item/"}

   A dictionary that makes Response schemas to strings.

.. autofunction:: fetch_data.item_url

.. autofunction:: fetch_data.get_page

.. autofunction:: fetch_data.get_data
