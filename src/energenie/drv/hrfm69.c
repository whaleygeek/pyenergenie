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
// If rxlen != NULL, assumes payload is count byte preceded
// and will read that number of bytes following it,
// and report actual bytes read in *rxlen.
// count byte is always returned as first byte of buffer

HRF_RESULT HRF_readfifo_burst(uint8_t* buf, uint8_t buflen, uint8_t* rxlen)
{
    uint8_t data;
    uint8_t count;

    spi_select();

    /* Read the first byte, and then decide how to do byte counting */
    data = spi_byte(ADDR_FIFO);
    count = 1; /* Already received 1 byte */
    *(buf++) = data; /* always return to user, regardless of if count byte */

    /* Decide byte-counting strategy */
    if (rxlen != NULL)
    { /* count-byte preceeded */
        if (data > buflen)
        { /* Payload won't fit into user buffer */
            spi_deselect();
            return HRF_RESULT_ERR_BUFFER_TOO_SMALL;
        }
        /* else, first byte is count byte, reduce buflen and use as count */
        buflen = data;
    }
    else
    { /* buflen is expected length of payload */
        buflen--; /* Have already received one byte */
    }

    /* buflen is now expected length, count is byte received counter */
    while (buflen != 0)
    {
        data = spi_byte(ADDR_FIFO);
        *(buf++) = data;
        buflen--;
        count++;
    }
    spi_deselect();

    if (rxlen != NULL)
    { /* Record count of actual bytes received */
        *rxlen = count;
    }
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

