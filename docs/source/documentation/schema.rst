###############
 Schema Models
###############

|  All msgspec.structs used in the program.

.. autoclass:: schema.Base
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. autoclass:: schema.ResponseBase
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. py:class:: schema.UserShort
   :canonical: warmac.schema.UserShort

   Bases: :py:class:`.Base`

   Shortened model of a user excluding irrelevant information.

   .. py:attribute:: schema.UserShort.id
      :type: str

      Warframe Market user-id.

   .. py:attribute:: schema.UserShort.ingame_name
      :type: str

      In-game name of user.

   .. py:attribute:: schema.UserShort.reputation
      :type: int

      Reputation score

   .. py:attribute:: schema.UserShort.platform
      :type: str

      Gaming platform used by the user

   .. py:attribute:: schema.UserShort.crossplay
      :type: bool

      Indicates if the user has crossplay trade enabled

.. py:class:: schema.Order
   :canonical: warmac.schema.Order

   Bases: :py:class:`.Base`

   An order on Warframe Market.

   .. py:attribute:: schema.Order.id
      :type: str

      Unique id of order.

   .. py:attribute:: schema.Order.order_type
      :type: str

      Specifies whether the order is a 'buy' or 'sell'.

   .. py:attribute:: schema.Order.platinum
      :type: int

      Total platinum currency involved in the order.

   .. py:attribute:: schema.Order.quantity
      :type: int

      Number of items included in the order.

   .. py:attribute:: schema.Order.created_at
      :type: str

      Creation time of the order.

   .. py:attribute:: schema.Order.updated_at
      :type: str

      Last modification time of the order.

   .. py:attribute:: schema.Order.item_id
      :type: str | None

      Unique identifier of the item.

   .. py:attribute:: schema.Order.per_trade
      :type: int | None

      Quantity per transaction.

   .. py:attribute:: schema.Order.rank
      :type: int | None

      Rank or level of the item in the order.

   .. py:attribute:: schema.Order.charges
      :type: int | None

      Number of charges left (requiem mods).

   .. py:attribute:: schema.Order.subtype
      :type: str | None

      Subtype or category of the item.

   .. py:attribute:: schema.Order.amber_stars
      :type: int | None

      Amber stars in a sculpture order.

   .. py:attribute:: schema.Order.cyan_stars
      :type: int | None

      Cyan stars in a sculpture order.

.. py:class:: schema.OrderWithUser
   :canonical: warmac.schema.OrderWithUser

   Bases: :py:class:`.Base`

   An order on Warframe Market with user info.

   .. py:attribute:: schema.OrderWithUser.id
      :type: str

      Unique id of the order.

   .. py:attribute:: schema.OrderWithUser.order_type
      :type: str

      Specifies whether the order is a 'buy' or 'sell'.

   .. py:attribute:: schema.OrderWithUser.platinum
      :type: int

      Total platinum currency involved in the order.

   .. py:attribute:: schema.OrderWithUser.quantity
      :type: int

      Number of items included in the order.

   .. py:attribute:: schema.OrderWithUser.created_at
      :type: str

      Creation time of the order.

   .. py:attribute:: schema.OrderWithUser.updated_at
      :type: str

      Last modification time of the order.

   .. py:attribute:: schema.OrderWithUser.item_id
      :type: str

      Unique identifier of the item.

   .. py:attribute:: schema.OrderWithUser.user
      :type: UserShort

      User who created the order, with basic profile info.

   .. py:attribute:: schema.OrderWithUser.per_trade
      :type: int | None

      Quantity per transaction.

   .. py:attribute:: schema.OrderWithUser.rank
      :type: int | None

      Rank or level of the item in the order.

   .. py:attribute:: schema.OrderWithUser.charges
      :type: int | None

      Number of charges left (requiem mods).

   .. py:attribute:: schema.OrderWithUser.subtype
      :type: str | None

      Subtype or category of the item.

   .. py:attribute:: schema.OrderWithUser.amber_stars
      :type: int | None

      Amber stars in a sculpture order.

   .. py:attribute:: schema.OrderWithUser.cyan_stars
      :type: int | None

      Cyan stars in a sculpture order.

.. py:class:: schema.OrderResponse
   :canonical: warmac.schema.OrderResponse

   Bases: :py:class:`.ResponseBase`

   Response received from making the HTTP request to the API.

   .. py:attribute:: schema.OrderResponse.api_version
      :type: str

      Version of the API.

   .. py:attribute:: schema.OrderResponse.data
      :type: list[OrderWithUser]

      List of orders associated with the item request.

   .. py:attribute:: schema.OrderResponse.error
      :type: str | None

      Error message.

.. py:class:: schema.Item
   :canonical: warmac.schema.Item

   Bases: :py:class:`.Base`

   Full item model containing information about the item.

   .. py:attribute:: schema.Item.id
      :type: str

      Unique identifier of the item.

   .. py:attribute:: schema.Item.slug
      :type: str

      URL-friendly name of the item.

   .. py:attribute:: schema.Item.tags
      :type: list[str]

      Info tags associated with the item.

   .. py:attribute:: schema.Item.set_root
      :type: bool | None

      Indicates if the item is the set root.

   .. py:attribute:: schema.Item.set_parts
      :type: list[str] | None

      Parts associated with the item set.

   .. py:attribute:: schema.Item.quantity_in_set
      :type: int | None

      Number of items in the set.

   .. py:attribute:: schema.Item.rarity
      :type: str | None

      Rarity of the item if a mod or arcane.

   .. py:attribute:: schema.Item.max_rank
      :type: int | None

      Maximum rank the item can achieve.

   .. py:attribute:: schema.Item.max_charges
      :type: int | None

      Maximum charges of the item, used for requiem mods.

   .. py:attribute:: schema.Item.bulk_tradable
      :type: bool | None

      Indicates if the item is bulk-tradable.

   .. py:attribute:: schema.Item.subtypes
      :type: list[str] | None

      Subtype or category of the item.

   .. py:attribute:: schema.Item.max_amber_stars
      :type: int | None

      Number of amber stars associated with the item.

   .. py:attribute:: schema.Item.max_cyan_stars
      :type: int | None

      Number of cyan stars associated with the item.

   .. py:attribute:: schema.Item.base_endo
      :type: int | None

      Base endo value of the item.

   .. py:attribute:: schema.Item.endo_multiplier
      :type: float | None

      Multiplier for the endo value.

   .. py:attribute:: schema.Item.ducats
      :type: int | None

      Ducats value of the item.

   .. py:attribute:: schema.Item.req_mastery_rank
      :type: int | None

      Mastery rank needed to trade the particular item.

.. py:class:: schema.ItemResponse
   :canonical: warmac.schema.ItemResponse

   Bases: :py:class:`.ResponseBase`

   Response received from making the HTTP request to the API.

   .. py:attribute:: schema.ItemResponse.api_version
      :type: str

      Version of the API.

   .. py:attribute:: schema.ItemResponse.data
      :type: Item

      Item information associated with the request.

   .. py:attribute:: schema.ItemResponse.error
      :type: str | None

      Error message.
