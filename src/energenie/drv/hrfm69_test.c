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

static uint8_t read_ver(void);
static void reset(void);

void hrf_test_send_ook_tone(void);
void hrf_test_send_energenie_ook_switch(void);


#if defined(HRFM69_TEST)
int main(int argc, char **argv)
{
    TRACE_OUTS("start\n");

    //gpio_init(); done by spi_init at moment
    spi_init(&radioConfig);

    gpio_setout(RESET);
    gpio_low(RESET);
    gpio_setout(LED_RED);
    gpio_low(LED_RED);
    gpio_setout(LED_GREEN);
    gpio_low(LED_GREEN);

    TRACE_OUTS("reset...\n");
    reset();

    TRACE_OUTS("reading radiover...\n");
    uint8_t rv = read_ver();
    TRACE_OUTN(rv);
    TRACE_NL();
    if (rv != 36)
    {
        TRACE_FAIL("unexpected radio ver, not 36(dec)\n");
    }

    TRACE_OUTS("testing...\n");
    hrf_test_send_ook_tone();
    //hrf_test_send_energenie_ook_switch();

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


static uint8_t read_ver(void)
{
  return HRF_readreg(HRF_ADDR_VERSION);
}


HRF_CONFIG_REC config_OOK[] = {
    {HRF_ADDR_REGDATAMODUL,   HRF_VAL_REGDATAMODUL_OOK},  // modulation scheme OOK
    {HRF_ADDR_FDEVMSB,        0},                         // frequency deviation:0kHz
    {HRF_ADDR_FDEVLSB,        0},                         // frequency deviation:0kHz
    {HRF_ADDR_FRMSB,          HRF_VAL_FRMSB433},          // carrier freq:433.92MHz 0x6C7AE1
    {HRF_ADDR_FRMID,          HRF_VAL_FRMID433},          // carrier freq:433.92MHz 0x6C7AE1
    {HRF_ADDR_FRLSB,          HRF_VAL_FRLSB433},          // carrier freq:433.92MHz 0x6C7AE1
    {HRF_ADDR_RXBW,           HRF_VAL_RXBW120},           // channel filter bandwidth:120kHz
    {HRF_ADDR_BITRATEMSB,     0x1A},                      // bitrate:4800b/s
    {HRF_ADDR_BITRATELSB,     0x0B},                      // bitrate:4800b/s
    {HRF_ADDR_PREAMBLELSB, 	  0},                         // preamble size LSB
    {HRF_ADDR_SYNCCONFIG,     HRF_VAL_SYNCCONFIG0},       // Size of sync word
    {HRF_ADDR_PACKETCONFIG1,  0x00},                      // Fixed length, no Manchester coding
    //{HRF_ADDR_PAYLOADLEN,     2},                         // Payload Length
    //{HRF_ADDR_FIFOTHRESH,     1}                          // Start tx when this is exceeded
};
#define CONFIG_OOK_COUNT (sizeof(config_OOK)/sizeof(HRF_CONFIG_REC))


// Send a test tone using OOK modulation
void hrf_test_send_ook_tone(void)
{
    /* two blips, to help prove the 01 at start */
    static uint8_t payload[] = {
        0x41, 0x40
    };

    int i;

    TRACE_OUTS("standby mode\n");
    HRF_change_mode(HRF_MODE_STANDBY);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);

    TRACE_OUTS("config\n");
    HRF_config(config_OOK, CONFIG_OOK_COUNT);
    HRF_writereg(HRF_ADDR_PAYLOADLEN, sizeof(payload));
    HRF_writereg(HRF_ADDR_FIFOTHRESH, sizeof(payload)-1);

    TRACE_OUTS("transmitter mode\n");
    HRF_change_mode(HRF_MODE_TRANSMITTER);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);


    uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    TRACE_OUTS("irqflags1,2=");
    TRACE_OUTN(irqflags1);
    TRACE_OUTC(',');
    TRACE_OUTN(irqflags2);
    TRACE_NL();


    TRACE_OUTS("wait for txready in irqflags1\n");
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);


    //NOTE: This uses a payloadlen of 2, and polls PACKETSENT in the repeat loop.
    //A better way to do it would be to set payloadlen to the total length,
    //check FIFOLEVEL < limit before putting more into FIFO
    //and check PACKETSENT at the end. That's how the original C code does it,
    //but there seems to be an error in the payload length calculation.
    while (1)
    {
        for (i=0; i<1; i++)
        {
            TRACE_OUTS("tx\n");
            HRF_writefifo_burst(payload, sizeof(payload));
            //TODO: should check FIFO level here??
            HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT); // wait for Packet sent
        }

        //TODO: should check PACKETSENT here??

        uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
        uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

        TRACE_OUTS("irqflags1,2=");
        TRACE_OUTN(irqflags1);
        TRACE_OUTC(',');
        TRACE_OUTN(irqflags2);
        TRACE_NL();

        if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
        {
            TRACE_OUTN(irqflags2);
            TRACE_NL();
            TRACE_FAIL("FIFO not empty or overrun at end of burst");
        }
        delaysec(1);
    }

    //NOTE: packetsent is only cleared when exiting TX (i.e. to STANDBY or RECEIVE)
}


/* Note, D0123 are transmitted as D3210
    # Coded as per the (working) C code would be:
    # b 3210
    #   0000 UNUSED         0
    #   0001 UNUSED         1
    #   0010 socket 4 off   2
    #   0011 socket 4 on    3
    #   0100 UNUSED         4
    #   0101 UNUSED         5
    #   0110 socket 2 off   6
    #   0111 socket 2 on    7
    #   1000 UNUSED         8
    #   1001 UNUSED         9
    #   1010 socket 3 off   A
    #   1011 socket 3 on    B
    #   1100 all off        C
    #   1101 all on         D
    #   1110 socket 1 off   E
    #   1111 socket 1 on    F
*/


// A hard coded test of switching an Energenie switch on and off
void hrf_test_send_energenie_ook_switch(void)
{
    /* manual preamble, 20 bit encoded address, 4 encoded data bits */
    static uint8_t payload[17] = {
        0x00,                   // pad away from the radio inserted 01 at start
        0x80, 0x00, 0x00, 0x00, // preamble pulse with timing violation gap
        // Energenie 'random' 20 bit address is 6C6C6
        // 0110 1100 0110 1100 0110
        // 0 encoded as 8 (1000)
        // 1 encoded as E (1110)
        0x8E, 0xE8,  0xEE, 0x88,  0x8E, 0xE8,  0xEE, 0x88,  0x8E, 0xE8,
        // Energenie 'switch 1 ON' command  F 1111  (0xEE, 0xEE)
        0xEE, 0xEE
        // Energenie 'switch 1 OFF' command E 1110  (0xEE, 0xE8)
        //0xEE, 0xE8
    };
/* Last byte of the payload for switch 1 */
#define ON  0xEE
#define OFF 0xE8
#define REPEATS 1

    int i;

    TRACE_OUTS("standby mode\n");
    HRF_change_mode(HRF_MODE_STANDBY);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);

    TRACE_OUTS("config\n");
    HRF_config(config_OOK, CONFIG_OOK_COUNT);
    HRF_writereg(HRF_ADDR_PAYLOADLEN, sizeof(payload));
    HRF_writereg(HRF_ADDR_FIFOTHRESH, sizeof(payload)-1);

    TRACE_OUTS("transmitter mode\n");
    HRF_change_mode(HRF_MODE_TRANSMITTER);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);

    uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    TRACE_OUTS("irqflags1,2=");
    TRACE_OUTN(irqflags1);
    TRACE_OUTC(',');
    TRACE_OUTN(irqflags2);
    TRACE_NL();

    TRACE_OUTS("wait for txready in irqflags1\n");
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);


    uint8_t last_byte = ON;

    while (1)
    {
        payload[sizeof(payload)-1] = last_byte;
        TRACE_OUTS("tx:");
        TRACE_OUTN(last_byte);
        TRACE_NL();

        for (i=0; i<REPEATS; i++)
        {
            HRF_writefifo_burst(payload, sizeof(payload));
            //TODO: should check FIFO level here?
            //if so, calculate payloadlen based on repeat count and payload size
            HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT); // wait for Packet sent
        }

        //TODO: should check packetsent here?

        uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
        uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

        TRACE_OUTS("irqflags1,2=");
        TRACE_OUTN(irqflags1);
        TRACE_OUTC(',');
        TRACE_OUTN(irqflags2);
        TRACE_NL();

        if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
        {
            TRACE_OUTN(irqflags2);
            TRACE_NL();
            TRACE_FAIL("FIFO not empty or overrun at end of burst");
        }

        delaysec(1);

        /* Toggle next switch state */
        if (last_byte == OFF)
        {
            last_byte = ON;
        }
        else
        {
            last_byte = OFF;
        }
    }
    //NOTE: packetsent is only cleared when exiting TX (i.e. to STANDBY or RECEIVE)
}


/***** END OF FILE *****/
