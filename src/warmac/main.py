"""
Warframe Market Average Calculator (WarMAC) 1.5.1
~~~~~~~~~~~~~~~~~~~
Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: May 5, 2023
Version of Python required: 3.10
External packages required: urllib3

UPCOMING:
    Mod rank and Arcane rank handling, show average from buy orders instead of sell orders,
    add drop sources tag, and deleting lowest/highest sell prices to keep average in line
    are coming soon. Possibly adding more average types.
"""

from datetime import datetime as dt, timezone as tz
from statistics import mean, median, mode, harmonic_mean
import urllib3 as rq
from src.warmac import _arguments

API_ROOT = 'https://api.warframe.market/v1/items'
headers = {'User-Agent': 'Mozilla', 'Content-Type': 'application/json'}


def err_handling(err_code: int) -> None:
    """Function that handles self-generated error codes within the program

    :param err_code: integer corresponding to a partciular error code.
    :type err_code: int
    """

    match err_code:
        case 1:
            print("You're not connected to the internet. Please check your internet connection and"
                  " try again.")
        case 2:
            print('There were no listings of this item found in your specified time range.')
        case 3:
            print('This item does not exist. Please check your spelling, and remember to use '
                  'parenthesis in the command line if the item is multiple words.')
        case 4:
            print('Database error. Please open a new issue on the Github/Gitlab page (link in '
                  'README.rst file).')
        case _:
            print('Unknown error, writing to errorLog.txt file. Please open a new issue on the '
                  'Github/Gitlab page (link in README.rst file).')


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
            err_handling(3)
            return False
        case _:
            err_handling(100)
            with open('./errorLog.txt', 'a', encoding='UTF-8') as log_file:
                print(log_file.write(f'{http_code}'))
            raise _arguments.WarMACError(message=f'Database Error. HTTP Code {http_code}')


def find_avg(plat_list: list, avg_type: str, extra: bool) -> float:
    """Calculates the average price of an item

    :param plat_list: list of the prices in platinum of each order
    :type plat_list: list
    :param avg_type: The type of average that the user wants to find. Can be mean, median, or mode
    :type avg_type: str
    :param extra: flag that indicates whether or not to print extra information
    :type extra: bool
    :return: the average price of all listings of the specified item
    :rtype: float
    """

    print(plat_list)
    if extra:
        print(f'Highest: {max(plat_list)}\tLowest: {min(plat_list)}\t'
              f'Number of orders found: {len(plat_list)}')
    if avg_type not in _arguments.AVG_MODES:
        raise _arguments.WarMACError(message='Not an acceptable average type.')
    return (
        round(mean(plat_list), 1) if avg_type == 'mean' else round(median(plat_list), 1)
        if avg_type == 'median' else round(mode(plat_list), 1) if avg_type == 'mode' else
        round(harmonic_mean(plat_list), 1) if avg_type == 'harmonic' else -1
    )


def recent_sale(item: dict, time_range: int) -> bool:
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
        item['order_type'] == 'sell'
        and (dt.now(tz.utc) - dt.fromisoformat(item['last_update'])).days <= time_range
    )


def main() -> None:
    """
    Main function that is called which handles colorama init and deinit, as well as connection
    errors and setting up the argument parser."
    """

    try:
        args = _arguments.create_parser().parse_args()
        headers['Platform'] = args.platform
        page = rq.request('GET', f"{API_ROOT}/{args.item.replace(' ', '_').replace('&', 'and')}"
                          "/orders", headers=headers, timeout=5)
        if net_error_checking(page.status):
            order_list = [
                order['platinum']
                for order in page.json()['payload']['orders'] if recent_sale(order, args.time_r)
            ]
            result = find_avg(order_list, args.avg_type, args.extra)
            print(f'The going rate for a {args.item} on {args.platform} is {result:.1f}.'
                  if args.verbose else f'{result:.1f}')

    except rq.exceptions.ProtocolError:
        # connection error
        err_handling(1)
    except ArithmeticError:
        # no orders of that item found
        err_handling(2)
    except _arguments.WarMACError:
        # 404 not found
        err_handling(4)
