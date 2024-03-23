class AEV:
    def __init__(self):
        self.telemetry = {}
        self.current_speed_mph = 0
        self.door_status = 'c'
        self.heartbeat = 0
        self.manual_control = False

    def get_telemetry(self):
        return self.telemetry
