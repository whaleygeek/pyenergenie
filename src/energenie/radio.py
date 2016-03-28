# test1.py  26/09/2015  D.J.Whale
#
# Simple low level test of the HopeRF interface
# Uses direct SPI commands to exercise the interface.
#
# Receives and dumps payload buffers.
#
# Eventually a lot of this will be pushed into a separate module,
# and then pushed back into C once it is proved working.

import spi

def warning(msg):
    print("warning:" + str(msg))

def trace(msg):
    print(str(msg))


#----- REGISTER ACCESS --------------------------------------------------------

def HRF_writereg(addr, data):
    """Write an 8 bit value to a register"""
    buf = [addr | MASK_WRITE_DATA, data]
    spi.select()
    spi.frame(buf)
    spi.deselect()


def HRF_readreg(addr):
    """Read an 8 bit value from a register"""
    buf = [addr, 0x00]
    spi.select()
    res = spi.frame(buf)
    spi.deselect()
    #print(hex(res[1]))
    return res[1] # all registers are 8 bit


def HRF_writefifo_burst(buf):
    """Write all bytes in buf to the payload FIFO, in a single burst"""
    # Don't modify buf, in case caller reuses it
    #txbuf = [ADDR_FIFO | MASK_WRITE_DATA]
    #for b in buf:
    #  txbuf.append(b)
    #print("write FIFO %s" % ashex(txbuf))

    # This is buggy as it modifies user buffer, but it works at present
    spi.select()
    buf.insert(0, ADDR_FIFO | MASK_WRITE_DATA)
    spi.frame(buf)
    spi.deselect()
    print("written: %s" % ashex(buf))

def ashex(buf):
    result = []
    for b in buf:
        result.append(hex(b))
    return result


def HRF_readfifo_burst():
    """Read bytes from the payload FIFO using burst read"""
    #first byte read is the length in remaining bytes
    buf = []
    spi.select()
    spi.frame([ADDR_FIFO])
    count = 1 # read at least the length byte
    while count > 0:
        rx = spi.frame([ADDR_FIFO])
        data = rx[0]
        if len(buf) == 0:
            count = data
        else:
            count -= 1
        buf.append(data)
    spi.deselect()
    trace("readfifo:" + str(ashex(buf)))
    return buf


def HRF_checkreg(addr, mask, value):
    """Check to see if a register matches a specific value or not"""
    regval = HRF_readreg(addr)
    #print("addr %d mask %d wanted %d actual %d" % (addr,mask,value,regval))
    return (regval & mask) == value


def HRF_pollreg(addr, mask, value):
    """Poll a register until it meet some criteria"""
    while not HRF_checkreg(addr, mask, value):
        pass


#----- HRF REGISTER PROTOCOL --------------------------------------------------

# HopeRF register addresses
# Precise register descriptions can be found on: 
# www.hoperf.com/upload/rf/RFM69W-V1.3.pdf
# on page 63 - 74

ADDR_FIFO                   = 0x00
ADDR_OPMODE                 = 0x01
ADDR_REGDATAMODUL           = 0x02
ADDR_BITRATEMSB             = 0x03
ADDR_BITRATELSB             = 0x04
ADDR_FDEVMSB                = 0x05
ADDR_FDEVLSB                = 0x06
ADDR_FRMSB                  = 0x07
ADDR_FRMID                  = 0x08
ADDR_FRLSB                  = 0x09
ADDR_AFCCTRL                = 0x0B
ADDR_LNA                    = 0x18
ADDR_RXBW                   = 0x19
ADDR_AFCFEI                 = 0x1E
ADDR_IRQFLAGS1              = 0x27
ADDR_IRQFLAGS2              = 0x28
ADDR_RSSITHRESH             = 0x29
ADDR_PREAMBLELSB            = 0x2D
ADDR_SYNCCONFIG             = 0x2E
ADDR_SYNCVALUE1             = 0x2F
ADDR_SYNCVALUE2             = 0x30
ADDR_SYNCVALUE3             = 0x31
ADDR_SYNCVALUE4             = 0x32
ADDR_PACKETCONFIG1          = 0x37
ADDR_PAYLOADLEN             = 0x38
ADDR_NODEADDRESS            = 0x39
ADDR_FIFOTHRESH             = 0x3C

# HopeRF masks to set and clear bits
MASK_REGDATAMODUL_OOK       = 0x08
MASK_REGDATAMODUL_FSK       = 0x00
MASK_WRITE_DATA             = 0x80
MASK_MODEREADY              = 0x80
MASK_FIFONOTEMPTY           = 0x40
MASK_FIFOLEVEL              = 0x20
MASK_FIFOOVERRUN            = 0x10
MASK_PACKETSENT             = 0x08
MASK_TXREADY                = 0x20
MASK_PACKETMODE             = 0x60
MASK_MODULATION             = 0x18
MASK_PAYLOADRDY             = 0x04

MODE_STANDBY                = 0x04	# Standby
MODE_TRANSMITER             = 0x0C	# Transmiter
MODE_RECEIVER               = 0x10	# Receiver
VAL_REGDATAMODUL_FSK        = 0x00	# Modulation scheme FSK
VAL_REGDATAMODUL_OOK        = 0x08	# Modulation scheme OOK
VAL_FDEVMSB30               = 0x01	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
VAL_FDEVLSB30               = 0xEC	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
VAL_FRMSB434                = 0x6C	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRMID434                = 0x93	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRLSB434                = 0x33	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRMSB433                = 0x6C	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_FRMID433                = 0x7A	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_FRLSB433                = 0xE1	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_AFCCTRLS                = 0x00	# standard AFC routine
VAL_AFCCTRLI                = 0x20	# improved AFC routine
VAL_LNA50                   = 0x08	# LNA input impedance 50 ohms
VAL_LNA50G                  = 0x0E	# LNA input impedance 50 ohms, LNA gain -> 48db
VAL_LNA200                  = 0x88	# LNA input impedance 200 ohms
VAL_RXBW60                  = 0x43	# channel filter bandwidth 10kHz -> 60kHz  page:26
VAL_RXBW120                 = 0x41	# channel filter bandwidth 120kHz
VAL_AFCFEIRX                = 0x04	# AFC is performed each time RX mode is entered
VAL_RSSITHRESH220           = 0xDC	# RSSI threshold 0xE4 -> 0xDC (220)
VAL_PREAMBLELSB3            = 0x03	# preamble size LSB 3
VAL_PREAMBLELSB5            = 0x05	# preamble size LSB 5
VAL_SYNCCONFIG2             = 0x88	# Size of the Synch word = 2 (SyncSize + 1)
VAL_SYNCCONFIG4             = 0x98	# Size of the Synch word = 4 (SyncSize + 1)
VAL_SYNCVALUE1FSK           = 0x2D	# 1st byte of Sync word
VAL_SYNCVALUE2FSK           = 0xD4	# 2nd byte of Sync word
VAL_SYNCVALUE1OOK           = 0x80	# 1nd byte of Sync word
VAL_PACKETCONFIG1FSK        = 0xA2	# Variable length, Manchester coding, Addr must match NodeAddress
VAL_PACKETCONFIG1FSKNO      = 0xA0	# Variable length, Manchester coding
VAL_PACKETCONFIG1OOK        = 0		# Fixed length, no Manchester coding
VAL_PAYLOADLEN255           = 0xFF	# max Length in RX, not used in Tx
VAL_PAYLOADLEN66            = 66	# max Length in RX, not used in Tx
VAL_PAYLOADLEN_OOK          = (13 + 8 * 17)	# Payload Length
VAL_NODEADDRESS01           = 0x01	# Node address used in address filtering
VAL_NODEADDRESS04           = 0x04	# Node address used in address filtering
VAL_FIFOTHRESH1             = 0x81	# Condition to start packet transmission: at least one byte in FIFO
VAL_FIFOTHRESH30            = 0x1E	# Condition to start packet transmission: wait for 30 bytes in FIFO


#----- CONFIGURATION TABLES ------------------------------------------------------------

config_FSK = [
    [ADDR_REGDATAMODUL,       VAL_REGDATAMODUL_FSK],         # modulation scheme FSK
    [ADDR_FDEVMSB,            VAL_FDEVMSB30],                # frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
    [ADDR_FDEVLSB,            VAL_FDEVLSB30],                # frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
    [ADDR_FRMSB,              VAL_FRMSB434],                 # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_FRMID,              VAL_FRMID434],                 # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_FRLSB,              VAL_FRLSB434],                 # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_AFCCTRL,            VAL_AFCCTRLS],                 # standard AFC routine
    [ADDR_LNA,                VAL_LNA50],                    # 200ohms, gain by AGC loop -> 50ohms
    [ADDR_RXBW,               VAL_RXBW60],                   # channel filter bandwidth 10kHz -> 60kHz  page:26
    [ADDR_BITRATEMSB,         0x1A],                         # 4800b/s
    [ADDR_BITRATELSB,         0x0B],                         # 4800b/s
    #[ADDR_AFCFEI,             VAL_AFCFEIRX],                 # AFC is performed each time rx mode is entered
    #[ADDR_RSSITHRESH,         VAL_RSSITHRESH220],            # RSSI threshold 0xE4 -> 0xDC (220)
    #[ADDR_PREAMBLELSB,        VAL_PREAMBLELSB5],             # preamble size LSB set to 5
    [ADDR_SYNCCONFIG,         VAL_SYNCCONFIG2],              # Size of the Synch word = 2 (SyncSize + 1)
    [ADDR_SYNCVALUE1,         VAL_SYNCVALUE1FSK],            # 1st byte of Sync word
    [ADDR_SYNCVALUE2,         VAL_SYNCVALUE2FSK],            # 2nd byte of Sync word
    #[ADDR_PACKETCONFIG1,     VAL_PACKETCONFIG1FSK],          # Variable length, Manchester coding, Addr must match NodeAddress
    [ADDR_PACKETCONFIG1,      VAL_PACKETCONFIG1FSKNO],       # Variable length, Manchester coding
    [ADDR_PAYLOADLEN,         VAL_PAYLOADLEN66],             # max Length in RX, not used in Tx
    #[ADDR_NODEADDRESS,       VAL_NODEADDRESS01],            # Node address used in address filtering
    [ADDR_NODEADDRESS,        0x06],                         # Node address used in address filtering
    [ADDR_FIFOTHRESH,         VAL_FIFOTHRESH1],              # Condition to start packet transmission: at least one byte in FIFO
    [ADDR_OPMODE,             MODE_RECEIVER]                 # Operating mode to Receiver
]

config_OOK = [
    [ADDR_REGDATAMODUL,       VAL_REGDATAMODUL_OOK],	     # modulation scheme OOK
    [ADDR_FDEVMSB,            0],                            # frequency deviation -> 0kHz
    [ADDR_FDEVLSB,            0],                            # frequency deviation -> 0kHz
    [ADDR_FRMSB,              VAL_FRMSB433],                 # carrier freq -> 433.92MHz 0x6C7AE1
    [ADDR_FRMID,              VAL_FRMID433],                 # carrier freq -> 433.92MHz 0x6C7AE1
    [ADDR_FRLSB,              VAL_FRLSB433],                 # carrier freq -> 433.92MHz 0x6C7AE1
    [ADDR_RXBW,               VAL_RXBW120],                  # channel filter bandwidth 120kHz
    [ADDR_BITRATEMSB, 	      0x40],                         # 1938b/s
    [ADDR_BITRATELSB,         0x80],                         # 1938b/s
    [ADDR_PREAMBLELSB, 	      0],                            # preamble size LSB 3
    [ADDR_SYNCCONFIG, 	      VAL_SYNCCONFIG4],		     # Size of the Sync word = 4 (SyncSize + 1)
    [ADDR_SYNCVALUE1, 	      VAL_SYNCVALUE1OOK],            # sync value 1
    [ADDR_SYNCVALUE2, 	      0],                            # sync value 2
    [ADDR_SYNCVALUE3, 	      0],                            # sync value 3
    [ADDR_SYNCVALUE4, 	      0],                            # sync value 4
    [ADDR_PACKETCONFIG1,      VAL_PACKETCONFIG1OOK],	     # Fixed length, no Manchester coding, OOK
    [ADDR_PAYLOADLEN, 	      VAL_PAYLOADLEN_OOK],	     # Payload Length
    [ADDR_FIFOTHRESH, 	      VAL_FIFOTHRESH30],             # Condition to start packet transmission: wait for 30 bytes in FIFO
]


def HRF_wait_ready():
    """Wait for HRF to be ready after last command"""
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY, MASK_MODEREADY)


def HRF_wait_txready():
    """Wait for HRF to be ready and ready for tx, after last command"""
    trace("waiting for transmit ready...")
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)
    trace("transmit ready")


def HRF_config_FSK():
    """Configure HRF for FSK modulation"""
    for cmd in config_FSK:
        HRF_writereg(cmd[0], cmd[1])
        HRF_wait_ready()


def HRF_config_OOK():
    """Configure HRF for OOK modulation"""
    for cmd in config_OOK:
        HRF_writereg(cmd[0], cmd[1])
        HRF_wait_ready()


def HRF_change_mode(mode):
    HRF_writereg(ADDR_OPMODE, mode)


def HRF_clear_fifo():
    """Clear any data in the HRF payload FIFO by reading until empty"""
    while (HRF_readreg(ADDR_IRQFLAGS2) & MASK_FIFONOTEMPTY) == MASK_FIFONOTEMPTY:
        HRF_readreg(ADDR_FIFO)


def HRF_check_payload():
    """Check if there is a payload in the FIFO waiting to be processed"""
    irqflags1 = HRF_readreg(ADDR_IRQFLAGS1)
    irqflags2 = HRF_readreg(ADDR_IRQFLAGS2)
    #trace("irq1 %s   irq2 %s" % (hex(irqflags1), hex(irqflags2)))

    return (irqflags2 & MASK_PAYLOADRDY) == MASK_PAYLOADRDY


def HRF_receive_payload():
    """Receive the whole payload"""
    return HRF_readfifo_burst()


def HRF_send_payload(payload):
    trace("send_payload")
    #dumpPayloadAsHex(payload)
    HRF_writefifo_burst(payload)
    trace("  waiting for sent...")
    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT)
    trace("  sent")
    reg = HRF_readreg(ADDR_IRQFLAGS2)
    trace("  irqflags2=%s" % hex(reg))
    if ((reg & MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
        warning("Failed to send payload to HRF")


def ashex(p):
    line = ""
    for b in p:
        line += str(hex(b)) + " "
    return line


def dumpPayloadAsHex(payload):
    length = payload[0]
    print(hex(length))
    if length+1 != len(payload):
        print("warning length byte mismatch actual:%d inbuf:%d" % (len(payload), length))

    for i in range(1,length+1):
        print("[%d] = %s" % (i, hex(payload[i])))

#ORIGINAL C CODE
#void HRF_send_OOK_msg(uint8_t relayState)
#{
#	uint8_t buf[17];
#	uint8_t i;
#
#	HRF_config_OOK();
#
#	buf[1] = 0x80;										// Preambule 32b enclosed in sync words
#	buf[2] = 0x00;
#	buf[3] = 0x00;
#	buf[4] = 0x00;
#
#	for (i = 5; i <= 14; ++i){
#		buf[i] = 8 + (i&1) * 6 + 128 + (i&2) * 48;		// address 20b * 4 = 10 Bytes
#	}
#
#	if (relayState == 1)
#	{
#		printf("relay ON\n\n");
#		buf[15] = 0xEE;		// D0-high, D1-h		// S1 on
#		buf[16] = 0xEE;		// D2-h, D3-h
#	}
#	else
#	{
#		printf("relay OFF\n\n");
#		buf[15] = 0xEE;		// D0-high, D1-h		// S1 off
#		buf[16] = 0xE8;		// D2-h, D3-l
#	}
#
#	HRF_wait_for (ADDR_IRQFLAGS1, MASK_MODEREADY | MASK_TXREADY, true);		// wait for ModeReady + TX ready
#	HRF_reg_Wn(buf + 4, 0, 12);						// don't include sync word (4 bytes) into data buffer
#
#	for (i = 0; i < 8; ++i)							// Send the same message few more times
#	{
#		HRF_wait_for(ADDR_IRQFLAGS2, MASK_FIFOLEVEL, false);
#		HRF_reg_Wn(buf, 0, 16);						// with sync word
#	}
#
#	HRF_wait_for (ADDR_IRQFLAGS2, MASK_PACKETSENT, true);		// wait for Packet sent
#	HRF_assert_reg_val(ADDR_IRQFLAGS2, MASK_FIFONOTEMPTY | MASK_FIFOOVERRUN, false, "are all bytes sent?");
#	HRF_config_FSK();
#	HRF_wait_for (ADDR_IRQFLAGS1, MASK_MODEREADY, true);		// wait for ModeReady
#}

def OLD_build_OOK_relay_msg(relayState=False):
    """Temporary test code to prove we can turn the relay on or off"""
    #This code does not live in this module, it lives in an EnergenieLegacy codec module
    #also there are 4 switches, so should pass in up to 4 relayState values

    # This generates a 20*4 bit address i.e. 10 bytes
    # The number generated is always the same
    # Presumably this is the 'Energenie address prefix'
    # The switch number is encoded in the payload
    # This code looks screwy, but it is correct compared to the C code.
    # It's probably doing bit encoding on the fly, manchester or sync bits or something.
    # Wait until we get the OOK spec from Energenie to better document this.

    # Looks like: 0000 00BA gets encoded as:
    # 128 64 32 16  8  4  2  1
    #   1  B  B  0  1  A  A  0

    #payload = []
    #for i in range(10):
    #    j = i + 5
    #    payload.append(8 + (j&1) * 6 + 128 + (j&2) * 48)
    #dumpPayloadAsHex(payload)
    #
    #          5     6     7     8     9     10    11    12    13    14
    #          1(01) 1(10) 1(11) 0(00) 0(01) 0(10) 0(11) 1(00) 1(01) 1(10)
    payload = [0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8]

    if relayState: # ON
        # D0=high, D1=high, D2-high, D3=high (S1 on)
        # 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
        #   1  0  B  B  1  A  A  0          1  0  B  B  1  A  A  0
        #   1  1  1  0  1  1  1  0          1  1  1  0  1  1  1  0   = 10 11 10 11
        payload += [0xEE, 0xEE]
    else: # OFF
        # D0=high, D1=high, D2=high, D3=low (S1 off)
        # 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
        #   1  0  B  B  1  A  A  0          1  0  B  B  1  A  A  0
        #   1  1  1  0  1  1  1  0          1  1  1  0  1  0  0  0   = 10 11 10 00
        payload += [0xEE, 0xE8]

    return payload


def OLD_send_payload_repeat(payload):
    """Send a payload multiple times"""

    # 32 bits enclosed in sync words
    #print("waiting for mode and tx ready")
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)

    #write first payload without sync preamble
    HRF_writefifo_burst(payload)

    # preceed all future payloads with a sync-word preamble
    preamble = [0x00,0x80,0x00,0x00,0x00]
    preamble_payload = preamble + payload
    # Note, payload length configured in OOK table is based on this
    for i in range(8): # Repeat the message a number of times
        #print("waiting for fifo empty")
        HRF_pollreg(ADDR_IRQFLAGS2, MASK_FIFOLEVEL, 0)
        HRF_writefifo_burst(preamble_payload)

    #print("waiting for fifo empty")
    HRF_pollreg(ADDR_IRQFLAGS2, MASK_FIFOLEVEL, 0)
    #print("waiting for packet sent")
    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT) # wait for Packet sent

    reg = HRF_readreg(ADDR_IRQFLAGS2)
    trace("  irqflags2=%s" % hex(reg))
    if (reg & (MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
        warning("Failed to send repeated payload to HRF")



def HRF_send_OOK_payload_repeat(payload, times=0):
    """Send a payload multiple times"""
    print("@@@@@ send OOK repeated")
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)

    # A payload is 32 bits enclosed in sync words
    # write first payload without sync preamble
    # 4   5   6   7   8   9   10   11   12   13   14
    # ..  01  10  11  00  01  10   11   00   01   10
    # 00  8E  E8  EE  88  8E  E8   EE   88   8E   E8
    
    payload = [0x8E,0xE8,0xEE,0x88,0x8E,0xE8,0xEE,0x88,0x8E,0xE8]
    # bits are labeled back to front in C code! D0 D1 D2 D3
    allon   = [0xEE, 0xEE]
    alloff  = [0xEE, 0xE8]
    payload += allon

    ##payload.insert(0, 0x00) # first byte should be all zeros (TODO add to payload builder)
    #print("send %s" % ashex(payload))
    HRF_writefifo_burst(payload)

    # preceed all future payloads with a sync-word preamble
    if times > 0:
        SYNC_PREAMBLE = [0x00,0x80,0x00,0x00,0x00]
        preamble_payload = SYNC_PREAMBLE + payload
        for i in range(times): # Repeat the message a number of times
            HRF_pollreg(ADDR_IRQFLAGS2, MASK_FIFOLEVEL, 0)
            #print("send %s" % ashex(preamble_payload))
            HRF_writefifo_burst(preamble_payload)

    #TODO: this might be unreliable, as the IRQ might fire on any single packet
    #need to check how big the FIFO is, and just build a single payload and burst load it
    #especially as Python will be slower loading the FIFO than the original C was.
    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT) # wait for Packet sent

    reg = HRF_readreg(ADDR_IRQFLAGS2)
    trace("  irqflags2=%s" % hex(reg))
    if (reg & (MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
        warning("Failed to send repeated OOK payload to HRF")



#----- USER API ---------------------------------------------------------------
#
# This is only a first-pass at a user API.
# it might change quite a bit in the second pass.
# The HRF functions are intentionally not used by the caller,
# this allows mock testing, and also for that part to be rewritten in C
# for speed later if required.

mode = None
modulation_fsk = None

def init():
    """Initialise the module ready for use"""
    spi.init_defaults()
    trace("RESET")
    spi.reset() # send a hardware reset to ensure radio in clean state

    trace("config FSK")
    HRF_config_FSK()
    HRF_clear_fifo()
    receiver()


def modulation(fsk=None, ook=None):
    """Switch modulation, if needed"""
    global modulation_fsk

    # Handle sensible module defaults for earlier versions of user code
    if fsk == None and ook == None:
        # Force FSK mode
        fsk = True

    if fsk != None and fsk:
        if modulation_fsk == None or modulation_fsk == False:
            trace("switch to FSK")
            HRF_config_FSK()
            modulation_fsk = True

    elif ook != None and ook:
        if modulation_fsk == None or modulation_fsk == True:
            trace("switch to OOK")
            HRF_config_OOK()
            modulation_fsk = False


def transmitter(fsk=None, ook=None):
    """Change into transmitter mode"""
    global mode

    trace("transmitter mode")
    modulation(fsk, ook)
    HRF_change_mode(MODE_TRANSMITER)
    mode = "TRANSMITTER"
    HRF_wait_txready()


def transmit(payload):
    """Transmit a single payload using the present modulation scheme"""
    if not modulation_fsk:
        HRF_send_OOK_payload_repeat(payload, times=8)
    else:
        HRF_send_payload(payload)


def receiver(fsk=None, ook=None):
    """Change into receiver mode"""
    global mode

    trace("receiver mode")
    modulation(fsk, ook)
    HRF_change_mode(MODE_RECEIVER)
    HRF_wait_ready()
    mode = "RECEIVER"


def isReceiveWaiting():
    """Check to see if a payload is waiting in the receive buffer"""
    return HRF_check_payload()


def receive():
    """Receive a single payload from the buffer using the present modulation scheme"""
    return HRF_receive_payload()


def finished():
    """Close the library down cleanly when finished"""
    spi.finished()


# END
