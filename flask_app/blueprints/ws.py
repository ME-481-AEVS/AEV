import json
import time
import threading

from flask_sock import Sock
from simple_websocket import ConnectionClosed

from aev import AEV

sock = Sock()
aev = AEV()


def send_telemetry(ws: Sock, controls: bool):
    """
    Sends telemetry data from the AEV to the websocket connection. Acts as a
    heartbeat for the controls ws, when no longer connected stops all movement
    on the AEV
    """
    while True:
        time.sleep(1 if controls else 2)
        aev.update_telemetry()
        print(aev.telemetry)
        try:
            ws.send(aev.telemetry)
        except ConnectionClosed:
            if controls:
                # stop all movement on aev
                print('WS DISCONNECTED - STOPPING ALL MOVEMENT')
            break


@sock.route('/telemetry')
def echo(ws):
    #_thread = threading.Thread(target=send_telemetry, args=(ws, False))
    #_thread.daemon = True
    #_thread.start()
    aev.update_telemetry()
    while True:
        data = ws.receive()
        print(data)


@sock.route('/control')
def control(ws):
    """
    0000 0000
      CO WASD
    C: close door       32
    O: open door        16
    W: forward           8
    A: left              4
    S: backward          2
    D: right             1
    """
    #_thread = threading.Thread(target=send_telemetry, args=(ws, True))
    #_thread.daemon = True
    #_thread.start()
    while ws.connected:
        data = json.loads(ws.receive())
        print(data)
        command = 0
        if data['type'] == 'command':
            command = data['message']
        else:
            continue
        if command == 32:
            # close door
            print('CLOSING DOOR')
        elif command == 16:
            # open door
            print('OPENING DOOR')
        elif command >= 8:
            # forward
            status = 'received FORWARD'
            if command == 12:
                # left
                status += ' LEFT'
            elif command == 9:
                # right
                status += ' RIGHT'
            else:
                # just forward
                pass
            aev.forward()
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
            aev.stop()
            print('received STOPPING')

