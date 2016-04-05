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


def ashex(p):
    line = ""
    for b in p:
        line += str(hex(b)) + " "
    return line


#----- HOPERF REGISTER INTERFACE ----------------------------------------------
# Precise register descriptions can be found in:
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


#----- HOPERF RADIO INTERFACE -------------------------------------------------

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
    txbuf = [ADDR_FIFO | MASK_WRITE_DATA]
    for b in buf:
      txbuf.append(b)
    #print("write FIFO %s" % ashex(txbuf))

    spi.select()
    spi.frame(txbuf)
    spi.deselect()


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


def HRF_wait_ready():
    """Wait for HRF to be ready after last command"""
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY, MASK_MODEREADY)


def HRF_wait_txready():
    """Wait for HRF to be ready and ready for tx, after last command"""
    trace("waiting for transmit ready...")
    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)
    trace("transmit ready")


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
    #trace("payload:%s" % ashex(payload))
    HRF_writefifo_burst(payload)
    trace("  waiting for sent...")
    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT)
    trace("  sent")
    reg = HRF_readreg(ADDR_IRQFLAGS2)
    trace("  irqflags2=%s" % hex(reg))
    if ((reg & MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
        warning("Failed to send payload to HRF")



#----- ENERGENIE SPECIFIC CONFIGURATIONS --------------------------------------

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
    [ADDR_SYNCCONFIG, 	      VAL_SYNCCONFIG4],		         # Size of the Sync word = 4 (SyncSize + 1)
    [ADDR_SYNCVALUE1, 	      VAL_SYNCVALUE1OOK],            # sync value 1
    [ADDR_SYNCVALUE2, 	      0],                            # sync value 2
    [ADDR_SYNCVALUE3, 	      0],                            # sync value 3
    [ADDR_SYNCVALUE4, 	      0],                            # sync value 4
    [ADDR_PACKETCONFIG1,      VAL_PACKETCONFIG1OOK],	     # Fixed length, no Manchester coding, OOK
    [ADDR_PAYLOADLEN, 	      VAL_PAYLOADLEN_OOK],	         # Payload Length
    [ADDR_FIFOTHRESH, 	      VAL_FIFOTHRESH30],             # Condition to start packet transmission: wait for 30 bytes in FIFO
]


def HRF_config(config):
    """Load a table of configuration values into HRF registers"""
    for cmd in config:
        HRF_writereg(cmd[0], cmd[1])
        HRF_wait_ready()


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


def HRF_send_OOK_payload(payload):
    """Send a payload multiple times"""

    p1 = [0x00] + payload
    # This sync pattern does not match C code, but it works.
    # The sync pattern from the C code does not work here
    # Note that buf[0] in the C is undefined due to being uninitialised
    #pn = [0x00,0x80,0x00,0x00,0x00] # from the C
    # Currently there is no explanation for this.
    pn = [0x80,0x80,0x80,0x80,0x80] + payload

    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)
    HRF_writefifo_burst(p1)
    
    for i in range(8):
        HRF_pollreg(ADDR_IRQFLAGS2, MASK_FIFOLEVEL, 0)
        HRF_writefifo_burst(pn)

    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT) # wait for Packet sent

    reg = HRF_readreg(ADDR_IRQFLAGS2)
    #trace("  irqflags2=%s" % hex(reg))
    if (reg & (MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
        warning("Failed to send repeated payload to HRF")



#----- RADIO API --------------------------------------------------------------

mode = None
modulation_fsk = None

def init():
    """Initialise the module ready for use"""
    spi.init_defaults()
    trace("RESET")

    # Note that if another program left GPIO pins in a different state
    # and did a dirty exit, the reset fails to work and the clear fifo hangs.
    # Might have to make the spi.init() set everything to inputs first,
    # then set to outputs, to make sure that the
    # GPIO registers are in a deterministic start state.
    spi.reset() # send a hardware reset to ensure radio in clean state

    HRF_clear_fifo()


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
            HRF_config(config_FSK)
            modulation_fsk = True

    elif ook != None and ook:
        if modulation_fsk == None or modulation_fsk == True:
            trace("switch to OOK")
            HRF_config(config_OOK)
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
    spi.start_transaction()
    if not modulation_fsk:
        HRF_send_OOK_payload(payload)
    else:
        HRF_send_payload(payload)
    spi.end_transaction()


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
    spi.start_transaction()
    waiting = HRF_check_payload()
    spi.end_transaction()
    return waiting


def receive():
    """Receive a single payload from the buffer using the present modulation scheme"""
    spi.start_transaction()
    payload = HRF_receive_payload()
    spi.end_transaction()
    return payload


def finished():
    """Close the library down cleanly when finished"""
    spi.finished()


# END
