from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
from Phidget22.PhidgetException import PhidgetException


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
        
        self.right1.setChannel(0)
        self.right2.setChannel(0)
        self.left1.setChannel(0)
        self.left2.setChannel(0)

        self.right1.openWaitForAttachment(5000)
        self.right2.openWaitForAttachment(5000)
        self.left1.openWaitForAttachment(5000)
        self.left2.openWaitForAttachment(5000)
        
        self.right1.setAcceleration(0.25)
        self.right2.setAcceleration(0.25)
        self.left1.setAcceleration(0.25)
        self.left2.setAcceleration(0.25)

    def forward(self):
        try:
            self.right1.setTargetVelocity(-0.25)
            self.right2.setTargetVelocity(-0.25)
            self.left1.setTargetVelocity(0.25)
            self.left2.setTargetVelocity(0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def forward_left(self):
        try:
            self.right1.setTargetVelocity(-0.25)
            self.right2.setTargetVelocity(-0.25)
            self.left1.setTargetVelocity(0.12)
            self.left2.setTargetVelocity(0.12)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def forward_right(self):
        try:
            self.right1.setTargetVelocity(-0.12)
            self.right2.setTargetVelocity(-0.12)
            self.left1.setTargetVelocity(0.25)
            self.left2.setTargetVelocity(0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def reverse(self):
        try:
            self.right1.setTargetVelocity(0.25)
            self.right2.setTargetVelocity(0.25)
            self.left1.setTargetVelocity(-0.25)
            self.left2.setTargetVelocity(-0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def reverse_left(self):
        try:
            self.right1.setTargetVelocity(0.25)
            self.right2.setTargetVelocity(0.25)
            self.left1.setTargetVelocity(-0.12)
            self.left2.setTargetVelocity(-0.12)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def reverse_right(self):
        try:
            self.right1.setTargetVelocity(0.12)
            self.right2.setTargetVelocity(0.12)
            self.left1.setTargetVelocity(-0.25)
            self.left2.setTargetVelocity(-0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def left(self):
        try:
            self.right1.setTargetVelocity(-0.25)
            self.right2.setTargetVelocity(-0.25)
            self.left1.setTargetVelocity(-0.25)
            self.left2.setTargetVelocity(-0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def right(self):
        try:
            self.right1.setTargetVelocity(0.25)
            self.right2.setTargetVelocity(0.25)
            self.left1.setTargetVelocity(0.25)
            self.left2.setTargetVelocity(0.25)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def stop(self):
        try:
            self.right1.setTargetVelocity(0)
            self.right2.setTargetVelocity(0)
            self.left1.setTargetVelocity(0)
            self.left2.setTargetVelocity(0)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            self.exit()

    def exit(self):
        if self.right1 is None:
            self.right1 = BLDCMotor()
            self.right1.setDeviceSerialNumber(672469)
            self.right1.setHubPort(0)
            self.right1.openWaitForAttachment(2000)
        if self.right2 is None:
            self.right2 = BLDCMotor()
            self.right2.setDeviceSerialNumber(672469)
            self.right2.setHubPort(3)
            self.right2.openWaitForAttachment(2000)
        if self.left1 is None:
            self.left1 = BLDCMotor()
            self.left1.setDeviceSerialNumber(672469)
            self.left1.setHubPort(4)
            self.left1.openWaitForAttachment(2000)
        if self.left2 is None:
            self.left2 = BLDCMotor()
            self.left2.setDeviceSerialNumber(672469)
            self.left2.setHubPort(5)
            self.left1.openWaitForAttachment(2000)
        self.right1.close()
        self.right2.close()
        self.left1.close()
        self.left2.close()
