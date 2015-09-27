/* gpio.h  D.J.Whale  8/07/2014
 * 
 * A very simple interface to the GPIO port on the Raspberry Pi.
 */

#ifndef GPIO_H
#define GPIO_H


/***** FUNCTION PROTOTYPES *****/

void gpio_init(void);
void gpio_setin(int g);
void gpio_setout(int g);
void gpio_high(int g);
void gpio_low(int g);
void gpio_write(int g, int v);
int  gpio_read(int g);
//TODO probably need gpio_finished() to unmmap() the memory region and clean up the peripheral?
#endif

/***** END OF FILE *****/

