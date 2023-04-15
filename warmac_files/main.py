"""
Warframe Market Average Calculator (WarMAC)
~~~~~~~~~~~~~~~~~~~
Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: April 14, 2023
Version 1.4.0
Version of Python required: 3.10
External packages required: requests, colorama

UPCOMING:
    Expansion of time lookup dates, and deleting lowest/highest sell prices to keep average in line
    are coming soon.
NOTABLE IDEAS:
    * Graph functionality for listing prices over time?
    * List top most expensive items? (Might be extremely hard given the amount of items within db)
"""
import typing
if typing.TYPE_CHECKING:
    from argparse import ArgumentParser
from datetime import datetime as dt, timezone as tz
from requests import api as rq, exceptions as rq_except
from colorama import Fore, Style, init as c_init, deinit as c_deinit
from warmac_files import _arguments

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

def find_avg(orders_list: dict) -> float:
    """function that calculates the avg price of the item

    :param orders_list: list of all orders of the specified item
    :type orders_list: dict
    :param now: the date and time that it is currently
    :type now: datetime
    :return: the average price of all listings of the specified item
    :rtype: float
    """

    now = dt.now(tz.utc)
    num_orders, plat_count = 0, 0
    for i in orders_list:
        if i['order_type'] == 'sell':
            time_difference = now - dt.fromisoformat(i['last_update'])
            if time_difference.days <= 60:
                num_orders += 1
                plat_count += i['platinum']
    avg_cost = plat_count/num_orders
    return round(avg_cost, 1)

def logic(args: "ArgumentParser"):
    """
    Logic of the program
    """
    headers['Platform'] = (args.platform).lower()
    name_of_item = args.item_to_find.strip().lower()
    # replace problematic characters that would cause issues in a URL
    char_fixes = name_of_item.replace(' ', '_').replace('&', 'and')

    page = rq.get(f"{API_ROOT}/{char_fixes}/orders", headers=headers, timeout=5)
    if net_error_checking(page.status_code):
        item_list = page.json()['payload']['orders']  # creates json dictionary
        try:
            print(f"The going rate for a {Fore.CYAN}{name_of_item}{Style.RESET_ALL} is "
                  f"{Fore.CYAN}{find_avg(item_list)}{Style.RESET_ALL}.")
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
            c_init()
            logic(args)
            c_deinit()
        else:
            _arguments.err_handling(4)
    except rq_except.ConnectionError:
        _arguments.err_handling(1)
