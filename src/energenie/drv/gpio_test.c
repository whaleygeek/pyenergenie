/* gpio_test.c  30/07/2015  D.J.Whale
 * Simple test that two GPIO pins work
 */

#include <stdio.h>
#include <time.h>

#include "system.h"
#include "gpio.h"
#include "delay.h"


/* Allows platform specific test harness,
 * different platforms will have different available GPIO numbers
 */

#define GPIO_A 22
#define GPIO_B 27

int main(void)
{
  int i;

  gpio_init();
  gpio_setout(GPIO_A);
  gpio_setout(GPIO_B);

  for (i=0; i<10; i++)
  {
    puts("GPIO A");
    gpio_write(GPIO_A, 1);
    delaysec(1);
    gpio_write(GPIO_A, 0);
    delaysec(1);

    puts("GPIO B");
    gpio_write(GPIO_B, 1);
    delaysec(1);
    gpio_write(GPIO_B, 0);
    delaysec(1);
  }
  return 0;
}
