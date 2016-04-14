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


/***** LOCAL FUNCTION PROTOTYPES *****/

static uint8_t read_ver(void);
static void reset(void);


/*---------------------------------------------------------------------------*/

static void reset(void)
{
  gpio_high(RESET);
  delayms(150);

  gpio_low(RESET);
  delayus(100);
}


/*---------------------------------------------------------------------------*/

static uint8_t read_ver(void)
{
  return HRF_readreg(HRF_ADDR_VERSION);
}


/*---------------------------------------------------------------------------*/

void radio_init(void)
{
#if 0

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

    TRACE_OUTS("standby mode\n");
    HRF_change_mode(HRF_MODE_STANDBY);
    HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);


    TRACE_OUTS("testing...\n");
    //hrf_test_send_ook_tick();
    hrf_test_send_energenie_ook_switch();

    //spi_finished();
    gpio_finished();

    return 0;
#endif
// //
// def init():
//     """Initialise the module ready for use"""
//     spi.init_defaults()
//     trace("RESET")
//
//     # Note that if another program left GPIO pins in a different state
//     # and did a dirty exit, the reset fails to work and the clear fifo hangs.
//     # Might have to make the spi.init() set everything to inputs first,
//     # then set to outputs, to make sure that the
//     # GPIO registers are in a deterministic start state.
//     spi.reset() # send a hardware reset to ensure radio in clean state
//
//     HRF_clear_fifo() // not needed?
}


/*---------------------------------------------------------------------------*/

void radio_modulation(RADIO_MODULATION mod)
{
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
// def transmitter(fsk=None, ook=None):
//     """Change into transmitter mode"""
//     global mode
//
//     trace("transmitter mode")
//     modulation(fsk, ook)
//     HRF_change_mode(MODE_TRANSMITER)
//     mode = "TRANSMITTER"
//     HRF_wait_txready()
}


/*---------------------------------------------------------------------------*/

void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats)
{
// NOTE: repeats parameter, needs to configure HRF payload sender to repeat
// packet that number of times.
// NOTE: Payload should already be bit encoded and preambled by time it gets here

// def transmit(payload):
//     """Transmit a single payload using the present modulation scheme"""
//     if not modulation_fsk:
//         HRF_send_OOK_payload(payload, repeats) // might not actually be different
//     else:
//         HRF_send_payload(payload, repeats)
}


/*---------------------------------------------------------------------------*/

void radio_receiver(RADIO_MODULATION mod)
{
// def receiver(fsk=None, ook=None):
//     """Change into receiver mode"""
//     global mode
//
//     trace("receiver mode")
//     modulation(fsk, ook)
//     HRF_change_mode(MODE_RECEIVER)
//     HRF_wait_ready()
//     mode = "RECEIVER"
}


/*---------------------------------------------------------------------------*/

RADIO_RESULT radio_isReceiveWaiting(void)
{
// def isReceiveWaiting():
//     """Check to see if a payload is waiting in the receive buffer"""
//     return HRF_check_payload()
    return RADIO_RESULT_ERR_UNIMPLEMENTED;
}


/*---------------------------------------------------------------------------*/

RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len)
{
// def receive():
//     """Receive a single payload from the buffer using the present modulation scheme"""
//     return HRF_receive_payload()
    return RADIO_RESULT_ERR_UNIMPLEMENTED;
}


/*---------------------------------------------------------------------------*/

void radio_standby(void)
{
  //TODO: change radio mode to STANDBY to turn PA off and preserve power.
}


/*---------------------------------------------------------------------------*/

void radio_finished(void)
{
// def finished():
//     """Close the library down cleanly when finished"""
//     radio.standby() ??
//     spi.finished() ??
//     gpio.finished() ??
}


/*---------------------------------------------------------------------------*/

// A hard coded test of switching an Energenie switch on and off
//TODO this is for testing only, will be simplified and moved into radio_transmit.
//
//TODO note that we want to change this to use FIFO level rather than PACKETSENT
//so that we can send arbitrary length packets with arbitrary number of repeats
//(i.e. not limited by the U8 size of the payloadlen register in HRF)

static void hrf_test_send_energenie_ook_switch(void)
{
#if 0
    // Note, when PA starts up, radio inserts a 01 at start before any user data
    // we might need to pad away from this by sending a sync of many zero bits
    // to prevent it being misinterpreted as a preamble, and prevent it causing
    // the first bit of the preamble being twice the length it should be in the
    // first packet.
    // Also need to confirm this bit only occurs when transmit actually starts,
    // and not on every FIFO load.

    /* manual preamble, 20 bit encoded address, 4 encoded data bits */
    static uint8_t payload[16] = {
        0x80, 0x00, 0x00, 0x00, // preamble pulse with timing violation gap
        // Energenie 'random' 20 bit address is 0x6C6C6
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
// Limited by U8 size of PAYLOADLEN reg (15*16=240)
#define REPEATS 15
// To get longer repeats, we'll have to design a new 'unlimited'
// payload sender, and use FIFOEMPTY as a way to detect end of transmit.

    int i;
    uint8_t irqflags1;
    uint8_t irqflags2;

    TRACE_OUTS("config\n");
    HRF_config(config_OOK, CONFIG_OOK_COUNT);
    // the full packet/burst consists of repeated payloads
    // packetsent will trigger when this number of bytes have been transmitted
    HRF_writereg(HRF_ADDR_PAYLOADLEN, sizeof(payload) * REPEATS);
    // but the FIFO is filled in 1 message (4+10+2=16 byte) sections
    // level triggers when it 'strictly exceeds' level (i.e. 16 bytes starts tx,
    // and <=15 bytes triggers fifolevel irqflag to be cleared)
    HRF_writereg(HRF_ADDR_FIFOTHRESH, sizeof(payload)-1);

    uint8_t last_byte = ON;

    while (1)
    {
        /* Bring into transmitter mode and ramp up the PA */
        TRACE_OUTS("transmitter mode\n");
        HRF_change_mode(HRF_MODE_TRANSMITTER);

        TRACE_OUTS("wait for modeready,txready in irqflags1\n");
        HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY|HRF_MASK_TXREADY, HRF_MASK_MODEREADY|HRF_MASK_TXREADY);

        irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
        irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);
        TRACE_OUTS("irqflags1,2=");
        TRACE_OUTN(irqflags1);
        TRACE_OUTC(',');
        TRACE_OUTN(irqflags2);
        TRACE_NL();

        /* Set this as alternate ON or OFF bursts */
        payload[sizeof(payload)-1] = last_byte;

        TRACE_OUTS("tx repeats in a single burst:");
        TRACE_OUTN(last_byte);
        TRACE_NL();

        // send a number of payload repeats for the whole packet burst
        for (i=0; i<REPEATS; i++)
        {
            HRF_writefifo_burst(payload, sizeof(payload));
            // Tx will auto start when fifolevel is exceeded by loading the payload
            // so the level register must be correct for the size of the payload
            // otherwise transmit will never start.
            /* wait for FIFO to not exceed threshold level */
            HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_FIFOLEVEL, 0);
        }

        // wait for packet sent (num bytes tx'ed matches PAYLOADLEN reg)
        HRF_pollreg(HRF_ADDR_IRQFLAGS2, HRF_MASK_PACKETSENT, HRF_MASK_PACKETSENT);

        // Check final flags in case of overruns etc
        irqflags1 = HRF_readreg(HRF_ADDR_IRQFLAGS1);
        irqflags2 = HRF_readreg(HRF_ADDR_IRQFLAGS2);

        TRACE_OUTS("irqflags1,2=");
        TRACE_OUTN(irqflags1);
        TRACE_OUTC(',');
        TRACE_OUTN(irqflags2);
        TRACE_NL();

        // Read back PAYLOADLENGTH to confirm chip doesn't use it as a counter itself
        uint8_t pl = HRF_readreg(HRF_ADDR_PAYLOADLEN);
        TRACE_OUTS("payloadlen reg at end:");
        TRACE_OUTN(pl);
        TRACE_NL();

        /* Back to STANDBY, this clears packetsent flag */
        // always back to standby, regardless of errors above
        // otherwise PA/carrier might be left permanently on.

        TRACE_OUTS("standby mode\n");
        HRF_change_mode(HRF_MODE_STANDBY);
        HRF_pollreg(HRF_ADDR_IRQFLAGS1, HRF_MASK_MODEREADY, HRF_MASK_MODEREADY);

        if (((irqflags2 & HRF_MASK_FIFONOTEMPTY) != 0) || ((irqflags2 & HRF_MASK_FIFOOVERRUN) != 0))
        {
            TRACE_OUTN(irqflags2);
            TRACE_NL();
            TRACE_FAIL("FIFO not empty or overrun at end of burst");
        }

        /* Inter-burst delay */
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
#endif
}



/***** END OF FILE *****/
