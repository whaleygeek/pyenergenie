/* spi_test.c  D.J.Whale  18/07/2014 
 *
 * A simple SPI port exerciser.
 * Written to do something vaguely useful on the HRFM69 module
 * (i.e. read out the version number)
 */


/***** INCLUDES *****/

#include <stdio.h>
#include <stdlib.h>
#include "system.h"
#include "gpio.h"
#include "spi.h"
#include "trace.h"
#include "delay.h"


/***** CONSTANTS *****/

/* GPIO BCM numbers on Raspberry Pi */
#define RESET 25
#define CS    7
#define SCLK  11
#define MOSI  10
#define MISO  9

/* ms */
//#define TSETTLE (1UL * 1000UL)     /* us */
//#define THOLD   (1UL * 1000UL)     /* us */
//#define TFREQ   (1UL * 1000UL)     /* 1us = 1MHz */


void reset(void)
{
    gpio_high(RESET);
    delayms(150);
    gpio_low(RESET);
    delayus(100);
}


int main(int argc, char **argv)
{
  unsigned char cmd_readver[2] = {0x10, 0x00};

  unsigned char rx[2];
  SPI_CONFIG spiConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0};
                          //{0,TSETTLE},{0,THOLD},{0,TFREQ}};

  /* Init */

  //printf("init\n");
  TRACE_OUTS("init");
  TRACE_NL();
  //gpio_init(); done by spi_init()
  spi_init(&spiConfig);
  gpio_setout(RESET);
  gpio_low(RESET);
  reset();

  /* Read version number */

  TRACE_OUTS("readver");
  TRACE_NL();
  spi_select();
  spi_frame(cmd_readver, rx, sizeof(cmd_readver));
  spi_deselect();
  TRACE_OUTS("ver=");
  TRACE_OUTN(rx[1]);
  TRACE_NL();

  /* Cleanup */

  spi_finished();
  gpio_finished();
  return 0;
}


/***** END OF FILE *****/
