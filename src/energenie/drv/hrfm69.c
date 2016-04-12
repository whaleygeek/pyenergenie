/* hrf69.c  03/04/2016  D.J.Whale
 *
 * Hope RF RFM69 radio controller code.
 */

#include <stdlib.h>
#include "system.h"
#include "hrfm69.h"
#include "spi.h"
#include "trace.h"

// Write an 8 bit value to a register
void HRF_writereg(uint8_t addr, uint8_t data)
{
    TRACE_OUTS("writereg ");
    TRACE_OUTN(addr);
    TRACE_OUTC(' ');
    TRACE_OUTN(data);
    TRACE_NL();

    spi_select();
    spi_byte(addr | HRF_MASK_WRITE_DATA);
    spi_byte(data);
    spi_deselect();
}


// Read an 8 bit value from a register
uint8_t HRF_readreg(uint8_t addr)
{
    uint8_t result;

    spi_select();
    spi_byte(addr);
    result = spi_byte(0x00);
    spi_deselect();
    return result;
}


// Write all bytes in buf to the payload FIFO, in a single burst
void HRF_writefifo_burst(uint8_t* buf, uint8_t len)
{
    spi_select();
    spi_byte(HRF_ADDR_FIFO | HRF_MASK_WRITE_DATA);
    spi_frame(buf, NULL, len);
    spi_deselect();
}


//TODO: where is the buffer memory defined?
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


// Check to see if a register matches a specific value or not
HRF_RESULT HRF_checkreg(uint8_t addr, uint8_t mask, uint8_t value)
{
    uint8_t regval = HRF_readreg(addr);
    return (regval & mask) == value;
}


// Poll a register until it meets some criteria
void HRF_pollreg(uint8_t addr, uint8_t mask, uint8_t value)
{
    while (! HRF_checkreg(addr, mask, value))
    {
      // busy wait
    }
}


// Wait for HRF to be ready after last command
void HRF_wait_ready(void)
{
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);
}


// Wait for the HRF to be ready, and ready for tx, after last command
void HRF_wait_txready(void)
{
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);
}


// Change the operating mode of the HRF radi
void HRF_change_mode(uint8_t mode)
{
    HRF_writereg(HRF_ADDR_OPMODE, mode);
}


// Clear any data in the HRF payload FIFO, by reading until empty
void HRF_clear_fifo(void)
{
    while ((HRF_readreg(HRF_ADDR_IRQFLAGS2) & HRF_MASK_FIFONOTEMPTY) == HRF_MASK_FIFONOTEMPTY)
    {
        HRF_readreg(HRF_ADDR_FIFO);
    }
}


// Check if there is a payload in the FIFO waiting to be processed
HRF_RESULT HRF_check_payload(void)
{
    //TODO: First read might be superflous, but left in just in case
    uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);

    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    return (irqflags2 & HRF_MASK_PAYLOADRDY) == HRF_MASK_PAYLOADRDY;
}


//TODO: unnecessary level of runtime indirection?
//TODO: where is the buffer memory defined?
//perhaps pass in buffer memory and maxlen
//how do we know the actual length of buffer written to?
//pass in ptr to len variable
uint8_t* HRF_receive_payload(void)
{
    return HRF_readfifo_burst();
}


// Send a preformatted payload of data
void HRF_send_payload(uint8_t* payload, uint8_t len)
{
    uint8_t reg;

    HRF_writefifo_burst(payload, len);
    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT);
    reg = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    //if ((reg & HRF_MASK_FIFONOTEMPTY) != 0) or ((reg & HRF_MASK_FIFOOVERRUN) != 0):
    //    warning("Failed to send payload to HRF")
}


// Load a table of configuration values into HRF registers
void HRF_config(HRF_CONFIG_REC* config, uint8_t len)
{
    while (len-- != 0)
    {
        HRF_writereg(config->addr, config->value);
        config++;
    }
}


//# END
