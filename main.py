# a runtime file for the AEV

# author: Owen Bramley
# date modified: 03/31/2023
# version: 0.1 (alpha)

import board
import os
import api


# startup sequence
def init():
    # connect to control center via COSMOS from api.py
    api.u_status_f
    return


# shutdown sequence
def shutdown():
    os.system("shutdown now -h")
