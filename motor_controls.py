from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
import time

def main():
    bldcMotor0 = BLDCMotor()
    bldcMotor0.setDeviceSerialNumber(672469)
    bldcMotor0.openWaitForAttachment(5000)
    bldcMotor0.setTargetVelocity(0.5)

    try:
        input('Press Enter to Stop\n')
    except (Exception, KeyboardInterrupt):
        pass

    bldcMotor0.close()

main()

