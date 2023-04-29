"""
Warframe Market Average Calculator (WarMAC)
~~~~~~~~~~~~~~~~~~~
Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: April 28, 2023
Version 1.4.3
Version of Python required: 3.10
External packages required: requests

UPCOMING:
    Expansion of time lookup dates, and deleting lowest/highest sell prices to keep average in line
    are coming soon.
"""

import typing
if typing.TYPE_CHECKING:
    from argparse import ArgumentParser
from datetime import datetime as dt, timezone as tz
from requests import api as rq, exceptions as rq_except
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
            return False

def find_avg(orders_list: dict, args: "ArgumentParser") -> float:
    """function that calculates the avg price of the item

    :param orders_list: list of all orders of the specified item
    :type orders_list: dict
    :return: the average price of all listings of the specified item
    :rtype: float
    """

    num_orders = plat_count = highest = 0
    lowest = 999999  # ARBITRARY NUMBER. If an item sells for this ever, I'd be surprised
    now = dt.now(tz.utc)
    for order in orders_list:
        if (
            order['order_type'] == 'sell'
            and (now - dt.fromisoformat(order['last_update'])).days <= 60
        ):
            num_orders += 1
            plat_count += order['platinum']
            if order["platinum"] > highest:
                highest = order["platinum"]
            elif order["platinum"] < lowest:
                lowest = order["platinum"]
    if args.extra:
        print(f"Highest: {highest}\tLowest: {lowest}\tNumber of orders: {num_orders}")
    return round(plat_count/num_orders, 1)

def logic(args: "ArgumentParser"):
    """
    Logic of the program
    """
    headers['Platform'] = args.platform
    # replace problematic characters that would cause issues in a URL
    char_fixes = args.item.replace(' ', '_').replace('&', 'and')
    page = rq.get(f"{API_ROOT}/{char_fixes}/orders", headers=headers, timeout=5)
    if net_error_checking(page.status_code):
        item_list = page.json()['payload']['orders']  # creates json dictionary
        try:
            if args.verbose:
                print(f"The going rate for a {args.item} is {find_avg(item_list, args)}.")
            else:
                print(find_avg(item_list, args))
        except ArithmeticError:
            _arguments.err_handling(2)

def main():
    """
    Main function that is called which handles colorama init and deinit, as well as connection
    errors and setting up the argument parser."
    """

    try:
        parser = _arguments.create_parser()
        args = parser.parse_args()
        if rq.head(API_ROOT, headers=headers, timeout=5).status_code == 200:
            # erroneous check to see if the website is up
            logic(args)
        else:
            _arguments.err_handling(4)
    except rq_except.ConnectionError:
        _arguments.err_handling(1)
