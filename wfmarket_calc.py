"""
Warframe Market Average Calculator (WarMAC)
Copyright (c) 2023 Noah Jenner under MIT License

**I am NOT affiliated with Warframe, Digital Extremes and its subsidaries, Warframe.market, 
Playstation, Sony and its subsidaries, XBOX, or Microsoft its subsidaries.**

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: March 24, 2023
Version 1.3.7
Version of Python required: 3.10
External packages required: requests, colorama

UPCOMING:
    Switching script to STRICTLY command line (maybe keep mixed one as an alternative for less
    technically inclined users?)
TO ADD:
    Expansion of time lookup dates, and deleting lowest/highest sell prices to keep average in line are coming soon.
NOTABLE IDEAS:
    Graph functionality for listing prices over time?
    List top most expensive items? (Might be extremely hard given the amount of items within db)
"""

import json
import sys
from datetime import datetime, timezone
import requests as rq
from colorama import Fore, Style, init as c_init, deinit as c_deinit
#importing init as c_init to avoid confusion with object init

PLATFORMS = {"xbox", "switch", "ps4", "pc"}
PLATFORM_DICT = {"xbox one":"xbox", "xbox series x":"xbox", "xbox series s":"xbox",
            "nintendo switch":"switch", "oled switch":"switch", "switch lite":"switch",
            "nintendo switch lite":"switch", "playstation":"ps4", "playstation 4":"ps4",
            "playstation 5":"ps4", "ps5":"ps4", "ps":"ps4"}

API_ROOT_LINK = "https://api.warframe.market/v1/items"
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
            sys.stderr.write("This item does not exist! Please check your spelling\n")
            return False
        case _:
            with open("errorLog.txt", "a", encoding="UTF-8") as log_file:
                print(log_file.write(http_code))
            return False

def get_db() -> dict:
    """Gets a complete database of all items in the game from the root link

    :return: returns a json object containing all items
    :rtype: dict
    """

    page = rq.get(API_ROOT_LINK, headers=headers, timeout=5)
    if page.status_code == 200:
        return json.loads(page.text)
    sys.stderr.write("Database error. Please report issue on the Github page " +
                    "(link in README.rst file)")
    return {}

def get_platform() -> any:
    """
    Gets the platform of the user and adds it to the HTTP request header
    """

    platform = ""
    while True:
        print(f"What platform are you on? {Fore.YELLOW}PC{Style.RESET_ALL}, " +
            f"{Fore.GREEN}XBOX{Style.RESET_ALL}, {Fore.BLUE}PS4{Style.RESET_ALL}, " +
            f"or {Fore.RED}Switch{Style.RESET_ALL}?")
        platform = str(input()).lower().strip()
        if platform in PLATFORMS:
            break
        if platform in PLATFORM_DICT:
            platform = platform.replace(platform, PLATFORM_DICT[platform])
            break
        sys.stderr.write(f"Sorry, {platform} is not a valid entry.")
    headers['Platform'] = platform

def get_input() -> str:
    """
    Gets the name of the item user wants to find the average price of. Prints messages in a
    colourful way and verifies that it exists within the API database. Suggested to run
    through url_of_item().

    :return: User input, unparsed. Contains spaces, not fixed for URLs
    :rtype: string
    """

    print("What part would you like to find the price of? " +
            f"Please use the form of {Fore.CYAN}\"Braton Prime Set\"{Style.RESET_ALL}: ")
    name_of_item = str(input()).lower().strip()
    return name_of_item

def url_of_item(name_of_item: str) -> str:
    """
    Fixes the string of a user input so it can be used in the APIs URL.

    :param name_of_item: the name of the item that the user requested
    :type name_of_item: string
    :return: the API URL containing the associated item that the user requested
    :rtype: string
    """
    name_of_item = name_of_item.replace("&", "and")
    name_of_item = name_of_item.replace(" ", "_")
    listings_url = API_ROOT_LINK + "/" + name_of_item + "/orders"
    return listings_url

def find_avg(orders_list: dict, year: str, month: str) -> float:
    """function that calculates the avg price of the item

    :param item: the name of the requested item
    :type item: string
    :param orders_list: json dictionary of all of the listings of the requested item
    :type orders_list: dictionary
    :param year: year of bounds for search
    :type year: string
    :param month: month of bounds for search
    :type month: string
    """

    num_orders, plat_count = 0, 0
    for i in orders_list:
        if i['order_type'] == 'sell':
            creatn_date = i['last_update']
            #IDEA: if no orders found, ask user if they want to expand their date bounds
            listing_y, listing_m = creatn_date[0:4], creatn_date[5:7]
            if listing_y == year and int(month) - int(listing_m) <= 2:
                num_orders += 1
                plat_count += i['platinum']


    avg_cost = plat_count/num_orders
    return round(avg_cost, 1)

def logic() -> any:
    """
    Logic of the program
    """
    get_platform()
    get_item = get_input()
    listings_url = url_of_item(get_item)
    page = rq.get(listings_url, headers=headers, timeout=5)
    if net_error_checking(page.status_code):
        pulled_listings = json.loads(page.text) #creates json dictionary
        #when there are no listings found, the program throws an error. Let's catch it!
        item_list = pulled_listings['payload']['orders']
        now = datetime.now(timezone.utc)
        year, month = now.strftime("%Y"), now.strftime("%m")
        try:
            print(f"The going rate for a {Fore.CYAN}{get_item}{Style.RESET_ALL} " +
                f"is {Fore.CYAN}{find_avg(item_list, year, month)}{Style.RESET_ALL}.")
        except ArithmeticError:
            sys.stderr.write("There were no listings of this item within the past 2 months found.")

def main() -> any:
    """
    Main function that is looped to acompany for repeated user requests.
    """
    try:
        item_db = get_db()
        if bool(item_db): #erroneous check to see if the database is up
            c_init()
            while True:
                logic()
                print("Would you like to find the average price of another item? (Y/N)")
                user_inp = str(input()).lower()
                if user_inp in ("no", "n"):
                    break
            print("Thanks for using this script!")
            c_deinit()
    except rq.exceptions.ConnectionError:
        sys.stderr.write("You're not connected to the internet.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #prevents errors if ctrl+c is used
        sys.stderr.write("")
