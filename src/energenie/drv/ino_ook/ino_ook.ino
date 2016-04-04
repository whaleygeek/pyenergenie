#include "gpio.h"
#include "spi.h"
//#include "trace.h"
#include "delay.h"
                      // pin number on Raspberry Pi (not GPIO number)
#define SPI_RESET 2   // P1-22 (active high)
#define SPI_CS    3   // P1-26 (active low)
#define SPI_SCLK  4   // P1-23
#define SPI_MOSI  5   // P1-19
#define SPI_MISO  6   // P1-21
                      // P1-20   GND
                      // P1-17   3V3

static SPI_CONFIG spiConfig = {SPI_CS, SPI_SCLK, SPI_MOSI, SPI_MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0, 1000, 1000, 1000};

void setup()
{
  gpio_setout(SPI_RESET);
  gpio_low(SPI_RESET);
  spi_init(&spiConfig);
  Serial.begin(19200);
}

void reset()
{
  gpio_high(SPI_RESET);
  delay(150);
  gpio_low(SPI_RESET);
}

void test2()
{
  unsigned char wr_mode_tx[]  = {0x80 |0x01, 0x0C}; // set mode register to TRANSMITTER
  unsigned char rd_mode[]     = {0x00 |0x01, 0x00}; // read mode register
  
  unsigned char rx[2];

  reset();
  spi_select();
  spi_frame(wr_mode_tx, NULL, sizeof(wr_mode_tx));
  spi_deselect();
  
  spi_select();
  spi_frame(rd_mode, rx, sizeof(rd_mode));
  spi_deselect();
  
  Serial.println(rx[1]);
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


