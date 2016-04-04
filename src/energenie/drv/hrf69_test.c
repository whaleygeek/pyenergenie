/* hrf69_test.c  D.J.Whale  03/04/2016
 *
 * A simple exerciser for the HopeRF RFM69 radio
 */


/***** INCLUDES *****/

#include <stdio.h>
//#include <stdlib.h>
#include "system.h"
#include "delay.h"
#include "gpio.h"
#include "spi.h"
#include "hrf69.h"


/***** CONFIGURATION *****/

/* Only define this if you are running mac/pc/pi,
 * arduino will have a different console wrapper to drive tests, probably
 */

#define HRF69_TEST

/* GPIO assignments for Arduino Pro Micro */

#define RESET  2
#define CS     3
#define MOSI   4
#define MISO   5
#define SCLK   6


/***** FUNCTION PROTOTYPES *****/

static void reset(void);
void hrf_test_connect(void);



#if defined(HRF69_TEST)
int main(int argc, char **argv)
{
  hrf_test_connect();
  return 0;
}
#endif

// Reset is really a function of how the Energenie radio is wired up to the Pi or
// Arduino, so it will appear in the 'radio' module. It is here for testing convenience.


static void reset(void)
{
  SPI_CONFIG radioConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0};
                          //TSETTLE, THOLD, TFREQ};
  spi_init(&radioConfig);

  gpio_setout(RESET);
  gpio_low(RESET);
  delayus(100);

  gpio_high(RESET);
  delayms(150);

  gpio_low(RESET);
  delayus(100);
}


void hrf_test_connect(void)
{
  uint8_t result;

  // can we reset the HRF, and read a register from it?

  reset();
  result = HRF_readreg(0x00);
  printf("result:%02X", (unsigned int) result);

  spi_finished();
}


/***** END OF FILE *****/
