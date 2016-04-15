/* radio.c  12/04/2016  D.J.Whale
 *
 * An interface to the Energenie Raspberry Pi Radio.
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

// Energenie specific radio config values
//#define RADIO_VAL_SYNCVALUE1FSK          0x2D	// 1st byte of Sync word
//#define RADIO_VAL_SYNCVALUE2FSK          0xD4	// 2nd byte of Sync word
//#define RADIO_VAL_SYNCVALUE1OOK          0x80	// 1nd byte of Sync word
//#define RADIO_VAL_PACKETCONFIG1FSK       0xA2	// Variable length, Manchester coding, Addr must match NodeAddress
//#define RADIO_VAL_PACKETCONFIG1FSKNO     0xA0	// Variable length, Manchester coding
//#define RADIO_VAL_PACKETCONFIG1OOK       0		// Fixed length, no Manchester coding
//#define RADIO_VAL_PAYLOADLEN_OOK         (13 + 8 * 17)	// Payload Length (WRONG!)

//TODO: Not sure, might pass this in? What about on Arduino?
//What about if we have multiple chip selects on same SPI?
//What about if we have multiple spi's on different pins?

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


/***** LOCAL FUNCTION PROTOTYPES *****/


static void _change_mode(uint8_t mode);
static void _wait_ready(void);
static void _wait_txready(void);
static void _config(HRF_CONFIG_REC* config, uint8_t len);
//static int _payload_waiting(void);


//----- ENERGENIE SPECIFIC CONFIGURATIONS --------------------------------------
// config_FSK = [
//     [ADDR_REGDATAMODUL,       VAL_REGDATAMODUL_FSK],         # modulation scheme FSK
//     [ADDR_FDEVMSB,            VAL_FDEVMSB30],                # frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
//     [ADDR_FDEVLSB,            VAL_FDEVLSB30],                # frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
//     [ADDR_FRMSB,              VAL_FRMSB434],                 # carrier freq -> 434.3MHz 0x6C9333
//     [ADDR_FRMID,              VAL_FRMID434],                 # carrier freq -> 434.3MHz 0x6C9333
//     [ADDR_FRLSB,              VAL_FRLSB434],                 # carrier freq -> 434.3MHz 0x6C9333
//     [ADDR_AFCCTRL,            VAL_AFCCTRLS],                 # standard AFC routine
//     [ADDR_LNA,                VAL_LNA50],                    # 200ohms, gain by AGC loop -> 50ohms
//     [ADDR_RXBW,               VAL_RXBW60],                   # channel filter bandwidth 10kHz -> 60kHz  page:26
//     [ADDR_BITRATEMSB,         0x1A],                         # 4800b/s
//     [ADDR_BITRATELSB,         0x0B],                         # 4800b/s
//     [ADDR_SYNCCONFIG,         VAL_SYNCCONFIG2],              # Size of the Synch word = 2 (SyncSize + 1)
//     [ADDR_SYNCVALUE1,         VAL_SYNCVALUE1FSK],            # 1st byte of Sync word
//     [ADDR_SYNCVALUE2,         VAL_SYNCVALUE2FSK],            # 2nd byte of Sync word
//     [ADDR_PACKETCONFIG1,      VAL_PACKETCONFIG1FSKNO],       # Variable length, Manchester coding
//     [ADDR_PAYLOADLEN,         VAL_PAYLOADLEN66],             # max Length in RX, not used in Tx
//     [ADDR_NODEADDRESS,        0x06],                         # Node address used in address filtering TODO???
//     [ADDR_FIFOTHRESH,         VAL_FIFOTHRESH1],              # Condition to start packet transmission: at least one byte in FIFO
//     [ADDR_OPMODE,             MODE_RECEIVER]                 # Operating mode to Receiver
// ]


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
    {HRF_ADDR_PACKETCONFIG1,  0x00},                      // Fixed length, no Manchester coding
};
#define CONFIG_OOK_COUNT (sizeof(config_OOK)/sizeof(HRF_CONFIG_REC))


/***** MODULE STATE *****/

// mode = None
// modulation_fsk = None


/***** PRIVATE ***************************************************************/


/*---------------------------------------------------------------------------*/
// Change the operating mode of the HRF radi

static void _change_mode(uint8_t mode)
{
    HRF_writereg(HRF_ADDR_OPMODE, mode);
}


/*---------------------------------------------------------------------------*/
// Wait for HRF to be ready after last command

static void _wait_ready(void)
{
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);
}


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
// Wait for the HRF to be ready, and ready for tx, after last command

static void _wait_txready(void)
{
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

uint8_t radio_get_ver(void)
{
  return HRF_readreg(HRF_ADDR_VERSION);
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
    if (rv != 36)
    {
        TRACE_FAIL("unexpected radio ver, not 36(dec)\n");
    }

    TRACE_OUTS("standby mode\n");
    _change_mode(HRF_MODE_STANDBY);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);
}

/*---------------------------------------------------------------------------*/

void radio_modulation(RADIO_MODULATION mod)
{
    if (mod == RADIO_MODULATION_OOK)
    {
        _config(config_OOK, CONFIG_OOK_COUNT);
    }
    else
    {
        TRACE_FAIL("Unknown modulation requested\n");
    }

// def modulation(fsk=None, ook=None):
//     """Switch modulation, if needed"""
//     global modulation_fsk
//
//     # Handle sensible module defaults for earlier versions of user code
//     if fsk == None and ook == None:
//         # Force FSK mode
//         fsk = True
//
//     if fsk != None and fsk:
//         if modulation_fsk == None or modulation_fsk == False:
//             trace("switch to FSK")
//             HRF_config(config_FSK)
//             modulation_fsk = True
//
//     elif ook != None and ook:
//         if modulation_fsk == None or modulation_fsk == True:
//             trace("switch to OOK")
//             HRF_config(config_OOK)
//             modulation_fsk = False
}


/*---------------------------------------------------------------------------*/

void radio_transmitter(RADIO_MODULATION mod)
{
    TRACE_OUTS("radio_transmitter\n");
    radio_modulation(mod);
    _change_mode(HRF_MODE_TRANSMITTER);
    _wait_txready();
    //radio_data.modulation = mod;
}


/*---------------------------------------------------------------------------*/

void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats)
{
    TRACE_OUTS("radio_transmit\n");
    radio_transmitter(RADIO_MODULATION_OOK); //TODO use present state
    radio_send_payload(payload, len, repeats);
    radio_standby();
}


/*---------------------------------------------------------------------------*/
// Send a payload of data
//TODO: Rewrite this to use FIFOLEV and FIFOEMPTY with payloadlen=0
//rather than PACKETSENT, as it will allow any number of repeats.

void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t repeats)
{
    TRACE_OUTS("send_payload\n");

    // Note, when PA starts up, radio inserts a 01 at start before any user data
    // we might need to pad away from this by sending a sync of many zero bits
    // to prevent it being misinterpreted as a preamble, and prevent it causing
    // the first bit of the preamble being twice the length it should be in the
    // first packet.
    // Also need to confirm this bit only occurs when transmit actually starts,
    // and not on every FIFO load.

    int i;
    uint8_t irqflags1;
    uint8_t irqflags2;

    /* CONFIGURE: Setup the radio for transmit of the correct payload length */
    TRACE_OUTS("config\n");
    if ((unsigned int)repeats * (unsigned int)len > 255)
    {
        // This is a temporary situation until the new 'indefinite transmit'
        // scheme is implemented using fifolevel only, and ignoring packetsent.
        TRACE_FAIL("repeats*payloadlen > 255, can't configure\n");
    }

    // the full packet/burst consists of repeated payloads
    // packetsent will trigger when this number of bytes have been transmitted
    HRF_writereg(HRF_ADDR_PAYLOADLEN, len * repeats);
    // but the FIFO is filled in 1 message (4+10+2=16 byte) sections
    // level triggers when it 'strictly exceeds' level (i.e. 16 bytes starts tx,
    // and <=15 bytes triggers fifolevel irqflag to be cleared)
    HRF_writereg(HRF_ADDR_FIFOTHRESH, len-1);


    /* Bring into transmitter mode and ramp up the PA */
    TRACE_OUTS("transmitter mode\n");
    _change_mode(HRF_MODE_TRANSMITTER);

    TRACE_OUTS("wait for modeready,txready in irqflags1\n");
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);

    irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
    irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
    TRACE_OUTS("irqflags1,2=");
    TRACE_OUTN(irqflags1);
    TRACE_OUTC(',');
    TRACE_OUTN(irqflags2);
    TRACE_NL();


    /* TRANSMIT: Transmit a number of bursts back to back */
    TRACE_OUTS("tx repeats in a single burst\n");

    // send a number of payload repeats for the whole packet burst
    for (i=0; i<repeats; i++)
    {
        HRF_writefifo_burst(payload, len);
        // Tx will auto start when fifolevel is exceeded by loading the payload
        // so the level register must be correct for the size of the payload
        // otherwise transmit will never start.
        /* wait for FIFO to not exceed threshold level */
        HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFOLEVEL, 0);
    }

    // wait for packet sent (num bytes tx'ed matches PAYLOADLEN reg)
    HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT);


    /* CONFIRM: Was the transmit ok? */
    // Check final flags in case of overruns etc
    irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
    irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

    TRACE_OUTS("irqflags1,2=");
    TRACE_OUTN(irqflags1);
    TRACE_OUTC(',');
    TRACE_OUTN(irqflags2);
    TRACE_NL();

    if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
    {
        TRACE_FAIL("FIFO not empty or overrun at end of burst");
    }
}


/*---------------------------------------------------------------------------*/

//void radio_receiver(RADIO_MODULATION mod)
//{
// def receiver(fsk=None, ook=None):
//     """Change into receiver mode"""
//     global mode
//
//     trace("receiver mode")
//     modulation(fsk, ook)
//     _change_mode(MODE_RECEIVER)
//     _wait_ready()
//     mode = "RECEIVER"
//}


/*---------------------------------------------------------------------------*/

//RADIO_RESULT radio_isReceiveWaiting(void)
//{
// def isReceiveWaiting():
//     """Check to see if a payload is waiting in the receive buffer"""
//     return check_payload()
//    return RADIO_RESULT_ERR_UNIMPLEMENTED;
//}


/*---------------------------------------------------------------------------*/
//TODO high level receive, put into receive, receive a payload, back to standby

//RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len)
//{
// def receive():
//     """Receive a single payload from the buffer using the present modulation scheme"""
//     return HRF_receive_payload()
//    return RADIO_RESULT_ERR_UNIMPLEMENTED;
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

void radio_standby(void)
{
    TRACE_OUTS("radio_standby\n");
    _change_mode(HRF_MODE_STANDBY);
    _wait_ready();
    //radio_data.mode = STANDBY
}


/*---------------------------------------------------------------------------*/

void radio_finished(void)
{
    TRACE_OUTS("radio_finished\n");
    //spi_finished();
    gpio_finished();
}


/***** END OF FILE *****/
