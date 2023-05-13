#!/usr/bin/env python3
"""
Warframe Market Average Calculator (WarMAC) 1.5.7
~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Entry point to WarMAC
Detailed program introduction found in main.py
Formal documentation WIP.

Date of Creation: January 22, 2023
Date Last Modified: May 13, 2023
Version of Python required for complete program: >=3.7.0
External packages required for complete program: urllib3
""" # noqa: D205,D400

from src.warmac import main as warmac

if __name__ == "__main__":
    try:
        warmac.main()
    except KeyboardInterrupt:
        # prevents errors if ctrl+c is used
        print("Exiting program.")
