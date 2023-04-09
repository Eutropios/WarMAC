#!/test

"""
Warframe Market Average Calculator (WarMAC)
Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: April 8, 2023
Version 1.3.9
Version of Python required: 3.10
External packages required: requests, colorama

UPCOMING:
    Switching script to STRICTLY command line (maybe keep mixed one as an alternative for less
    technically inclined users?)
TO ADD:
    Expansion of time lookup dates, and deleting lowest/highest sell prices to keep average in line
    are coming soon.
NOTABLE IDEAS:
    Graph functionality for listing prices over time?
    List top most expensive items? (Might be extremely hard given the amount of items within db)
"""

#import argparse
from datetime import datetime, timezone
from requests import api as rq, exceptions as rq_except
from colorama import Fore, Style, init as c_init, deinit as c_deinit
#importing init as c_init to avoid confusion with object init

PLATFORMS = {"xbox", "switch", "ps4", "pc"}
PLATFORM_DICT = {"xbox one":"xbox", "xbox series x":"xbox", "xbox series s":"xbox",
            "nintendo switch":"switch", "oled switch":"switch", "switch lite":"switch",
            "nintendo switch lite":"switch", "playstation":"ps4", "playstation 4":"ps4",
            "playstation 5":"ps4", "ps5":"ps4", "ps":"ps4"}

API_ROOT = "https://api.warframe.market/v1/items"
headers={'User-Agent': 'Mozilla', 'Content-Type': 'application/json'}

def net_error_checking(http_code: int) -> bool:
    """Uses a switch statement to check the server's response code.

    :param http_code: the status code returned by the GET request sent to the server
    :type http_code: integer
    :return: boolean indicating if the GET request was succesful. True if 200, False otherwise
    :rtype: bool
    """

    match http_code:
        case 200:
            return True
        case 404:
            #when the requested item doesnt exist within the db
            return False
        case _:
            with open("errorLog.txt", "a", encoding="UTF-8") as log_file:
                print(log_file.write(http_code))
            return False

def get_platform():
    """
    Gets the platform of the user and adds it to the HTTP request header
    """

    platform = ""
    while True:
        print(f"What platform are you on? {Fore.YELLOW}PC{Style.RESET_ALL}, " +
            f"{Fore.GREEN}XBOX{Style.RESET_ALL}, {Fore.BLUE}PS4{Style.RESET_ALL}, " +
            f"or {Fore.RED}Switch{Style.RESET_ALL}?")
        platform = input().strip().lower()
        if platform in PLATFORM_DICT:
            platform = platform.replace(platform, PLATFORM_DICT[platform])
        if platform in PLATFORMS:
            break
        print(f"Sorry, {platform} is not a valid entry.")
    headers['Platform'] = platform

def find_avg(orders_list: dict, now: datetime) -> float:
    """function that calculates the avg price of the item

    :param orders_list: list of all orders of the specified item
    :type orders_list: dict
    :param now: the date and time that it is currently
    :type now: datetime
    :return: the average price of all listings of the specified item
    :rtype: float
    """

    num_orders, plat_count = 0, 0
    for i in orders_list:
        if i['order_type'] == 'sell':
            time_difference = now - datetime.fromisoformat(i['last_update'])
            #IDEA: if no orders found, ask user if they want to expand their date bounds
            if time_difference.days <= 60:
                num_orders += 1
                plat_count += i['platinum']
    avg_cost = plat_count/num_orders
    return round(avg_cost, 1)

def logic():
    """
    Logic of the program
    """
    get_platform()
    print("What part would you like to find the price of? " +
            f"Please use the form of {Fore.CYAN}\"Braton Prime Set\"{Style.RESET_ALL}: ")

    #get user input and sends it to lowercase, then strips it of trailing spaces
    name_of_item = input().strip().lower()
    #replace problematic characters that would cause issues in a URL
    char_fixes = name_of_item.replace(' ', '_').replace('&', 'and')
    req_url = f"{API_ROOT}/{char_fixes}/orders"

    page = rq.get(req_url, headers=headers, timeout=5)
    if net_error_checking(page.status_code):
        pulled_listings = page.json() #creates json dictionary
        item_list = pulled_listings['payload']['orders']
        now = datetime.now(timezone.utc)
        try:
            print(f"The going rate for a {Fore.CYAN}{name_of_item}{Style.RESET_ALL} " +
                f"is {Fore.CYAN}{find_avg(item_list, now)}{Style.RESET_ALL}.")
        except ArithmeticError:
            print("There were no listings of this item within the past 2 months found.")
    else:
        print("This item does not exist! Please check your spelling\n")

def main():
    """
    Main function that is looped to acompany for repeated user requests.
    """
    try:
        if rq.head(API_ROOT, headers=headers, timeout=5).status_code == 200:
            #erroneous check to see if the website is up
            c_init()
            while True:
                logic()
                print("Would you like to find the average price of another item? (Y/N)")
                user_inp = input().strip().lower()
                if user_inp in ("no", "n"):
                    break
            print("Thanks for using this script!")
            c_deinit()
        else:
            print("Database error. Please report issue on the Github page " +
                    "(link in README.rst file)")
    except rq_except.ConnectionError:
        print("You're not connected to the internet.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #prevents errors if ctrl+c is used
        print("Exiting program.")
