/* radio.c  12/04/2016  D.J.Whale
 *
 * An interface to the Energenie Raspberry Pi Radio board ENER314-RT-VER01
 *
 * https://energenie4u.co.uk/index.phpcatalogue/product/ENER314-RT
 */

/* TODO
DONE: push the FSK configuration into radio.c
DONE: remove radio.py (the old version of the radio interface)
DONE: contrive a switch.py that only transmits
DONE: hard code device address into the dictionary
DONE: disable the call to the receive check
DONE: radio_modulation fix for FSK
DONE: implement FSK transmit in radio.c (it's just transmit())
DONE: move radio.py modulation switcher to radio2.py modulation (as it is written better?)

TODO: run the code, it should turn the switch on and off repeatedly.
*/


/***** INCLUDES *****/

#include "system.h"
#include "radio.h"
#include "delay.h"
#include "gpio.h"
#include "spi.h"
#include "hrfm69.h"
#include "trace.h"


/***** CONFIGURATION *****/

#define EXPECTED_RADIOVER 36


// Energenie specific radio config values
#define RADIO_VAL_SYNCVALUE1FSK          0x2D	// 1st byte of Sync word
#define RADIO_VAL_SYNCVALUE2FSK          0xD4	// 2nd byte of Sync word
#define RADIO_VAL_SYNCVALUE1OOK          0x80	// 1nd byte of Sync word
//#define RADIO_VAL_PACKETCONFIG1FSK       0xA2	// Variable length, Manchester coding, Addr must match NodeAddress
#define RADIO_VAL_PACKETCONFIG1FSKNO     0xA0	// Variable length, Manchester coding

//TODO: Not sure, might pass this in? What about on Arduino?
//What about if we have multiple chip selects on same SPI?
//What about if we have multiple spi's on different pins?

/* GPIO assignments for Raspberry Pi using BCM numbering */
#define RESET     25
// GREEN used for RX, RED used for TX
#define LED_GREEN 27   // (not B rev1)
#define LED_RED   22

#define CS        7    // CE1
#define SCLK      11
#define MOSI      10
#define MISO      9

SPI_CONFIG radioConfig = {CS, SCLK, MOSI, MISO, SPI_SPOL0, SPI_CPOL0, SPI_CPHA0};
                          //TSETTLE, THOLD, TFREQ};


/***** LOCAL FUNCTION PROTOTYPES *****/

static void _change_mode(uint8_t mode);
static void _wait_ready(void);
static void _wait_txready(void);
static void _config(HRF_CONFIG_REC* config, uint8_t len);
//static int _payload_waiting(void);


//----- ENERGENIE SPECIFIC CONFIGURATIONS --------------------------------------

static HRF_CONFIG_REC config_FSK[] = {
     {HRF_ADDR_REGDATAMODUL,       HRF_VAL_REGDATAMODUL_FSK},         // modulation scheme FSK
     {HRF_ADDR_FDEVMSB,            HRF_VAL_FDEVMSB30},                // frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
     {HRF_ADDR_FDEVLSB,            HRF_VAL_FDEVLSB30},                // frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
     {HRF_ADDR_FRMSB,              HRF_VAL_FRMSB434},                 // carrier freq -> 434.3MHz 0x6C9333
     {HRF_ADDR_FRMID,              HRF_VAL_FRMID434},                 // carrier freq -> 434.3MHz 0x6C9333
     {HRF_ADDR_FRLSB,              HRF_VAL_FRLSB434},                 // carrier freq -> 434.3MHz 0x6C9333
     {HRF_ADDR_AFCCTRL,            HRF_VAL_AFCCTRLS},                 // standard AFC routine
     {HRF_ADDR_LNA,                HRF_VAL_LNA50},                    // 200ohms, gain by AGC loop -> 50ohms
     {HRF_ADDR_RXBW,               HRF_VAL_RXBW60},                   // channel filter bandwidth 10kHz -> 60kHz  page:26
     {HRF_ADDR_BITRATEMSB,         0x1A},                             // 4800b/s
     {HRF_ADDR_BITRATELSB,         0x0B},                             // 4800b/s
     {HRF_ADDR_SYNCCONFIG,         HRF_VAL_SYNCCONFIG2},              // Size of the Synch word = 2 (SyncSize + 1)
     {HRF_ADDR_SYNCVALUE1,         RADIO_VAL_SYNCVALUE1FSK},            // 1st byte of Sync word
     {HRF_ADDR_SYNCVALUE2,         RADIO_VAL_SYNCVALUE2FSK},            // 2nd byte of Sync word
     {HRF_ADDR_PACKETCONFIG1,      RADIO_VAL_PACKETCONFIG1FSKNO},       // Variable length, Manchester coding
     //{HRF_ADDR_PAYLOADLEN,         HRF_VAL_PAYLOADLEN66},             // max Length in RX, not used in Tx
     //{HRF_ADDR_NODEADDRESS,        0x06},                             // Node address used in address filtering (not used)
};
#define CONFIG_FSK_COUNT (sizeof(config_FSK)/sizeof(HRF_CONFIG_REC))


static HRF_CONFIG_REC config_OOK[] = {
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
    {HRF_ADDR_SYNCCONFIG,     HRF_VAL_SYNCCONFIG0},       // Size of sync word (disabled)
    {HRF_ADDR_PACKETCONFIG1,  0x80},                      // Tx Variable length, no Manchester coding
    {HRF_ADDR_PAYLOADLEN,     0}                          // no payload length

};
#define CONFIG_OOK_COUNT (sizeof(config_OOK)/sizeof(HRF_CONFIG_REC))


/***** MODULE STATE *****/

typedef uint8_t RADIO_MODE; // Stores HRF_MODE_xxx

typedef struct
{
  RADIO_MODULATION modu;
  RADIO_MODE       mode;
} RADIO_DATA;

RADIO_DATA radio_data;


/***** PRIVATE ***************************************************************/

/*---------------------------------------------------------------------------*/
// Load a table of configuration values into HRF registers

static void _config(HRF_CONFIG_REC* config, uint8_t count)
{
    while (count-- != 0)
    {
        HRF_writereg(config->addr, config->value);
        config++;
    }
}


/*---------------------------------------------------------------------------*/
// Change the operating mode of the HRF radio

static void _change_mode(uint8_t mode)
{
    HRF_writereg(HRF_ADDR_OPMODE, mode);
    _wait_ready();
    gpio_low(LED_GREEN); // TX OFF
    gpio_low(LED_RED);   // RX OFF

    if (mode == HRF_MODE_TRANSMITTER)
    {
        _wait_txready();
        gpio_high(LED_RED);   // TX ON
    }
    else if (mode == HRF_MODE_RECEIVER)
    {
        gpio_high(LED_GREEN); // RX ON
    }
    radio_data.mode = mode;
}


/*---------------------------------------------------------------------------*/
// Wait for HRF to be ready after last command

static void _wait_ready(void)
{
    TRACE_OUTS("_wait_ready\n");
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);
}


/*---------------------------------------------------------------------------*/
// Wait for the HRF to be ready, and ready for tx, after last command

static void _wait_txready(void)
{
    TRACE_OUTS("_wait_txready\n");
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);
}


/*---------------------------------------------------------------------------*/
// Check if there is a payload in the FIFO waiting to be processed

//static int _payload_waiting(void)
//{
//    //TODO: First read might be superflous, but left in just in case
//    //uint8_t irqflags1 =
//    HRF_readreg(HRF_ADDR_IRQFLAGS1);
//
//    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
//    return (irqflags2 & HRF_MASK_PAYLOADRDY) == HRF_MASK_PAYLOADRDY;
//}


/***** PUBLIC ****************************************************************/

/*---------------------------------------------------------------------------*/

void radio_reset(void)
{
    gpio_high(RESET);
    delayms(150);

    gpio_low(RESET);
    delayus(100);
}


/*---------------------------------------------------------------------------*/

void radio_init(void)
{
    TRACE_OUTS("radio_init\n");

    //gpio_init(); done by spi_init at moment
    spi_init(&radioConfig);

    gpio_setout(RESET);
    gpio_low(RESET);
    gpio_setout(LED_RED);
    gpio_low(LED_RED);
    gpio_setout(LED_GREEN);
    gpio_low(LED_GREEN);

    TRACE_OUTS("reset...\n");
    radio_reset();

    TRACE_OUTS("reading radiover...\n");
    uint8_t rv = radio_get_ver();
    TRACE_OUTN(rv);
    TRACE_NL();
    if (rv < EXPECTED_RADIOVER) //TODO: make this ASSERT()
    {
        TRACE_OUTS("warning:unexpected radio ver<min\n");
        //TRACE_FAIL("unexpected radio ver<min\n");
    }
    else if (rv > EXPECTED_RADIOVER)
    {
        TRACE_OUTS("warning:unexpected radio ver>exp\n");
    }

    radio_standby();
}


/*---------------------------------------------------------------------------*/

uint8_t radio_get_ver(void)
{
  return HRF_readreg(HRF_ADDR_VERSION);
}


/*---------------------------------------------------------------------------*/

void radio_modulation(RADIO_MODULATION mod)
{
    if (mod == RADIO_MODULATION_OOK)
    {
        _config(config_OOK, CONFIG_OOK_COUNT);
        radio_data.modu = mod;
    }
    else if (mod == RADIO_MODULATION_FSK)
    {
        _config(config_FSK, CONFIG_FSK_COUNT);
        radio_data.modu = mod;
    }
    else //TODO: make this ASSERT()
    {
        TRACE_FAIL("Unknown modulation\n");
    }
}


/*---------------------------------------------------------------------------*/

void radio_transmitter(RADIO_MODULATION mod)
{
    TRACE_OUTS("radio_transmitter\n");

    radio_modulation(mod);
    _change_mode(HRF_MODE_TRANSMITTER);
}


/*---------------------------------------------------------------------------*/

void radio_receiver(RADIO_MODULATION mod)
{
    TRACE_OUTS("radio_receiver\n");

    radio_modulation(mod);
    _change_mode(HRF_MODE_RECEIVER);
}


/*---------------------------------------------------------------------------*/

void radio_standby(void)
{
    TRACE_OUTS("radio_standby\n");
    _change_mode(HRF_MODE_STANDBY);
}


/*---------------------------------------------------------------------------*/

void radio_transmit(uint8_t* payload, uint8_t len, uint8_t times)
{
    TRACE_OUTS("radio_transmit\n");

    uint8_t prevmode = radio_data.mode;
    if (radio_data.mode != HRF_MODE_TRANSMITTER)
    {
        _change_mode(HRF_MODE_TRANSMITTER);
    }

    radio_send_payload(payload, len, times);

    if (radio_data.mode != prevmode)
    {
       _change_mode(prevmode);
    }
}


/*---------------------------------------------------------------------------*/
// Send a payload of data

/* DESIGN FOR DUTY CYCLE PROTECTION REQUIREMENT (write this later)
 *
 * At OOK 4800bps, 1 bit is 20uS, 1 byte is 1.6ms, 16 bytes is 26.6ms
 * 15 times (old design limit) is 400ms
 * 255 times (new design limit) is 6.8s

 * See page 3 of this app note: http://www.ti.com/lit/an/swra090/swra090.pdf
 *
 * Transmitter duty cycle
 * The transmitter duty cycle is defined as the ratio of the maximum ”on” time, relative to a onehour period.
 * If message acknowledgement is required, the additional ”on” time shall be included. Advisory limits are:
 *
 * Duty cycle  Maximum “on” time [sec]   Minimum “off” time [sec]
 * 0.1 %       0.72                      0.72
 * 1 %         3.6                       1.8
 * 10 %        36                        3.6
 */

/* DESIGN FOR >255 payload len (write this later)

   will need to set fifolevel as a proportion of payload len
   and load that proportion.
   i.e. inside the payload repeat loop
     load the fifo up in non integral payload portions
   also, txstart condition would need to start before whole payload loaded in FIFO
   that is probably ok, but fifolev is more to do with fill rate and transmit rate,
   and less to do with the actual payload length.
   Note that FIFO empties at a rate proportional to the bitrate,
   and also adding on manchester coding will slow the emptying rate.
 */


void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t times)
{
    TRACE_OUTS("radio_send_payload\n");

    // Note, when PA starts up, radio inserts a 01 at start before any user data
    // we might need to pad away from this by sending a sync of many zero bits
    // to prevent it being misinterpreted as a preamble, and prevent it causing
    // the first bit of the preamble being twice the length it should be in the
    // first packet.
    // Also need to confirm this bit only occurs when transmit actually starts,
    // and not on every FIFO load.

    int i;

    /* VALIDATE: Check input parameters are in range */
    if (times == 0 || len == 0) //TODO: make this an ASSERT()
    {
        TRACE_FAIL("zero times or payloadlen\n");
    }
    if (len > 32) //TODO: make this an ASSERT()
    {
        TRACE_FAIL("payload length>32\n");
    }

    /* CONFIGURE: Setup the radio for transmit of the correct payload length */
    TRACE_OUTS("config\n");
    // Start transmitting when a full payload is loaded. So for '15':
    // level triggers when it 'strictly exceeds' level (i.e. 16 bytes starts tx,
    // and <=15 bytes triggers fifolevel irqflag to be cleared)
    // We already know from earlier that payloadlen<=32 (which fits into half a FIFO)
    HRF_writereg(HRF_ADDR_FIFOTHRESH, len-1);


    /* TRANSMIT: Transmit a number of payloads back to back */
    TRACE_OUTS("tx multiple payloads in a single burst\n");

    // send a number of payload repeats for the whole packet burst
    for (i=0; i<times; i++)
    {
        HRF_writefifo_burst(payload, len);
        // Tx will auto start when fifolevel is exceeded by loading the payload
        // so the level register must be correct for the size of the payload
        // otherwise transmit will never start.
        /* wait for FIFO to not exceed threshold level */
        HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFOLEVEL, 0);
    }

    // wait for FIFO empty, to indicate transmission completed
    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFONOTEMPTY, 0);


    /* CONFIRM: Was the transmit ok? */
    // Check final flags in case of overruns etc
#if defined(TRACE)
    uint8_t irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
    uint8_t irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    TRACE_OUTS("irqflags1,2=");
    TRACE_OUTN(irqflags1);
    TRACE_OUTC(',');
    TRACE_OUTN(irqflags2);
    TRACE_NL();

    //TODO: make this ASSERT()??
    if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
    {
        TRACE_FAIL("FIFO not empty or overrun at end of burst");
    }
#endif
}


/*---------------------------------------------------------------------------*/

//RADIO_RESULT radio_isReceiveWaiting(void)
//{
// def isReceiveWaiting():
//     """Check to see if a payload is waiting in the receive buffer"""
//     return check_payload()
//    return RADIO_RESULT_ERR_UNIMPLEMENTED;
//}


/*---------------------------------------------------------------------------*/
//TODO: high level receive, put into receive, receive a payload, back to standby

//RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len)
//{
// def receive():
//     """Receive a single payload from the buffer using the present modulation scheme"""
// change into receive mode if not already there
// receive payload
// if was not in receive mode, change back to previous mode
//}


/*---------------------------------------------------------------------------*/
//TODO: low level receive, just receive a payload
//
//RADIO_RESULT radio_receive_payload(uint8_t* buf, uint8_t len)
//{
// def receive():
//     """Receive a single payload from the buffer using the present modulation scheme"""
//     return HRF_receive_payload()
//    return RADIO_RESULT_ERR_UNIMPLEMENTED;
//}


/*---------------------------------------------------------------------------*/

void radio_finished(void)
{
    TRACE_OUTS("radio_finished\n");
    //spi_finished();
    gpio_finished();
}


/***** END OF FILE *****/
