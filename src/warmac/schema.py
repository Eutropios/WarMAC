"""Schemas used for msgspec validation against http requests.

-----------------------------------------------------------------------

WarMAC — https://github.com/Eutropios/WarMAC Copyright (C) 2024  Noah
Jenner

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import msgspec

# Descriptions of structs pulled from
# https://42bytes.notion.site/Data-Models-65e9ab01868c4dcca6ba499e68a04ac9#c61f4bb38c2e4b7abfcf4cfd3e7bdc35


class Base(msgspec.Struct):
    """The base struct for all structs to inherit from.

    The base struct for all structs to inherit from. Not actually used
    programmatically. Only exists for typing purposes.
    """


class ResponseBase(Base, rename="camel"):
    """The base struct for all Response structs to inherit from.

    The base struct for all Response structs to inherit from. Not
    actually used programmatically. Only exists for typing purposes.
    """


class UserShort(Base, rename="camel"):
    """Shortened model of a user excluding irrelevant information.

    Attributes:
        id: WFM user id.
        ingame_name: In-game name of user.
        reputation: Reputation score.
        platform: Gaming platform used by the user.
        crossplay: Indicates if the user has crossplay trade enabled.
    """

    id: str
    ingame_name: str
    reputation: int
    platform: str
    crossplay: bool


class Order(Base, rename="camel"):
    """An order on WFM.

    Attributes:
        id: Unique id of order.
        order_type: Specifies whether the order is a 'buy' or 'sell'.
        platinum: Total platinum currency involved in the order.
        quantity: Number of items included in the order.
        created_at: Creation time of the order.
        updated_at: Last modification time of the order.
        item_id: (optional) Unique identifier of the item.
        per_trade: (optional) Quantity per transaction.
        rank: (optional) Rank or level of the item in the order.
        charges: (optional) Number of charges left (requiem mods).
        subtype: (optional) Subtype or category of the item.
        amber_stars: (optional) Amber stars in a sculpture order.
        cyan_stars: (optional) Cyan stars in a sculpture order.
        vosfor: (optional) Vosfor associated with arcane item.
    """

    id: str
    order_type: str = msgspec.field(name="type")
    platinum: int
    quantity: int
    created_at: str
    updated_at: str
    item_id: str | None = None
    per_trade: int | None = None
    rank: int | None = None
    charges: int | None = None
    subtype: str | None = None
    amber_stars: int | None = None
    cyan_stars: int | None = None
    vosfor: int | None = None


class OrderWithUser(Base, rename="camel"):
    """Order with user info.

    Attributes:
        id: Unique id of order.
        order_type: Specifies whether the order is a 'buy' or 'sell'.
        platinum: Total platinum currency involved in the order.
        quantity: Number of items included in the order.
        created_at: Creation time of the order.
        updated_at: Last modification time of the order.
        item_id: Unique identifier of the item.
        user: User who created the order, with basic profile info.
        per_trade: (optional) Quantity per transaction.
        rank: (optional) Rank or level of the item in the order.
        charges: (optional) Number of charges left (requiem mods).
        subtype: (optional) Subtype or category of the item.
        amber_stars: (optional) Amber stars in a sculpture order.
        cyan_stars: (optional) Cyan stars in a sculpture order.
        vosfor: (optional) Vosfor associated with arcane item.
    """

    id: str
    order_type: str = msgspec.field(name="type")
    platinum: int
    quantity: int
    created_at: str
    updated_at: str
    item_id: str
    user: UserShort
    per_trade: int | None = None
    rank: int | None = None
    charges: int | None = None
    subtype: str | None = None
    amber_stars: int | None = None
    cyan_stars: int | None = None
    vosfor: int | None = None


class OrderResponse(ResponseBase, rename="camel"):
    """Response received from making the HTTP request to the API.

    Attributes:
        api_version: Version of the API.
        data: List of orders associated with item request.
        error: (optional) Error message.
    """

    api_version: str
    data: list[OrderWithUser]
    error: str | None = None


class Item(Base, rename="camel"):
    """Full item model containing information about item.

    Attributes:
        id: Unique identifier of the item.
        slug: URL-friendly name of the item.
        tags: Info tags associated with item.
        set_root: (optional) Indicates if the item is the set root.
        set_parts: (optional) Parts associated with item set.
        quantity_in_set: (optional) Number of items in set.
        rarity: (optional) Rarity of item if mod or arcane.
        max_rank: (optional) Maximum rank the item can achieve.
        max_charges: (optional) Maximum charges of item, used for
            requiem mods.
        bulk_tradable: (optional) Indicates if the item is bulk-
            tradable.
        subtypes: (optional) Subtype or category of the item.
        max_amber_stars: (optional) Number of amber stars associated
            with the item.
        max_cyan_stars: (optional) Number of cyan stars associated with
            the item.
        base_endo: (optional) Base endo value of the item.
        endo_multiplier: (optional) Multiplier for the endo value.
        ducats: (optional) Ducats value of the item.
        req_mastery_rank: (optional) Mastery rank needed to trade the
            particular item.
        vaulted: (optional) Indicates if the item is vaulted.
        trading_tax: (optional) Trading tax of item.
    """

    id: str
    slug: str
    tags: list[str]
    set_root: bool | None = None
    set_parts: list[str] | None = None
    quantity_in_set: int | None = None
    rarity: str | None = None
    max_rank: int | None = None
    max_charges: int | None = None
    bulk_tradable: bool | None = None
    subtypes: list[str] | None = None
    max_amber_stars: int | None = None
    max_cyan_stars: int | None = None
    base_endo: int | None = None
    endo_multiplier: float | None = None
    ducats: int | None = None
    req_mastery_rank: int | None = None
    vaulted: bool | None = None
    trading_tax: int | None = None


class ItemResponse(ResponseBase, rename="camel"):
    """Response received from making the HTTP request to the API.

    Attributes:
        api_version: Version of the API.
        data: Item information associated with request.
        error: (optional) Error message.
    """

    api_version: str
    data: Item
    error: str | None = None
