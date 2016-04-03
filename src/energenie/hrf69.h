/* hrf69.h  03/04/2016  D.J.Whale
 *
 * Interface for HopeRF RFM69 radio
 */

//# Precise register descriptions can be found in:
//# www.hoperf.com/upload/rf/RFM69W-V1.3.pdf
//# on page 63 - 74

//ADDR_FIFO                   = 0x00
//ADDR_OPMODE                 = 0x01
//ADDR_REGDATAMODUL           = 0x02
//ADDR_BITRATEMSB             = 0x03
//ADDR_BITRATELSB             = 0x04
//ADDR_FDEVMSB                = 0x05
//ADDR_FDEVLSB                = 0x06
//ADDR_FRMSB                  = 0x07
//ADDR_FRMID                  = 0x08
//ADDR_FRLSB                  = 0x09
//ADDR_AFCCTRL                = 0x0B
//ADDR_LNA                    = 0x18
//ADDR_RXBW                   = 0x19
//ADDR_AFCFEI                 = 0x1E
//ADDR_IRQFLAGS1              = 0x27
//ADDR_IRQFLAGS2              = 0x28
//ADDR_RSSITHRESH             = 0x29
//ADDR_PREAMBLELSB            = 0x2D
//ADDR_SYNCCONFIG             = 0x2E
//ADDR_SYNCVALUE1             = 0x2F
//ADDR_SYNCVALUE2             = 0x30
//ADDR_SYNCVALUE3             = 0x31
//ADDR_SYNCVALUE4             = 0x32
//ADDR_PACKETCONFIG1          = 0x37
//ADDR_PAYLOADLEN             = 0x38
//ADDR_NODEADDRESS            = 0x39
//ADDR_FIFOTHRESH             = 0x3C

//# HopeRF masks to set and clear bits
//MASK_REGDATAMODUL_OOK       = 0x08
//MASK_REGDATAMODUL_FSK       = 0x00
//MASK_WRITE_DATA             = 0x80
//MASK_MODEREADY              = 0x80
//MASK_FIFONOTEMPTY           = 0x40
//MASK_FIFOLEVEL              = 0x20
//MASK_FIFOOVERRUN            = 0x10
//MASK_PACKETSENT             = 0x08
//MASK_TXREADY                = 0x20
//MASK_PACKETMODE             = 0x60
//MASK_MODULATION             = 0x18
//MASK_PAYLOADRDY             = 0x04

//MODE_STANDBY                = 0x04	# Standby
//MODE_TRANSMITER             = 0x0C	# Transmiter
//MODE_RECEIVER               = 0x10	# Receiver
//VAL_REGDATAMODUL_FSK        = 0x00	# Modulation scheme FSK
//VAL_REGDATAMODUL_OOK        = 0x08	# Modulation scheme OOK
//VAL_FDEVMSB30               = 0x01	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
//VAL_FDEVLSB30               = 0xEC	# frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
//VAL_FRMSB434                = 0x6C	# carrier freq -> 434.3MHz 0x6C9333
//VAL_FRMID434                = 0x93	# carrier freq -> 434.3MHz 0x6C9333
//VAL_FRLSB434                = 0x33	# carrier freq -> 434.3MHz 0x6C9333
//VAL_FRMSB433                = 0x6C	# carrier freq -> 433.92MHz 0x6C7AE1
//VAL_FRMID433                = 0x7A	# carrier freq -> 433.92MHz 0x6C7AE1
//VAL_FRLSB433                = 0xE1	# carrier freq -> 433.92MHz 0x6C7AE1
//VAL_AFCCTRLS                = 0x00	# standard AFC routine
//VAL_AFCCTRLI                = 0x20	# improved AFC routine
//VAL_LNA50                   = 0x08	# LNA input impedance 50 ohms
//VAL_LNA50G                  = 0x0E	# LNA input impedance 50 ohms, LNA gain -> 48db
//VAL_LNA200                  = 0x88	# LNA input impedance 200 ohms
//VAL_RXBW60                  = 0x43	# channel filter bandwidth 10kHz -> 60kHz  page:26
//VAL_RXBW120                 = 0x41	# channel filter bandwidth 120kHz
//VAL_AFCFEIRX                = 0x04	# AFC is performed each time RX mode is entered
//VAL_RSSITHRESH220           = 0xDC	# RSSI threshold 0xE4 -> 0xDC (220)
//VAL_PREAMBLELSB3            = 0x03	# preamble size LSB 3
//VAL_PREAMBLELSB5            = 0x05	# preamble size LSB 5
//VAL_SYNCCONFIG2             = 0x88	# Size of the Synch word = 2 (SyncSize + 1)
//VAL_SYNCCONFIG4             = 0x98	# Size of the Synch word = 4 (SyncSize + 1)
//VAL_SYNCVALUE1FSK           = 0x2D	# 1st byte of Sync word
//VAL_SYNCVALUE2FSK           = 0xD4	# 2nd byte of Sync word
//VAL_SYNCVALUE1OOK           = 0x80	# 1nd byte of Sync word
//VAL_PACKETCONFIG1FSK        = 0xA2	# Variable length, Manchester coding, Addr must match NodeAddress
//VAL_PACKETCONFIG1FSKNO      = 0xA0	# Variable length, Manchester coding
//VAL_PACKETCONFIG1OOK        = 0		# Fixed length, no Manchester coding
//VAL_PAYLOADLEN255           = 0xFF	# max Length in RX, not used in Tx
//VAL_PAYLOADLEN66            = 66	# max Length in RX, not used in Tx
//VAL_PAYLOADLEN_OOK          = (13 + 8 * 17)	# Payload Length
//VAL_NODEADDRESS01           = 0x01	# Node address used in address filtering
//VAL_NODEADDRESS04           = 0x04	# Node address used in address filtering
//VAL_FIFOTHRESH1             = 0x81	# Condition to start packet transmission: at least one byte in FIFO
//VAL_FIFOTHRESH30            = 0x1E	# Condition to start packet transmission: wait for 30 bytes in FIFO


//def HRF_writereg(addr, data):

//def HRF_readreg(addr):

//def HRF_writefifo_burst(buf):

//def HRF_readfifo_burst():

//def HRF_checkreg(addr, mask, value):

//def HRF_pollreg(addr, mask, value):

//def HRF_wait_ready():

//def HRF_wait_txready():

//def HRF_change_mode(mode):

//def HRF_clear_fifo():

//def HRF_check_payload():

//def HRF_receive_payload():

//def HRF_send_payload(payload):

//def HRF_config(config):

//# END
