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
    spi.select()
    buf.insert(0, ADDR_FIFO | MASK_WRITE_DATA)
    spi.frame(buf)
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
    trace("readfifo:" + str(buf))
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
# Precise register description can be found on: 
# www.hoperf.com/upload/rf/RFM69W-V1.3.pdf
# on page 63 - 74

ADDR_FIFO			= 0x00
ADDR_OPMODE			= 0x01
ADDR_REGDATAMODUL	= 0x02
ADDR_BITRATEMSB		= 0x03
ADDR_BITRATELSB		= 0x04
ADDR_FDEVMSB		= 0x05
ADDR_FDEVLSB		= 0x06
ADDR_FRMSB			= 0x07
ADDR_FRMID			= 0x08
ADDR_FRLSB			= 0x09
ADDR_AFCCTRL		= 0x0B
ADDR_LNA			= 0x18
ADDR_RXBW			= 0x19
ADDR_AFCFEI			= 0x1E
ADDR_IRQFLAGS1		= 0x27
ADDR_IRQFLAGS2		= 0x28
ADDR_RSSITHRESH		= 0x29
ADDR_PREAMBLELSB	= 0x2D
ADDR_SYNCCONFIG		= 0x2E
ADDR_SYNCVALUE1		= 0x2F
ADDR_SYNCVALUE2		= 0x30
ADDR_SYNCVALUE3		= 0x31
ADDR_SYNCVALUE4		= 0x32
ADDR_PACKETCONFIG1	= 0x37
ADDR_PAYLOADLEN		= 0x38
ADDR_NODEADDRESS	= 0x39
ADDR_FIFOTHRESH		= 0x3C

# HopeRF masks to set and clear bits
MASK_REGDATAMODUL_OOK	= 0x08
MASK_REGDATAMODUL_FSK	= 0x00
MASK_WRITE_DATA		    = 0x80
MASK_MODEREADY		    = 0x80
MASK_FIFONOTEMPTY	    = 0x40
MASK_FIFOLEVEL		    = 0x20
MASK_FIFOOVERRUN	    = 0x10
MASK_PACKETSENT		    = 0x08
MASK_TXREADY		    = 0x20
MASK_PACKETMODE		    = 0x60
MASK_MODULATION		    = 0x18
MASK_PAYLOADRDY		    = 0x04

MODE_STANDBY 			= 0x04	# Standby
MODE_TRANSMITER 		= 0x0C	# Transmiter
MODE_RECEIVER 			= 0x10	# Receiver
VAL_REGDATAMODUL_FSK	= 0x00	# Modulation scheme FSK
VAL_REGDATAMODUL_OOK	= 0x08	# Modulation scheme OOK
VAL_FDEVMSB30			= 0x01	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
VAL_FDEVLSB30			= 0xEC	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
VAL_FRMSB434			= 0x6C	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRMID434			= 0x93	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRLSB434			= 0x33	# carrier freq -> 434.3MHz 0x6C9333
VAL_FRMSB433			= 0x6C	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_FRMID433			= 0x7A	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_FRLSB433			= 0xE1	# carrier freq -> 433.92MHz 0x6C7AE1
VAL_AFCCTRLS			= 0x00	# standard AFC routine
VAL_AFCCTRLI			= 0x20	# improved AFC routine
VAL_LNA50				= 0x08	# LNA input impedance 50 ohms
VAL_LNA50G				= 0x0E	# LNA input impedance 50 ohms, LNA gain -> 48db
VAL_LNA200				= 0x88	# LNA input impedance 200 ohms
VAL_RXBW60				= 0x43	# channel filter bandwidth 10kHz -> 60kHz  page:26
VAL_RXBW120				= 0x41	# channel filter bandwidth 120kHz
VAL_AFCFEIRX			= 0x04	# AFC is performed each time RX mode is entered
VAL_RSSITHRESH220		= 0xDC	# RSSI threshold 0xE4 -> 0xDC (220)
VAL_PREAMBLELSB3		= 0x03	# preamble size LSB 3
VAL_PREAMBLELSB5		= 0x05	# preamble size LSB 5
VAL_SYNCCONFIG2			= 0x88	# Size of the Synch word = 2 (SyncSize + 1)
VAL_SYNCCONFIG4			= 0x98	# Size of the Synch word = 4 (SyncSize + 1)
VAL_SYNCVALUE1FSK		= 0x2D	# 1st byte of Sync word
VAL_SYNCVALUE2FSK		= 0xD4	# 2nd byte of Sync word
VAL_SYNCVALUE1OOK		= 0x80	# 1nd byte of Sync word
VAL_PACKETCONFIG1FSK	= 0xA2	# Variable length, Manchester coding, Addr must match NodeAddress
VAL_PACKETCONFIG1FSKNO	= 0xA0	# Variable length, Manchester coding
VAL_PACKETCONFIG1OOK	= 0		# Fixed length, no Manchester coding
VAL_PAYLOADLEN255		= 0xFF	# max Length in RX, not used in Tx
VAL_PAYLOADLEN66		= 66	# max Length in RX, not used in Tx
VAL_PAYLOADLEN_OOK		= (13 + 8 * 17)	# Payload Length
VAL_NODEADDRESS01		= 0x01	# Node address used in address filtering
VAL_NODEADDRESS04		= 0x04	# Node address used in address filtering
VAL_FIFOTHRESH1			= 0x81	# Condition to start packet transmission: at least one byte in FIFO
VAL_FIFOTHRESH30		= 0x1E	# Condition to start packet transmission: wait for 30 bytes in FIFO

config_FSK = [
    [ADDR_REGDATAMODUL,     VAL_REGDATAMODUL_FSK],	    # modulation scheme FSK
    [ADDR_FDEVMSB, 		    VAL_FDEVMSB30],  			# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
    [ADDR_FDEVLSB, 		    VAL_FDEVLSB30],			    # frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
    [ADDR_FRMSB, 		    VAL_FRMSB434],			    # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_FRMID, 		    VAL_FRMID434],			    # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_FRLSB, 		    VAL_FRLSB434],			    # carrier freq -> 434.3MHz 0x6C9333
    [ADDR_AFCCTRL, 		    VAL_AFCCTRLS],			    # standard AFC routine
    [ADDR_LNA, 			    VAL_LNA50],				    # 200ohms, gain by AGC loop -> 50ohms
    [ADDR_RXBW, 		    VAL_RXBW60],				# channel filter bandwidth 10kHz -> 60kHz  page:26
    [ADDR_BITRATEMSB, 	    0x1A],					    # 4800b/s
    [ADDR_BITRATELSB, 	    0x0B],					    # 4800b/s
    #[ADDR_AFCFEI, 		    VAL_AFCFEIRX],		        # AFC is performed each time rx mode is entered
    #[ADDR_RSSITHRESH, 	    VAL_RSSITHRESH220],	        # RSSI threshold 0xE4 -> 0xDC (220)
    #[ADDR_PREAMBLELSB, 	VAL_PREAMBLELSB5],	        # preamble size LSB set to 5
    [ADDR_SYNCCONFIG, 	    VAL_SYNCCONFIG2],		    # Size of the Synch word = 2 (SyncSize + 1)
    [ADDR_SYNCVALUE1, 	    VAL_SYNCVALUE1FSK],		    # 1st byte of Sync word
    [ADDR_SYNCVALUE2, 	    VAL_SYNCVALUE2FSK],		    # 2nd byte of Sync word
    #[ADDR_PACKETCONFIG1,   VAL_PACKETCONFIG1FSK],	    # Variable length, Manchester coding, Addr must match NodeAddress
    [ADDR_PACKETCONFIG1,    VAL_PACKETCONFIG1FSKNO],	# Variable length, Manchester coding
    [ADDR_PAYLOADLEN, 	    VAL_PAYLOADLEN66],		    # max Length in RX, not used in Tx
    #[ADDR_NODEADDRESS, 	VAL_NODEADDRESS01],		    # Node address used in address filtering
    [ADDR_NODEADDRESS, 	    0x06],		                # Node address used in address filtering
    [ADDR_FIFOTHRESH, 	    VAL_FIFOTHRESH1],		    # Condition to start packet transmission: at least one byte in FIFO
    [ADDR_OPMODE, 		    MODE_RECEIVER]			    # Operating mode to Receiver
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

def dumpPayloadAsHex(payload):
    length = payload[0]
    print(hex(length))
    if length+1 != len(payload):
        print("warning length byte mismatch actual:%d inbuf:%d" % (len(payload), length))

    for i in range(1,length+1):
        print("[%d] = %s" % (i, hex(payload[i])))





#----- USER API ---------------------------------------------------------------
#
# This is only a first-pass at a user API.
# it might change quite a bit in the second pass.

mode = None

def init():
    spi.init_defaults()
    trace("config FSK")
    HRF_config_FSK()
    HRF_clear_fifo()
    receiver()


def transmitter():
    """Change into transmitter mode"""
    global mode
    trace("transmitter mode")
    HRF_change_mode(MODE_TRANSMITER)
    mode = "TRANSMITTER"
    HRF_wait_txready()


def transmit(payload):
    HRF_send_payload(payload)


def receiver():
    """Change into receiver mode"""
    global mode
    trace("receiver mode")
    HRF_change_mode(MODE_RECEIVER)
    HRF_wait_ready()
    mode = "RECEIVER"


def isReceiveWaiting():
    return HRF_check_payload()


def receive():
    return HRF_receive_payload()


def finished():
    """Close the library down cleanly when finished"""
    spi.finished()



# END
