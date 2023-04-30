"""
Warframe Market Average Calculator (WarMAC)
~~~~~~~~~~~~~~~~~~~
Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: April 30, 2023
Version 1.4.3
Version of Python required: 3.10
External packages required: urllib3

UPCOMING:
    Expansion of time lookup dates, and deleting lowest/highest sell prices to keep average in line
    are coming soon.
"""

from datetime import datetime as dt, timezone as tz
from statistics import mean
import urllib3 as rq
from src.warmac import _arguments

API_ROOT = "https://api.warframe.market/v1/items"
headers = {'User-Agent': 'Mozilla', 'Content-Type': 'application/json'}

def net_error_checking(http_code: int) -> bool:
    """Uses a switch statement to check the server's response code.

    :param http_code: the status code returned by the GET request
    :type http_code: integer
    :return: boolean indicating if the GET request was succesful. Returns True if https_code
    is 200, False otherwise
    :rtype: bool
    """

    match http_code:
        case 200:
            return True
        case 404:
            _arguments.err_handling(3)
            return False
        case _:
            _arguments.err_handling(100)
            with open("errorLog.txt", "a", encoding="UTF-8") as log_file:
                print(log_file.write(http_code))
            raise _arguments.DatabaseError

def find_avg(plat_list: list, extra: bool) -> float:
    """Calculates the average price of an item

    :param plat_list: list of the prices in platinum of each order
    :type plat_list: list
    :param extra: flag that indicates whether or not to print extra information
    :type extra: bool
    :return: the average price of all listings of the specified item
    :rtype: float
    """

    if extra:
        print(f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\t"
              f"Number of orders found: {len(plat_list)}")
    return round(mean(plat_list), 1)

def recent_sale(item: dict) -> bool:
    """
    Helper function that determines if the order listing is a sale, and if it was made or
    updated within the last 60 days.

    :param item: Information about a listing
    :type item: dict
    :return: True is the listing was created or modified in the last 60 days is of sell type.
    False if the listing was a buy type or older than 60 days.
    :rtype: bool
    """
    return (
        item["order_type"] == "sell"
        and (dt.now(tz.utc) - dt.fromisoformat(item['last_update'])).days <= 60
    )

def main():
    """
    Main function that is called which handles colorama init and deinit, as well as connection
    errors and setting up the argument parser."
    """

    try:
        args = _arguments.create_parser().parse_args()
        headers['Platform'] = args.platform
        page = rq.request("GET", f"{API_ROOT}/{args.item.replace(' ', '_').replace('&', 'and')}"
                          "/orders", headers=headers, timeout=5)
        if net_error_checking(page.status):
            order_list = [
                order["platinum"]
                for order in page.json()['payload']['orders'] if recent_sale(order)
            ]
            result = find_avg(order_list, args.extra)
            print(f"The going rate for a {args.item} is {result}." if args.verbose else result)

    except rq.exceptions.ProtocolError:
        # connection error
        _arguments.err_handling(1)
    except ArithmeticError:
        # no orders of that item found
        _arguments.err_handling(2)
    except _arguments.DatabaseError:
        # 404 not found
        _arguments.err_handling(4)
