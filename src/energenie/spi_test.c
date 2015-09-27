/* spi_test.c  D.J.Whale  18/07/2014 
 *
 * A simple SPI port exerciser.
 */


/***** INCLUDES *****/
#include <stdio.h>
#include <stdlib.h>
#include "gpio.h"
#include "spi.h"


/***** CONSTANTS *****/

/* GPIO numbers on Raspberry Pi */
#define CS    8
#define SCLK  11
#define MOSI  10
#define MISO  9

/* ms */
#define TSETTLE (1UL * 1000UL)     /* us */
#define THOLD   (1UL * 1000UL)     /* us */
#define TFREQ   (1UL * 1000UL)     /* 1us = 1MHz */

int main(int argc, char **argv)
{
  unsigned char cmd_prog[4] = {0xAC, 0x53, 0x00, 0x00};
  unsigned char cmd_id0[4]  = {0x30, 0x00, 0x00, 0x00};
  unsigned char cmd_id1[4]  = {0x30, 0x00, 0x01, 0x00};
  unsigned char cmd_id2[4]  = {0x30, 0x00, 0x02, 0x00};

  unsigned char rx[4];
  SPI_CONFIG spiConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0,
                          {0,TSETTLE},{0,THOLD},{0,TFREQ}};
  int i;
  unsigned char id[3];


  /* Init */

  printf("init\n");
  //gpio_init();
  spi_init(&spiConfig);


  /* Enter programming mode */

  printf("select\n");
  spi_select();
  spi_frame(cmd_prog, NULL, 4);


  /* Get ID bytes */

  printf("read ID bytes\n");
  spi_frame(cmd_id0, rx, 4);
  id[0] = rx[3];

  spi_frame(cmd_id1, rx, 4);
  id[1] = rx[3];

  spi_frame(cmd_id2, rx, 4);
  id[2] = rx[3];

  spi_deselect();


  /* Show ID bytes */

  printf("ID: %02X %02X %02X\n", id[0], id[1], id[2]);

  spi_finished();
  return 0;
}


/***** END OF FILE *****/
