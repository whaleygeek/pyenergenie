/* gpio_sim.c  D.J.Whale  04/04/2016
 * 
 * A very simple interface to a simulated GPIO port with no platform dependencies.
 */

/***** INCLUDES *****/

#include <stdio.h>
//#include <stdlib.h>

#include "gpio.h"


/***** CONFIGURATION *****/


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
  // Nothing to do
}


void gpio_setin(int g)
{
    printf("gpio:in:%d\n", g);
}


void gpio_setout(int g)
{
    printf("gpio:out:%d\n", g);
}


void gpio_high(int g)
{
    printf("gpio:high:%d\n", g);
}


void gpio_low(int g)
{
    printf("gpio:low:%d\n", g);
}


void gpio_write(int g, int v)
{
    printf("gpio:write:%d=%d\n", g, v);
}


int gpio_read(int g)
{
    //TODO add a console interface to allow GPIO reads to be injected
    //either from keyboard, or from a script file
    return 0; /* always low in simulation */
}


/***** END OF FILE *****/
