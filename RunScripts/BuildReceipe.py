#!/usr/bin/env python3

#-------------------------------------------------------------------------------------------#
# Description: Script which build user receipe and store on disc
# Author:<name>
#-------------------------------------------------------------------------------------------#

# libraries
import sys
from TestApp import ReceipeMngr

receipeMngr = ReceipeMngr()  # init manager

# Build user defined receipe
if receipeMngr.Build():

    # Store receipe on disk in JSON/XML
    receipeMngr.Store()

    print("Build success")
else:
    print("Build failed")
