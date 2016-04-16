# test_encoder.py  27/03/2016  D.J.Whale
#
# Test the OOK message encoder

import encoder

def ashex(data):
    if type(data) == list:
        line = ""
        for b in data:
            line += str(hex(b)) + " "
        return line
    else:
        return str(hex(data))


#----- TEST APPLICATION -------------------------------------------------------

print("*" * 80)

ALL_ON         = encoder.build_switch_msg(True)
ALL_OFF        = encoder.build_switch_msg(False)
ONE_ON         = encoder.build_switch_msg(True, device_address=1)
ONE_OFF        = encoder.build_switch_msg(False, device_address=1)
TWO_ON         = encoder.build_switch_msg(True, device_address=2)
TWO_OFF        = encoder.build_switch_msg(False, device_address=2)
THREE_ON       = encoder.build_switch_msg(True, device_address=3)
THREE_OFF      = encoder.build_switch_msg(False, device_address=3)
FOUR_ON        = encoder.build_switch_msg(True, device_address=4)
FOUR_OFF       = encoder.build_switch_msg(False, device_address=4)
MYHOUSE_ALL_ON = encoder.build_switch_msg(True, house_address=0x12345)

tests = [ALL_ON, ALL_OFF, ONE_ON, ONE_OFF, TWO_ON, TWO_OFF, THREE_ON, THREE_OFF, FOUR_ON, FOUR_OFF, MYHOUSE_ALL_ON]

for t in tests:
    print('')
    print(ashex(t))

# END


