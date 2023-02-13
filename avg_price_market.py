"""
Author: Noah J (Eutropios; Sink Cat)
Date of Creation: January 22, 2023
Date Last Modified: February 13, 2023
Version 1.1.0
Version of Python built with: 3.11.2 (Not required, I believe 3.6 will suffice)

THIS PROJECT IS STILL IN DEVELOPMENT. Additional error handling, expansion of time lookups,
and deleting lowest/highest sell prices to keep average in line are coming soon.
I recognize that this isn't the most efficient method of obtaining prices. Warframe.market has
an API that can be accessed, which would increase efficiency.
Packages required: urllib3, colorama, beautifulsoup4

Scrapes the sell price from all listings of a given item from https://warframe.market,
then finds the average of the remaining listings.

***I am NOT affiliated with Warframe, Digital Extremes and its subsidaries, Warframe.market, 
Playstation, Sony and its subsidaries, XBOX, or Microsoft its subsidaries.***
"""

import json
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from bs4 import BeautifulSoup as bs

def get_platform():
    colorama_init()
    print(f"What platform are you on? {Fore.YELLOW}PC{Style.RESET_ALL}, " +
            f"{Fore.GREEN}XBOX{Style.RESET_ALL}, {Fore.BLUE}PS4{Style.RESET_ALL}, " +
            f"or {Fore.RED}Switch{Style.RESET_ALL}?")
    platform = str(input()).lower().strip()
    if platform != "pc":
        return platform + "."
    else:
        return ""

def get_input():
    """Gets item user wants in a colourful way."""
    print("What part would you like to find the price of? " +
            f"Please use the form of {Fore.GREEN}\"Braton Prime Set\"{Style.RESET_ALL}: ")
    name_of_item = str(input()).lower().strip()
    return name_of_item

def url_of_item(platform, name_of_item):
    """Fixes the string of a user input so it can be used in a URL."""
    name_of_item = name_of_item.replace("&", "and")
    name_of_item = name_of_item.replace(" ", "_")
    url_to_scrape = "https://" + platform + "warframe.market/items/" + name_of_item
    return url_to_scrape

def output_message(item, avg):
    """Outputs the average platinum for the specified item in a colourful way."""
    print(f"The going rate for a {Fore.GREEN}{item}{Style.RESET_ALL} " +
            f"is {Fore.GREEN}{avg}{Style.RESET_ALL}.")

def main():
    """Main function"""
    platform, get_item = get_platform(), get_input()
    url_to_scrape = url_of_item(platform, get_item)
    page = urlopen(Request(url_to_scrape, headers={'User-Agent': 'Mozilla'}))
    page_decoded = bs(page.read().decode('utf-8'), "lxml")
    found_em = page_decoded.find("script", attrs = {"id": "application-state"})
    em_decoded = found_em.decode(None, "utf-8")
    no_prefix = em_decoded.removeprefix('<script id="application-state" type="application/json">')
    stripped_garbage = json.loads(no_prefix.removesuffix('</script>'))
    item_list = stripped_garbage['payload']['orders']
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

if __name__ == "__main__":
    main()
    print("Would you like to find the average price of another item? (Y/N)")
    user_inp = str(input()).lower()
    while(user_inp == "yes") or user_inp == "y":
        main()
        print("Would you like to find the average price of another item? (Y/N)")
        user_inp = str(input()).lower()
    print("Thanks for using this script!")
