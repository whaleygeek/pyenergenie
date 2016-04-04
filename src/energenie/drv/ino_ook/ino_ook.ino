#include "gpio.h"
#include "spi.h"
//#include "trace.h"
#include "delay.h"

#define SPI_RESET 2
#define SPI_CS    3
#define SPI_SCLK  4
#define SPI_MISO  5
#define SPI_MOSI  6

static SPI_CONFIG spiConfig = {SPI_CS, SPI_SCLK, SPI_MOSI, SPI_MISO, SPI_SPOL1, SPI_CPOL0, SPI_CPHA0, 1000, 1000, 1000};

void setup()
{
  gpio_setout(SPI_RESET);
  gpio_low(SPI_RESET);
  spi_init(&spiConfig);
}

void reset()
{
  gpio_high(SPI_RESET);
  delay(150);
  gpio_low(SPI_RESET);
}

void test2()
{
  unsigned char payload[]  = {0xF0};

  reset();
  spi_select();
  spi_frame(payload, NULL, sizeof(payload));
  spi_deselect();
}


void loop()
{
  while (true)
  {
    test2();
  }
}



//void setup()
//{
//  gpio_init();
//  gpio_setout(SPI_RESET);
//  gpio_setout(SPI_CS);
//  gpio_setout(SPI_SCLK);
//  gpio_setout(SPI_MISO);
//  gpio_setout(SPI_MOSI);  
//}


//void loop()
//{
//  while (true)
//  {
//    gpio_high(SPI_RESET);
//    delaysec(1);
//    gpio_low(SPI_RESET);
//    delaysec(1);
//
//    gpio_high(SPI_CS);
//    delaysec(1);
//    gpio_low(SPI_CS);
//    delaysec(1);
//    
//    gpio_high(SPI_SCLK);
//    delaysec(1);
//    gpio_low(SPI_SCLK);
//    delaysec(1);
//    
//    gpio_high(SPI_MISO);
//    delaysec(1);
//    gpio_low(SPI_MISO);
//    delaysec(1);
//    
//    gpio_high(SPI_MOSI);
//    delaysec(1);
//    gpio_low(SPI_MOSI);
//    delaysec(1);
//  }
//}


