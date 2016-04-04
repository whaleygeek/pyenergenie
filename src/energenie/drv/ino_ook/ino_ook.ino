#include "gpio.h"

#define SPI_RESET 2
#define SPI_CS    3
#define SPI_SCLK  4
#define SPI_MISO  5
#define SPI_MOSI  6

static void delaysec(int s)
{
  for (int i=0; i<s; i++)
  {
    delay(1000); // ms
  }
}


void setup()
{
  gpio_init();
  gpio_setout(SPI_RESET);
  gpio_setout(SPI_CS);
  gpio_setout(SPI_SCLK);
  gpio_setout(SPI_MISO);
  gpio_setout(SPI_MOSI);  
}


void loop()
{
  
  while (true)
  {
    gpio_high(SPI_RESET);
    delaysec(1);
    gpio_low(SPI_RESET);
    delaysec(1);

    gpio_high(SPI_CS);
    delaysec(1);
    gpio_low(SPI_CS);
    delaysec(1);
    
    gpio_high(SPI_SCLK);
    delaysec(1);
    gpio_low(SPI_SCLK);
    delaysec(1);
    
    gpio_high(SPI_MISO);
    delaysec(1);
    gpio_low(SPI_MISO);
    delaysec(1);
    
    gpio_high(SPI_MOSI);
    delaysec(1);
    gpio_low(SPI_MOSI);
    delaysec(1);
  }
}
