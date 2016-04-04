/* gpio_test.c  30/07/2015  D.J.Whale
 * Simple test that GPIO 2/3 work
 */

#include <stdio.h>
#include <time.h>

#include "gpio.h"

//TODO this is platform specific (won't work on Arduino?)
static void delay(struct timespec time)
{
  nanosleep(&time, NULL);
}

static struct timespec delay_1sec = {1, 0};


// To allow platform specific test harnesses

#define GPIO_A 2
#define GPIO_B 3

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
    delay(delay_1sec);
    gpio_write(GPIO_A, 0);
    delay(delay_1sec);

    puts("GPIO B");
    gpio_write(GPIO_B, 1);
    delay(delay_1sec);
    gpio_write(GPIO_B, 0);
    delay(delay_1sec);
  }
  return 0;
}
