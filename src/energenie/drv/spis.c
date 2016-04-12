/* spis.c  D.J.Whale  19/07/2014
 *
 * Software SPI driver built on top of gpio
 */


/***** INCLUDES *****/

//#include <stdio.h>
//#include <stdlib.h> // memcpy
#include <string.h> // memcpy (not on Arduino?)

#include "system.h"
#include "spi.h"
#include "gpio.h"
#include "delay.h"
#include "trace.h"


/***** MACROS *****/

#define CLOCK_ACTIVE() gpio_write(config.sclk, config.cpol?0:1)
#define CLOCK_IDLE()   gpio_write(config.sclk, config.cpol?1:0)

#define SELECTED()     gpio_write(config.cs, config.spol?1:0)
#define NOT_SELECTED() gpio_write(config.cs, config.spol?0:1)


/***** VARIABLES *****/

static SPI_CONFIG config;


void spi_init_defaults(void)
{
#define CS    7    //CE1
#define SCLK  11
#define MOSI  10
#define MISO  9

/* ms */
#define TSETTLE (1)     /* us settle */
#define THOLD   (1)     /* us hold */
#define TFREQ   (1)     /* us half clock */

  SPI_CONFIG defaultConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0,
                          TSETTLE, THOLD, TFREQ};

  spi_init(&defaultConfig);
}


void spi_init(SPI_CONFIG* pConfig)
{
  /* It's a standalone library, so init GPIO also */
  gpio_init();
  memcpy(&config, pConfig, sizeof(SPI_CONFIG));

  //TODO: Implement CPHA1
  if (config.cpha != 0)
  {
    TRACE_FAIL("error: CPHA 1 not yet supported");
  }

  gpio_setout(config.sclk);
  CLOCK_IDLE();

  gpio_setout(config.mosi);
  gpio_low(config.mosi);
  gpio_setin(config.miso);

  gpio_setout(config.cs);
  NOT_SELECTED();
}


void spi_finished(void)
{
  gpio_setin(config.mosi);
  gpio_setin(config.sclk);
  gpio_setin(config.cs);
}


void spi_select(void)
{
  SELECTED();
  delayus(config.tSettle);
}


void spi_deselect(void)
{
  NOT_SELECTED();
  delayus(config.tSettle);
}


int spi_byte(uint8_t txbyte)
{
  uint8_t rxbyte = 0;
  uint8_t bitno;
  uint8_t bit ;

  //TODO: Implement CPHA1

  for (bitno=0; bitno<8; bitno++)
  {
    /* Transmit MSB first */
    bit = ((txbyte & 0x80) != 0x00);
    txbyte <<= 1;
    gpio_write(config.mosi, bit);
    delayus(config.tSettle);
    CLOCK_ACTIVE();
    delayus(config.tHold);
    delayus(config.tFreq);

    /* Read MSB first */
    bit = gpio_read(config.miso);
    rxbyte = (rxbyte<<1) | bit;

    CLOCK_IDLE();
    delayus(config.tFreq);
  }
  return rxbyte;
}


void spi_frame(uint8_t* pTx, uint8_t* pRx, uint8_t count)
{
  uint8_t tx = 0;
  uint8_t rx;

  while (count > 0)
  {
    if (pTx != NULL)
    {
      tx = *(pTx++);
    }
    rx = spi_byte(tx);
    if (pRx != NULL)
    {
      *(pRx++) = rx;
    }
    count--;
  }
}


/***** END OF FILE *****/
