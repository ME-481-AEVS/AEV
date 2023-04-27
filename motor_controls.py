from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *


class MotorControl:
    def __init__(self):
        self.right1 = BLDCMotor()
        self.right2 = BLDCMotor()
        self.left1 = BLDCMotor()
        self.left2 = BLDCMotor()

        self.right1.setDeviceSerialNumber(672469)
        self.right2.setDeviceSerialNumber(672469)
        self.left1.setDeviceSerialNumber(672469)
        self.left2.setDeviceSerialNumber(672469)

        self.right1.setHubPort(0)
        self.right2.setHubPort(3)
        self.left1.setHubPort(4)
        self.left2.setHubPort(5)

        self.right1.openWaitForAttachment(5000)
        self.right2.openWaitForAttachment(5000)
        self.left1.openWaitForAttachment(5000)
        self.left2.openWaitForAttachment(5000)

    def forward(self):
        self.right1.setTargetVelocity(1)
        self.right2.setTargetVelocity(1)
        self.left1.setTargetVelocity(1)
        self.left2.setTargetVelocity(1)

    def reverse(self):
        # will this work?
        self.right1.setTargetVelocity(-1)
        self.right2.setTargetVelocity(-1)
        self.left1.setTargetVelocity(-1)
        self.left2.setTargetVelocity(-1)

    def stop(self):
        self.right1.setTargetVelocity(0)
        self.right2.setTargetVelocity(0)
        self.left1.setTargetVelocity(0)
        self.left2.setTargetVelocity(0)

    def exit(self):
        self.right1.close()
        self.right2.close()
        self.left1.close()
        self.left2.close()