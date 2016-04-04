/* gpio_arduino.c  D.J.Whale  04/04/2016
 * 
 * A very simple interface to the GPIO port on the Arduino.
 *
 * Arduino internally uses the 'wiring' library, but experiments have shown
 * that it is really slow.
 *
 * (see blog by skpang)
 *
 * So this module uses direct register writes, and provides a placeholder for
 * compile-time selection of bitmasks and bitpatterns to support more Arduino
 * boards in the future.
 */

//TODO GPIO_SIMULATED can be replaced with gpio_sim.c in future

/***** INCLUDES *****/

//#include <stdio.h>
//#include <stdlib.h>
//#include <stdint.h>
//#include <fcntl.h>
//#include <sys/mman.h>
//#include <unistd.h>
//#include <time.h>

//#include "gpio.h"


/***** CONFIGURATION *****/

/* uncomment to make this a simulated driver */
//#define GPIO_SIMULATED


/***** CONSTANTS *****/


/***** VARIABLES *****/

/****** MACROS *****/

//#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
//#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
//#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

//#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
//#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

//#define GPIO_READ(g) ((*(gpio+13)&(1<<g)) != 0)

//#define GPIO_HIGH(g) GPIO_SET = (1<<(g))
//#define GPIO_LOW(g)  GPIO_CLR = (1<<(g))


void gpio_init()
{
  //TODO
}


void gpio_setin(int g)
{
  //TODO
}


void gpio_setout(int g)
{
  //TODO
}


void gpio_high(int g)
{
  //TODO
}


void gpio_low(int g)
{
  //TODO
}


void gpio_write(int g, int v)
{
  //TODO
}


int  gpio_read(int g)
{
  //TODO
}


/***** END OF FILE *****/
