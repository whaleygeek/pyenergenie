#include "gpio.h"
#include "spi.h"
//#include "trace.h"
#include "delay.h"
#include "hrf69.h"

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
  delay(2000);
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

//TODO this table should be in progmem??
HRF_CONFIG_REC config_OOK[] = {
    {HRF_ADDR_REGDATAMODUL,       HRF_VAL_REGDATAMODUL_OOK},	 // modulation scheme OOK
    {HRF_ADDR_FDEVMSB,            0},                            // frequency deviation -> 0kHz
    {HRF_ADDR_FDEVLSB,            0},                            // frequency deviation -> 0kHz
    {HRF_ADDR_FRMSB,              HRF_VAL_FRMSB433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_FRMID,              HRF_VAL_FRMID433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_FRLSB,              HRF_VAL_FRLSB433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_RXBW,               HRF_VAL_RXBW120},              // channel filter bandwidth 120kHz
    {HRF_ADDR_BITRATEMSB, 	      0x40},                         // 1938b/s
    {HRF_ADDR_BITRATELSB,         0x80},                         // 1938b/s
    {HRF_ADDR_PREAMBLELSB, 	      0},                            // preamble size LSB 3
    {HRF_ADDR_SYNCCONFIG, 	      HRF_VAL_SYNCCONFIG4},		     // Size of the Sync word = 4 (SyncSize + 1)
    {HRF_ADDR_SYNCVALUE1, 	      HRF_VAL_SYNCVALUE1OOK},        // sync value 1
    {HRF_ADDR_SYNCVALUE2, 	      0},                            // sync value 2
    {HRF_ADDR_SYNCVALUE3, 	      0},                            // sync value 3
    {HRF_ADDR_SYNCVALUE4, 	      0},                            // sync value 4
    {HRF_ADDR_PACKETCONFIG1,      HRF_VAL_PACKETCONFIG1OOK},	 // Fixed length, no Manchester coding, OOK
    {HRF_ADDR_PAYLOADLEN, 	      HRF_VAL_PAYLOADLEN_OOK},	     // Payload Length
    {HRF_ADDR_FIFOTHRESH, 	      HRF_VAL_FIFOTHRESH30}          // Condition to start packet transmission: wait for 30 bytes in FIFO
};


// A 'go for broke' OOK payload sender
void hrf_test_send_ook(void)
{
    uint8_t payload[] = {
        // Preamble
        0x00, 0x80, 0x00, 0x00, 0x00,
        // Encoded 20 bit address
        0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8,
        // Command bits
        0xEE, 0xE8       // 1110 = E = switch 1 off
        //0xEE, 0xEE     // 1111 = F = switch 1 on
    };

    reset();
    HRF_config(config_OOK, sizeof(config_OOK));
    HRF_change_mode(HRF_MODE_TRANSMITTER);


    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);
    HRF_writefifo_burst(payload, sizeof(payload));

    //for (int i=0; i<8; i++)
    //{
    //    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFOLEVEL, 0);
    //    HRF_writefifo_burst(payload, sizeof(payload));
    //}

    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT); // wait for Packet sent

    //uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

    //TRACE_OUTS("irqflags2:");
    //TRACE_OUTN(irqflags2);
    //TRACE_NL();
    //if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
    //{
    //    //TRACE_FAIL("Failed to send repeated payload");
    //}

}


void loop()
{
  while (true)
  {
    hrf_test_send_ook();
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


