.. _schema:

###############
 Schema Models
###############

| All msgspec.structs used in the program.

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
   
   Bases: :py:class:`.Base`

   An order on Warframe Market.

   .. py:attribute:: schema.Order.id
      :type: str

      Unique id of order.

   .. py:attribute:: schema.Order.type
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
