#!/usr/bin/env python
"""
Allows for program execution without calling python3
Detailed program introduction found in main.py
Formal documentation WIP
"""

from WarMAC import main
if __name__ == "__main__":
    try:
        main.main()
    except KeyboardInterrupt:
        #prevents errors if ctrl+c is used
        print("Exiting program.")
