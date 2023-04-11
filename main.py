# a runtime file for the AEV

# author: Owen Bramley
# date modified: 04/10/2023
# version: 0.1 (alpha)


import os
import api
import sensors


# startup sequence
def init():
    # connect to control center via COSMOS from api.py
    api.u_status_f
    return


# shutdown sequence
def shutdown():
    os.system("shutdown now -h")


def alpha_demo():
    """ Demo for alpha - flash warning lights """
    sensors.lights(1)


def linear_actuators():
    """ Demo for alpha - linear actuators """
    pass
