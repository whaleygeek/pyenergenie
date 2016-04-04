/* hrf69_test.c  D.J.Whale  03/04/2016
 *
 * A simple exerciser for the HopeRF RFM69 radio
 */


/***** INCLUDES *****/

#include <stdio.h>
//#include <stdlib.h>
#include "system.h"
#include "delay.h"
#include "gpio.h"
#include "spi.h"
#include "hrf69.h"
#include "trace.h"


/***** CONFIGURATION *****/

/* Only define this if you are running mac/pc/pi,
 * arduino will have a different console wrapper to drive tests, probably
 */

#define HRF69_TEST

/* GPIO assignments for Arduino Pro Micro */

#define RESET  2
#define CS     3
#define MOSI   4
#define MISO   5
#define SCLK   6


/***** FUNCTION PROTOTYPES *****/

static void reset(void);
void hrf_test_rw(void);
void hrf_test_send_ook(void);



#if defined(HRF69_TEST)
int main(int argc, char **argv)
{
    hrf_test_rw();

    //TODO: Can't test this until real radio added,
    // polling means flags will never clear
    //hrf_test_send_ook();

    return 0;
}
#endif

// Reset is really a function of how the Energenie radio is wired up to the Pi or
// Arduino, so it will appear in the 'radio' module. It is here for testing convenience.


static void reset(void)
{
  SPI_CONFIG radioConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0};
                          //TSETTLE, THOLD, TFREQ};
  spi_init(&radioConfig);

  gpio_setout(RESET);
  gpio_low(RESET);
  delayus(100);

  gpio_high(RESET);
  delayms(150);

  gpio_low(RESET);
  delayus(100);
}


extern void gpio_mock_set_in(uint8_t g, uint8_t v);


// write a register and read it back

#define TX 0x04
#define RX 0x0C

void hrf_test_rw(void)
{
  uint8_t result;

  reset();
  gpio_mock_set_in(MISO, 1); // force return bus high to test

  //printf("** write:%02X\n", (unsigned int) HRF_MODE_TRANSMITER);
  TRACE_OUTS("** write:");
  TRACE_OUTN(TX);
  TRACE_NL();

  HRF_writereg(HRF_ADDR_OPMODE, TX);
  result = HRF_readreg(0x00);

  //printf("** read:%02X\n", (unsigned int) result);
  TRACE_OUTS("** read:");
  TRACE_OUTN(result);
  TRACE_NL();

  //printf("** write:%02X\n", (unsigned int) HRF_MODE_RECEIVER);
  TRACE_OUTS("** write:");
  TRACE_OUTN(RX);
  TRACE_NL();

  HRF_writereg(HRF_ADDR_OPMODE, RX);
  result = HRF_readreg(0x00);

  //printf("** read:%02X\n", (unsigned int) result);
  TRACE_OUTS("** read:");
  TRACE_OUTN(result);
  TRACE_NL();

  spi_finished();
}


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

    reset();
    gpio_mock_set_in(MISO, 1); // force return bus high to test

    HRF_config(config_OOK, sizeof(config_OOK));
    HRF_change_mode(HRF_MODE_TRANSMITTER);

    static uint8_t payload[] = {
        // Preamble
        0x00, 0x80, 0x00, 0x00, 0x00,
        // Encoded 20 bit address
        0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8,
        // Command bits
        0xEE, 0xE8       // 1110 = E = switch 1 off
        //0xEE, 0xEE     // 1111 = F = switch 1 on
    };

    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);
    HRF_writefifo_burst(payload, sizeof(payload));

    for (int i=0; i<8; i++)
    {
        HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFOLEVEL, 0);
        HRF_writefifo_burst(payload, sizeof(payload));
    }

    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT); // wait for Packet sent

    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

    TRACE_OUTS("irqflags2:");
    TRACE_OUTN(irqflags2);
    TRACE_NL();
    if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
    {
        TRACE_FAIL("Failed to send repeated payload");
    }

    spi_finished();
}


/***** END OF FILE *****/
