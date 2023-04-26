from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
import time

def main():
    bldcMotorR1 = BLDCMotor()
    bldcMotorR2 = BLDCMotor()
    bldcMotorL1 = BLDCMotor()
    bldcMotorL2 = BLDCMotor()
    bldcMotorR1.setDeviceSerialNumber(672469)
    bldcMotorR2.setDeviceSerialNumber(672469)
    bldcMotorL1.setDeviceSerialNumber(672469)
    bldcMotorL2.setDeviceSerialNumber(672469)
    bldcMotorR1.setHubPort(0)
    bldcMotorR2.setHubPort(3)
    bldcMotorL1.setHubPort(4)
    bldcMotorL2.setHubPort(5)
    bldcMotorR1.openWaitForAttachment(5000)
    bldcMotorR2.openWaitForAttachment(5000)
    bldcMotorL1.openWaitForAttachment(5000)
    bldcMotorL2.openWaitForAttachment(5000)
    bldcMotorR1.setTargetVelocity(1)
    bldcMotorR2.setTargetVelocity(1)
    bldcMotorL1.setTargetVelocity(1)
    bldcMotorL2.setTargetVelocity(1)

    try:
        input('Press Enter to Stop\n')
    except (Exception, KeyboardInterrupt):
        pass

    bldcMotorR1.close()
    bldcMotorR2.close()
    bldcMotorL1.close()
    bldcMotorL2.close()

main()

