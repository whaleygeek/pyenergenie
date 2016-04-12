/* hrf69_test.c  D.J.Whale  03/04/2016
 *
 * A simple exerciser for the HopeRF RFM69 radio
 * Configures for OOK, and uses a bitpattern than generates
 * a fixed tone, that can be measured at the receiving end.
 */


/***** INCLUDES *****/

//#include <stdio.h>
//#include <stdlib.h>
#include "system.h"
#include "delay.h"
#include "gpio.h"
#include "spi.h"
#include "hrfm69.h"
#include "trace.h"


/***** CONFIGURATION *****/

/* Only define this if you are running mac/pc/pi,
 * arduino will have a different console wrapper to drive tests, probably
 */

#define HRFM69_TEST
extern void gpio_mock_set_in(uint8_t g, uint8_t v);


/* GPIO assignments for Arduino Pro Micro */

//#define RESET  2
//#define CS     3
//#define MOSI   4
//#define MISO   5
//#define SCLK   6

/* GPIO assignments for Raspberry Pi using BCM numbering */
#define RESET     25
#define LED_GREEN 27   // (not B rev1)
#define LED_RED   22

#define CS        7    // CE1
#define SCLK      11
#define MOSI      10
#define MISO      9

SPI_CONFIG radioConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0};
                          //TSETTLE, THOLD, TFREQ};


/***** FUNCTION PROTOTYPES *****/

static void reset(void);
//void hrf_test_rw(void);
//void hrf_test_send_ook_tone(void);


#if defined(HRFM69_TEST)
int main(int argc, char **argv)
{
    gpio_init();

    gpio_setout(RESET);
    gpio_low(RESET);

    gpio_setout(LED_RED);
    gpio_low(LED_RED);
    gpio_setout(LED_GREEN);
    gpio_low(LED_GREEN);

    // spi_init does gpio_init (might not be correct in the longer term for shared GPIO)
    //spi_init(&radioConfig);

    gpio_high(LED_RED);
    gpio_high(LED_GREEN);


    delaysec(2);

    gpio_low(LED_RED);
    gpio_low(LED_GREEN);

    //hrf_test_send_ook();
    //spi_finished();

    gpio_finished();

    return 0;
}
#endif


// Reset is really a function of how the Energenie radio is wired up to the Pi or
// Arduino, so it will appear in the 'radio' module. It is here for testing convenience.

static void reset(void)
{
  gpio_high(RESET);
  delayms(150);

  gpio_low(RESET);
  delayus(100);
}


// write a register and read it back
// TODO readback should read the version register
// write should write a register that is not likely to mess with too much configuration

//#define TX 0x04
//#define RX 0x0C

//void hrf_test_rw(void)
//{
//  uint8_t result;
//
//  reset();
//  gpio_mock_set_in(MISO, 1); // force return bus high to test
//
//  //printf("** write:%02X\n", (unsigned int) HRF_MODE_TRANSMITER);
//  TRACE_OUTS("** write:");
//  TRACE_OUTN(TX);
//  TRACE_NL();
//
//  HRF_writereg(HRF_ADDR_OPMODE, TX);
//  result = HRF_readreg(0x00);
//
//  //printf("** read:%02X\n", (unsigned int) result);
//  TRACE_OUTS("** read:");
//  TRACE_OUTN(result);
//  TRACE_NL();
//
//  //printf("** write:%02X\n", (unsigned int) HRF_MODE_RECEIVER);
//  TRACE_OUTS("** write:");
//  TRACE_OUTN(RX);
//  TRACE_NL();
//
//  HRF_writereg(HRF_ADDR_OPMODE, RX);
//  result = HRF_readreg(0x00);
//
//  //printf("** read:%02X\n", (unsigned int) result);
//  TRACE_OUTS("** read:");
//  TRACE_OUTN(result);
//  TRACE_NL();
//
//  spi_finished();
//}


#if 0
HRF_CONFIG_REC config_OOK[] = {
    {HRF_ADDR_REGDATAMODUL,       HRF_VAL_REGDATAMODUL_OOK},	 // modulation scheme OOK
    {HRF_ADDR_FDEVMSB,            0},                            // frequency deviation -> 0kHz
    {HRF_ADDR_FDEVLSB,            0},                            // frequency deviation -> 0kHz
    {HRF_ADDR_FRMSB,              HRF_VAL_FRMSB433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_FRMID,              HRF_VAL_FRMID433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_FRLSB,              HRF_VAL_FRLSB433},             // carrier freq -> 433.92MHz 0x6C7AE1
    {HRF_ADDR_RXBW,               HRF_VAL_RXBW120},              // channel filter bandwidth 120kHz
    {HRF_ADDR_BITRATEMSB, 	      0x1A},                         // 4800b/s
    {HRF_ADDR_BITRATELSB,         0x0B},                         // 4800b/s
    {HRF_ADDR_PREAMBLELSB, 	      0},                            // preamble size LSB 3
    {HRF_ADDR_SYNCCONFIG, 	      HRF_VAL_SYNCCONFIG0},		     // Size of the Sync word = 4 (SyncSize + 1)
    {HRF_ADDR_PACKETCONFIG1,      HRF_VAL_PACKETCONFIG1OOK},	 // Fixed length, no Manchester coding, OOK
    {HRF_ADDR_PAYLOADLEN, 	      8},	                         // Payload Length
    {HRF_ADDR_FIFOTHRESH, 	      8}                             // Condition to start packet transmission: wait for 30 bytes in FIFO
};
#endif


#if 0
// Send a test tone using OOK modulation
void hrf_test_send_ook_tone(void)
{
    reset();

    HRF_config(config_OOK, sizeof(config_OOK));
    HRF_change_mode(HRF_MODE_TRANSMITTER);

    /* Wait for transmitter to be ready */
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);

    /* A regular tone */
    static uint8_t payload[] = {
        0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA
    };

    while (1) /* Forever */
    {
        HRF_writefifo_burst(payload, sizeof(payload));
        HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT); // wait for Packet sent
    }


    //uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

    //TRACE_OUTS("irqflags2:");
    //TRACE_OUTN(irqflags2);
    //TRACE_NL();
    //if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
    //{
    //    TRACE_FAIL("Failed to send repeated payload");
    //}
}
#endif


/***** END OF FILE *****/
