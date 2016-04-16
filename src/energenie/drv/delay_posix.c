/* delay_posix.c  04/04/2016  D.J.Whale
 *
 * Delay routines for posix compliant standard libraries (not Arduino)
 */

#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#include "system.h"
#include "delay.h"

static struct timespec delay_1sec = {1, 0};    // 1sec, 0us
static struct timespec delay_1ms  = {0, 1000}; // 0sec, 1000us


void delaysec(uint8_t secs)
{
  while (secs-- != 0)
  {
    delay(delay_1sec);
  }
}


void delayms(unsigned int ms)
{
  while (ms-- > 0)
  {
    delay(delay_1ms);
  }
}


void delay(struct timespec time)
{
  nanosleep(&time, NULL);
}


/* Based on code suggested by Gordon Henderson:
 * https://github.com/WiringPi/WiringPi/blob/master/wiringPi/wiringPi.c
 *
 * Note that his trick of using the hardware timer just didn't work,
 * and this is the best of a bad bunch. nanosleep() delays at least
 * 100uS in some cases.
 */


void delayus(unsigned int us)
{
  struct timeval tNow, tLong, tEnd;

  gettimeofday(&tNow, NULL);
  tLong.tv_sec  = us / 1000000;
  tLong.tv_usec = us % 1000000;
  timeradd(&tNow, &tLong, &tEnd);

  while (timercmp(&tNow, &tEnd, <))
  {
    gettimeofday(&tNow, NULL);
  }
}


/***** END OF FILE *****/

