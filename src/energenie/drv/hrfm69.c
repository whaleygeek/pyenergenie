/* hrf69.c  03/04/2016  D.J.Whale
 *
 * Hope RF RFM69 radio controller low level register interface.
 */

#include "system.h"
#include "hrfm69.h"
#include "spi.h"
#include "trace.h"
#include "gpio.h"


/*---------------------------------------------------------------------------*/
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


/*---------------------------------------------------------------------------*/
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


/*---------------------------------------------------------------------------*/
// Write all bytes in buf to the payload FIFO, in a single burst

void HRF_writefifo_burst(uint8_t* buf, uint8_t len)
{
    spi_select();
    spi_byte(HRF_ADDR_FIFO | HRF_MASK_WRITE_DATA);
    spi_frame(buf, NULL, len);
    spi_deselect();
}


/*---------------------------------------------------------------------------*/

void HRF_readfifo_burst(uint8_t* buf, uint8_t len)
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
}


/*---------------------------------------------------------------------------*/
// Check to see if a register matches a specific value or not

HRF_RESULT HRF_checkreg(uint8_t addr, uint8_t mask, uint8_t value)
{
    uint8_t regval = HRF_readreg(addr);
    return (regval & mask) == value;
}


/*---------------------------------------------------------------------------*/
// Poll a register until it meets some criteria

void HRF_pollreg(uint8_t addr, uint8_t mask, uint8_t value)
{
    if (gpio_sim)
    {
        TRACE_OUTS("gpio simulated, bailing early to prevent lockup\n");
        return;
    }

    while (! HRF_checkreg(addr, mask, value))
    {
      // busy wait (TODO:with no timeout & error recovery?)
    }
}


/*---------------------------------------------------------------------------*/
// Clear any data in the HRF payload FIFO, by reading until empty

void HRF_clear_fifo(void)
{
    //TODO: max fifolen is 66, should bail after that to prevent lockup
    while ((HRF_readreg(HRF_ADDR_IRQFLAGS2) & HRF_MASK_FIFONOTEMPTY) == HRF_MASK_FIFONOTEMPTY)
    {
        HRF_readreg(HRF_ADDR_FIFO);
    }
}


/***** END OF FILE *****/

