/* gpio_test.c  30/07/2015  D.J.Whale
 * Simple test that GPIO 2/3 work
 */

#include <stdio.h>
#include <time.h>

#include "gpio.h"

static void delay(struct timespec time)
{
  nanosleep(&time, NULL);
}

static struct timespec delay_1sec = {1, 0};


void main(void)
{
  int i;

  gpio_init();
  gpio_setout(2);
  gpio_setout(3);

  for (i=0; i<10; i++)
  {
    puts("GPIO 2");
    gpio_write(2, 1);
    delay(delay_1sec);
    gpio_write(2, 0);
    delay(delay_1sec);

    puts("GPIO 3");
    gpio_write(3, 1);
    delay(delay_1sec);
    gpio_write(3, 0);
    delay(delay_1sec);
  }
}
