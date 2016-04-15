# crypto.py  27/09/2015  D.J.Whale
#
# Crypto engine for OpenThings, including crc calculation



ran = None

#static uint16_t ran;

#void seed(uint8_t pid, uint16_t pip)
#{
#	ran = ((((uint16_t) pid) << 8) ^ pip);
#}


def init(pid, pip):
    """Initialise the crypto engine state variables"""
    global ran
    ran = (((pid&0xFF)<<8) ^ pip) & 0xFFFF # maintain U16


#uint8_t crypt(uint8_t dat)
#{
#	unsigned char i; //(u8)

#	for (i = 0; i < 5; ++i)
#	{
#		ran = (ran & 1) ? ((ran >> 1) ^ 62965U) : (ran >> 1);
#	}
#	return (uint8_t)(ran ^ dat ^ 90U);
#}

def cryptByte(data):
    """crypt a byte of data and update the crypto engine state variable"""
    global ran
    for i in range(5):
        if (ran&0x01) != 0: # bit0
            # bit0 set
            ran = ((ran>>1) ^ 62965) & 0xFFFF # maintain U16
        else:
            # bit0 clear
            ran = ran >> 1

    return (ran ^ data ^ 90) & 0xFF


def cryptPayload(payload, start, length):
    """Encrypt a range of bytes in place by modifying those payload bytes"""
    for i in range(start, start+length):
        payload[i] = cryptByte(payload[i])

# END
