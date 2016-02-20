import argparse
from energenie import OpenHEMS, Devices
from energenie import radio

SWITCH_MESSAGE = {
    "header": {
        "mfrid":       Devices.MFRID,
        "productid":   Devices.PRODUCTID_R1_MONITOR_AND_CONTROL,
        "encryptPIP":  Devices.CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      True,
            "paramid": OpenHEMS.PARAM_SWITCH_STATE,
            "typeid":  OpenHEMS.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        }
    ]
}

def change_switch_state(switch, state):
    request = OpenHEMS.alterMessage(SWITCH_MESSAGE,
                                    header_sensorid=switch,
                                    recs_0_value=state)

    try:
        radio.init()
        OpenHEMS.init(Devices.CRYPT_PID)

        command = OpenHEMS.encode(request)

        radio.transmitter()
        radio.transmit(command)

        radio.receiver()
        if radio.isReceiveWaiting():
            print("Receiving response.")
            payload = radio.receive()
            try:
                decoded = OpenHEMS.decode(payload)
                OpenHEMS.showMessage(decoded)
            except OpenHEMS.OpenHEMSException as DecodeError:
                print("Can't decode payload: " + str(DecodeError))
        else:
            print("No message waiting.")
    except UnexpectedError:
        print("Unexpected error: " + str(UnexpectedError))
    finally:
        radio.finished()


def main():
    """Switches a plug on or off."""
    parser = argparse.ArgumentParser(description='Switches a plug on or off.')
    parser.add_argument('--name', nargs=1, required=True,
                        help='the name of the switch to act upon')
    parser.add_argument('--action', nargs=1, required=True,
                        choices=['on', 'off'], help='turns the switch on')

    args = parser.parse_args()
    state = 0
    if args.action[0] == 'on':
        state = 1
    name = args.name[0]
    value = int(name, base=16)

    change_switch_state(value, state)

if __name__ == "__main__":
    # execute only if run as a script
    main()
