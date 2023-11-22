import json
import time

from flask_sock import Sock

from aev import AEV


sock = Sock()
aev = AEV()


@sock.route('/telemetry')
def echo(ws):
    data = ws.receive()
    print(data)
    while True:
        aev.update_telemetry()
        ws.send(aev.telemetry)
        print('sending telemetry')
        time.sleep(2)


@sock.route('/control')
def control(ws):
    """
    0000 0000
     ECO WASD
    E: emergency stop   64
    C: close door       32
    O: open door        16
    W: forward           8
    A: left              4
    S: backward          2
    D: right             1
    """
    while True:
        data = json.loads(ws.receive())
        print(data)
        command = 0
        if data['type'] == 'command':
            command = data['message']
        else:
            continue
        if command >= 64:
            # emergency stop
            print('EMERGENCY STOP')
        elif command == 32:
            # close door
            print('CLOSING DOOR')
        elif command == 16:
            # open door
            print('OPENING DOOR')
        elif command >= 8:
            # forward
            status = 'MOVING FORWARD'
            if command == 12:
                # left
                status += ' LEFT'
            elif command == 9:
                # right
                status += ' RIGHT'
            else:
                # just forward
                pass
            print(status)
        elif command == 4:
            # left
            print('TURNING LEFT')
        elif command == 1:
            # right
            print('TURNING RIGHT')
        elif command >= 2:
            # backward
            status = 'MOVING BACKWARD'
            if command == 6:
                # left
                status += ' LEFT'
            elif command == 3:
                # right
                status += ' RIGHT'
            else:
                # just back
                pass
            print(status)
        else:
            print('STOPPING')
    print('DISCONNECTED')

