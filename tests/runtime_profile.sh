#!/usr/bin/env bash

# This script is not meant to supply a standardized runtime-measuring process.
# The data obtained using viztracer should be used to get a general breakdown of WarMAC's execution.

# The three main parts to be looked at when examining this data are:
# 1. The overhead execution of Python starting up, importing modules, and compiling files
# 2. The amount of time it takes for WarMAC to request and receive information from warframe.market
# 3a. The amount of time it takes for WarMAC to parse the CLI arguments (done before the HTTP request).
# 3b. The amount of time it takes for WarMAC to filter the data and complete its calculations.
# 3c. The amount of time it takes for WarMAC to output its result.

python -m viztracer -o ./tests/profile.json -- warmac average -mv "vengeful revenant"
vizviewer ./tests/profile.json
