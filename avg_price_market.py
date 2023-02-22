"""
Warframe Market Average Price Calculator
Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Copyright (C) 2023  Noah Jenner
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

***I am NOT affiliated with Warframe, Digital Extremes and its subsidaries, Warframe.market, 
Playstation, Sony and its subsidaries, XBOX, or Microsoft its subsidaries.***

Date of Creation: January 22, 2023
Date Last Modified: February 21, 2023
Version 1.3.0
Version of Python built with: 3.11.2 (Not required, I believe 3.6 will suffice)
Built in packages required: json, datetime
External packages required: urllib3, colorama, beautifulsoup4

TO ADD:
    THIS PROJECT IS STILL IN DEVELOPMENT. Additional error handling, expansion of time lookup dates,
    and deleting lowest/highest sell prices to keep average in line are coming soon.
"""

import json
from datetime import datetime, timezone
import requests as rq
from colorama import init as colorama_init, deinit as colorama_deinit
from colorama import Fore, Style

PLATFORMS = {"xbox", "switch", "ps4", "pc"}
PLATFORM_DICT = {"xbox one":"xbox", "xbox series x":"xbox", "xbox series s":"xbox",
            "nintendo switch":"switch", "oled switch":"switch", "switch lite":"switch",
            "nintendo switch lite":"switch", "playstation":"ps4", "playstation 4":"ps4",
            "playstation 5":"ps4", "ps5":"ps4", "ps":"ps4"}
API_ROOT_LINK = "https://api.warframe.market/v1/items"
headers={'User-Agent': 'Mozilla', 'Content-Type': 'application/json'}

def get_platform():
    """Gets the platform of the user and adds it to the HTTP request header"""
    colorama_init()
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
        print(f"Sorry, {platform} is not a valid entry.")
    headers['Platform'] = platform

def get_input():
    """Gets item user wants in a colourful way."""
    print("What part would you like to find the price of? " +
            f"Please use the form of {Fore.CYAN}\"Braton Prime Set\"{Style.RESET_ALL}: ")
    name_of_item = str(input()).lower().strip()
    return name_of_item

def url_of_item(name_of_item):
    """Fixes the string of a user input so it can be used in a URL."""
    name_of_item = name_of_item.replace("&", "and")
    name_of_item = name_of_item.replace(" ", "_")
    listings_url = API_ROOT_LINK + "/" + name_of_item + "/orders"
    return listings_url

def output_message(item, avg):
    """Outputs the average platinum for the specified item in a colourful way."""
    print(f"The going rate for a {Fore.CYAN}{item}{Style.RESET_ALL} " +
            f"is {Fore.CYAN}{avg}{Style.RESET_ALL}.")

def logic():
    """Logic of the program"""
    get_platform()
    get_item = get_input()
    listings_url = url_of_item(get_item)
    page = rq.get(listings_url, headers=headers, timeout=5)
    pulled_listings = json.loads(page.text)
    item_list = pulled_listings['payload']['orders']
    now = datetime.now(timezone.utc)
    year, month = now.strftime("%Y"), now.strftime("%m")

    num_orders, plat_count = 0, 0
    for i in item_list:
        if i['order_type'] == 'sell':
            creatn_date = i['last_update']
            listing_y, listing_m = creatn_date[0:4], creatn_date[5:7]
            if listing_y == year and int(month) - int(listing_m) <= 2:
                num_orders += 1
                plat_count += i['platinum']

    try:
        avg_cost = plat_count/num_orders

    except ArithmeticError:
        print("There were no listings of this item within the past 2 months found.")

    else:
        output_message(get_item, round(avg_cost, 1))

def main():
    """Main function that is looped."""
    while True:
        logic()
        print("Would you like to find the average price of another item? (Y/N)")
        user_inp = str(input()).lower()
        if user_inp in ("no", "n"):
            break
    print("Thanks for using this script!")
    colorama_deinit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #prevents errors if ctrl+c is used
        pass
