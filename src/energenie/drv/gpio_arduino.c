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

#else if defined(ARDUINO)
#if defined(ARDUINO_PROMICRO)

//TODO: there might be platform specific macros here to
//extract register address and bitmask
//really, what we want is to be able to pass in a uint8_t which is a GPIO number
//and this get converted (at compile time preferably) into the register access code
//required to read/write and configure that bit. The actual mapping shoudl probably
//be in the C code for gpio_arduino

//something a bit like this, but this is not correct yet
//#define GPIO_0   PORTB,0x01
//#define GPIO_1   PORTB,0x02
//#define GPIO_2   PORTB,0x04
//#define GPIO_3   PORTB,0x08
//#define GPIO_4   PORTB,0x10
//#define GPIO_5   PORTB,0x20
//#define GPIO_6   PORTB,0x40
//#define GPIO_7   PORTB,0x90
//#define GPIO_8   PORTC,0x01
//#define GPIO_9   PORTC,0x02
//#define GPIO_10  PORTC,0x04
//#define GPIO_14  PORTC,0x08
//#define GPIO_15  PORTC,0x10
//#define GPIO_16  PORTC,0x20

#else
//#error Unknown Arduino platform
#endif
#else
//#error Unknown platform
#endif


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
