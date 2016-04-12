/* radio_test.c  D.J.Whale  03/04/2016
 *
 * A simple Energenie radio exerciser
 *
 * Repeatedly transmits OOK packets to turn switch 1 on and off.
 */


/***** INCLUDES *****/

#include "system.h"
#include "radio.h"
#include "gpio.h"
#include "spi.h"
#include "hrf69.h"


/***** CONSTANTS *****/


int main(int argc, char **argv)
{
  gpio_init();
  spi_init_defaults();

  //TODO
  return 0;
}


/***** END OF FILE *****/
