/* gpio.h  D.J.Whale  8/07/2014
 * 
 * A very simple interface to the GPIO port on the Raspberry Pi.
 */

#ifndef GPIO_H
#define GPIO_H

#include "system.h"

extern const uint8_t gpio_sim; /* 0=> not simulated */

/***** FUNCTION PROTOTYPES *****/

void    gpio_init(void);
void    gpio_setin(uint8_t g);
void    gpio_setout(uint8_t g);
void    gpio_high(uint8_t g);
void    gpio_low(uint8_t g);
void    gpio_write(uint8_t g, uint8_t v);
uint8_t gpio_read(uint8_t g);
void    gpio_finished(void);

#endif

/***** END OF FILE *****/

