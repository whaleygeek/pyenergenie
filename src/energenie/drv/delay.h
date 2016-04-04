/* delay.h  04/04/2016  D.J.Whale
 *
 * Abstraction for delay routines, as they are often platform specific
 */

#ifndef _DELAY_H
#define _DELAY_H

#include "system.h"

//#include <time.h>
#include <sys/time.h> // Won't work on Arduino

void delay(struct timespec time);

void delaysec(uint8_t secs);

void delayms(unsigned int ms);

void delayus(unsigned int us);

#endif

/***** END OF FILE *****/
