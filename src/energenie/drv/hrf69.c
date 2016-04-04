/* hrf69.c  03/04/2016  D.J.Whale
 *
 * Hope RF RFM69 radio controller code.
 */

#include "system.h"
#include "hrf69.h"

//import spi

//def warning(msg):
//    print("warning:" + str(msg))


//def trace(msg):
//    print(str(msg))


//def ashex(p):
//    line = ""
//    for b in p:
//        line += str(hex(b)) + " "
//    return line



void HRF_writereg(uint8_t addr, uint8_t data)
{
//def HRF_writereg(addr, data):
//    """Write an 8 bit value to a register"""
//    buf = [addr | MASK_WRITE_DATA, data]
//    spi.select()
//    spi.frame(buf)
//    spi.deselect()
}


uint8_t HRF_readreg(uint8_t addr)
{
//def HRF_readreg(addr):
//    """Read an 8 bit value from a register"""
//    buf = [addr, 0x00]
//    spi.select()
//    res = spi.frame(buf)
//    spi.deselect()
//    return res[1] # all registers are 8 bit
    return 0; // TODO
}


void HRF_writefifo_burst(uint8_t* buf, uint8_t len)
{
//def HRF_writefifo_burst(buf):
//    """Write all bytes in buf to the payload FIFO, in a single burst"""
//    # Don't modify buf, in case caller reuses it
//    txbuf = [ADDR_FIFO | MASK_WRITE_DATA]
//    for b in buf:
//      txbuf.append(b)
//    spi.select()
//    spi.frame(txbuf)
//    spi.deselect()
}


//TODO where is the buffer memory defined?
//perhaps pass in buffer memory and maxlen
//how do we know the actual length of buffer written to?
//pass in ptr to len variable
uint8_t* HRF_readfifo_burst(void)
{
//def HRF_readfifo_burst():
//    """Read bytes from the payload FIFO using burst read"""
//    #first byte read is the length in remaining bytes
//    buf = []
//    spi.select()
//    spi.frame([ADDR_FIFO])
//    count = 1 # read at least the length byte
//    while count > 0:
//        rx = spi.frame([ADDR_FIFO])
//        data = rx[0]
//        if len(buf) == 0:
//            count = data
//        else:
//            count -= 1
//        buf.append(data)
//    spi.deselect()
//    return buf
    return (void*)0; // TODO
}


HRF_RESULT HRF_checkreg(uint8_t addr, uint8_t mask, uint8_t value)
{
//def HRF_checkreg(addr, mask, value):
//    """Check to see if a register matches a specific value or not"""
//    regval = HRF_readreg(addr)
//    #print("addr %d mask %d wanted %d actual %d" % (addr,mask,value,regval))
//    return (regval & mask) == value
    return 0; // TODO
}


void HRF_pollreg(uint8_t addr, uint8_t mask, uint8_t value)
{
//def HRF_pollreg(addr, mask, value):
//    """Poll a register until it meet some criteria"""
//    while not HRF_checkreg(addr, mask, value):
//        pass
}


void HRF_wait_ready(void)
{
//def HRF_wait_ready():
//    """Wait for HRF to be ready after last command"""
//    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY, MASK_MODEREADY)
}


void HRF_wait_txready(void)
{
//def HRF_wait_txready():
//    """Wait for HRF to be ready and ready for tx, after last command"""
//    HRF_pollreg(ADDR_IRQFLAGS1, MASK_MODEREADY|MASK_TXREADY, MASK_MODEREADY|MASK_TXREADY)
}


void HRF_change_mode(uint8_t mode)
{
//def HRF_change_mode(mode):
//    HRF_writereg(ADDR_OPMODE, mode)
}


void HRF_clear_fifo(void)
{
//def HRF_clear_fifo():
//    """Clear any data in the HRF payload FIFO by reading until empty"""
//    while (HRF_readreg(ADDR_IRQFLAGS2) & MASK_FIFONOTEMPTY) == MASK_FIFONOTEMPTY:
//        HRF_readreg(ADDR_FIFO)
}


HRF_RESULT HRF_check_payload(void)
{
//def HRF_check_payload():
//    """Check if there is a payload in the FIFO waiting to be processed"""
//    irqflags1 = HRF_readreg(ADDR_IRQFLAGS1)
//    irqflags2 = HRF_readreg(ADDR_IRQFLAGS2)
//    return (irqflags2 & MASK_PAYLOADRDY) == MASK_PAYLOADRDY
    return 0; // TODO
}


//TODO unnecessary level of runtime indirection?
//TODO where is the buffer memory defined?
//perhaps pass in buffer memory and maxlen
//how do we know the actual length of buffer written to?
//pass in ptr to len variable
uint8_t* HRF_receive_payload(void)
{
    return HRF_readfifo_burst();
}


void HRF_send_payload(uint8_t* payload, uint8_t len)
{
//def HRF_send_payload(payload):
//    HRF_writefifo_burst(payload)
//    HRF_pollreg(ADDR_IRQFLAGS2, MASK_PACKETSENT, MASK_PACKETSENT)
//    reg = HRF_readreg(ADDR_IRQFLAGS2)
//    if ((reg & MASK_FIFONOTEMPTY) != 0) or ((reg & MASK_FIFOOVERRUN) != 0):
//        warning("Failed to send payload to HRF")
}


void HRF_config(HRF_CONFIG_REC* config, uint8_t len)
{
//def HRF_config(config):
//    """Load a table of configuration values into HRF registers"""
//    for cmd in config:
//        HRF_writereg(cmd[0], cmd[1])
//        HRF_wait_ready()
}


//# END
