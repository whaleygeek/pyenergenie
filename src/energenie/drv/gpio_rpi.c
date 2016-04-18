/* gpio.c  D.J.Whale  8/07/2014
 * 
 * A very simple interface to the GPIO port on the Raspberry Pi.
 */

/***** INCLUDES *****/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>

#include "gpio.h"


/***** CONSTANTS *****/

#define BCM2708_PERI_BASE        0x20000000
//#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */
#define GPIO_BASE_OFFSET           0x200000

#define PAGE_SIZE  (4*1024)
#define BLOCK_SIZE (4*1024)


/***** VARIABLES *****/

static int  mem_fd;
static void *gpio_map;

static volatile unsigned *gpio;

const uint8_t gpio_sim=0; /* 0=> not simulated */


/****** MACROS *****/

#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

#define GPIO_READ(g) ((*(gpio+13)&(1<<g)) != 0)

#define GPIO_HIGH(g) GPIO_SET = (1<<(g))
#define GPIO_LOW(g)  GPIO_CLR = (1<<(g))


void gpio_init()
{
   uint32_t peri_base = BCM2708_PERI_BASE; /* default if device tree not found */
   uint32_t gpio_base;
   FILE* fp;

   /* for RPi2, get peri-base from device tree */
   if ((fp = fopen("/proc/device-tree/soc/ranges", "rb")) != NULL)
   {
      unsigned char buf[4];

      fseek(fp, 4, SEEK_SET);
      if (fread(buf, 1, sizeof(buf), fp) == sizeof(buf))
      {
         peri_base = buf[0]<<24 | buf[1]<<16 | buf[2]<<8 | buf[3];
      }
      fclose(fp);
   }

   gpio_base = peri_base + GPIO_BASE_OFFSET;


   /* open /dev/mem */
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) 
   {
      printf("can't open /dev/mem \n");
      exit(-1); //TODO return a result code
   }

   /* mmap GPIO */
   gpio_map = mmap(
      NULL,             //Any adddress in our space will do
      BLOCK_SIZE,       //Map length
      PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
      MAP_SHARED,       //Shared with other processes
      mem_fd,           //File to map
      gpio_base         //Offset to GPIO peripheral
   );

   close(mem_fd); //No need to keep mem_fd open after mmap

   if (gpio_map == MAP_FAILED) 
   {
      printf("mmap error %d\n", (int)gpio_map);//errno also set!
      exit(-1); //TODO return a result code
   }

   // Always use volatile pointer!
   gpio = (volatile unsigned *)gpio_map;
}


void gpio_setin(uint8_t g)
{
  INP_GPIO(g);
}


void gpio_setout(uint8_t g)
{
  /* always INP_GPIO before OUT_GPIO */
  //INP_GPIO(g); #### this causes glitching
  OUT_GPIO(g);
}


void gpio_high(uint8_t g)
{
  GPIO_HIGH(g);
}


void gpio_low(uint8_t g)
{
  GPIO_LOW(g);
}


void gpio_write(uint8_t g, uint8_t v)
{
  if (v != 0)
  {
    GPIO_HIGH(g);
  }
  else
  {
    GPIO_LOW(g);
  }
}


uint8_t gpio_read(uint8_t g)
{
  return GPIO_READ(g);
}


void gpio_finished(void)
{
  //TODO probably need gpio_finished() to unmmap() the memory region and clean up the peripheral?
}


/***** END OF FILE *****/
