#include "gpio.h"
#include "spi.h"
#include "trace.h"

#define SPI_RESET 2
#define SPI_CS    3
#define SPI_SCLK  4
#define SPI_MISO  5
#define SPI_MOSI  6



void setup()
{
  unsigned char payload[]  = {0xFF};

  SPI_CONFIG spiConfig = {SPI_CS, SPI_SCLK, SPI_MOSI, SPI_MISO, SPI_SPOL1, SPI_CPOL0, SPI_CPHA0};
                          //{0,TSETTLE},{0,THOLD},{0,TFREQ}};

  /* Init */

  //printf("init\n");
  //TRACE_OUTS("init");
  //TRACE_NL();
  //gpio_init(); done by spi_init()
  spi_init(&spiConfig);


  //printf("select\n");
  //TRACE_OUTS("select");
  //TRACE_NL();
  spi_select();
  
  //TRACE_OUTS("write");
  spi_frame(payload, NULL, sizeof(payload));

  spi_deselect();
  spi_finished();  
}

void loop()
{
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


