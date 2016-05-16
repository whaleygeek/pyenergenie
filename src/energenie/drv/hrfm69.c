/* hrf69.c  03/04/2016  D.J.Whale
 *
 * Hope RF RFM69 radio controller low level register interface.
 */

#include <stdlib.h>

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
// Read bytes from FIFO in burst mode.
// Never reads more than buflen bytes
// First received byte is the count of remaining bytes
// That byte is also returned in the user buffer.
// Note the user buffer can be > FIFO_MAX, but there is no flow control
// in the HRF driver yet, so you might get an underflow error if data is read
// quicker than it comes in on-air. You might get an overflow error if
// data comes in quicker than it is read.


HRF_RESULT HRF_readfifo_burst_cbp(uint8_t* buf, uint8_t buflen)
{
    uint8_t data;

    spi_select();
    spi_byte(HRF_ADDR_FIFO); /* prime the fifo burst reader */

    /* Read the first byte, and then decide how many remaining bytes to receive */
    data = spi_byte(HRF_ADDR_FIFO);
    *(buf++) = data; /* the count byte is always returned as first byte of user buffer */

    /* Validate the payload len against the supplied user buffer */
    if (data > buflen)
    {
        spi_deselect();
        TRACE_OUTS("buffer too small for payload len=");
        TRACE_OUTN(data);
        TRACE_NL();
        return HRF_RESULT_ERR_BUFFER_TOO_SMALL;
    }

    buflen = data; /* now the expected payload length */

    while (buflen != 0)
    {
        data = spi_byte(HRF_ADDR_FIFO);
        *(buf++) = data;
        buflen--;
    }
    spi_deselect();

    //TODO: Read irqflags
    //if underflow, this is an error (reading out too quick)
    //if overflow, this is an error (not reading out quick enough)
    //if not empty at end, this is a warning (might be ok, but user might want to clear_fifo after)
    return HRF_RESULT_OK;
}


/*---------------------------------------------------------------------------*/
// Read bytes from FIFO in burst mode.
// Tries to read exactly buflen bytes

HRF_RESULT HRF_readfifo_burst_len(uint8_t* buf, uint8_t buflen)
{
    uint8_t data;

    spi_select();
    spi_byte(HRF_ADDR_FIFO); /* prime the fifo burst reader */

    while (buflen != 0)
    {
        data = spi_byte(HRF_ADDR_FIFO);
        *(buf++) = data;
        buflen--;
    }
    spi_deselect();

    //TODO: Read irqflags
    //if underflow, this is an error (reading out too quick)
    //if overflow, this is an error (not reading out quick enough)
    //if not empty at end, this is a warning (might be ok, but user might want to clear_fifo after)
    return HRF_RESULT_OK;
}


/*---------------------------------------------------------------------------*/
// Check to see if a register matches a specific value or not

HRF_RESULT HRF_checkreg(uint8_t addr, uint8_t mask, uint8_t value)
{
    uint8_t regval = HRF_readreg(addr);
    if ((regval & mask) == value)
    {
        return HRF_RESULT_OK_TRUE;
    }
    return HRF_RESULT_OK_FALSE;
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
      // busy wait
      //TODO: No timeout or error recovery? Can cause permanent lockup
    }
}


/*---------------------------------------------------------------------------*/
// Clear any data in the HRF payload FIFO, by reading until empty

void HRF_clear_fifo(void)
{
    //TODO: max fifolen is 66, should bail after that to prevent lockup
    //especially if radio crashed and SPI always returns stuck flag bit
    while ((HRF_readreg(HRF_ADDR_IRQFLAGS2) & HRF_MASK_FIFONOTEMPTY) == HRF_MASK_FIFONOTEMPTY)
    {
        HRF_readreg(HRF_ADDR_FIFO);
    }
}


/***** END OF FILE *****/

