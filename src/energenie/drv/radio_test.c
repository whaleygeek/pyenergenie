/* radio_test.c  D.J.Whale  03/04/2016
 *
 * A simple Energenie radio exerciser
 *
 * Repeatedly transmits OOK packets to turn switch 1 on and off.
 */


/***** INCLUDES *****/

#include "system.h"
#include "radio.h"
#include "delay.h"
#include "trace.h"


/***** CONSTANTS *****/

#define REPEATS 8


/***** FORWARD FUNCTION PROTOTYPES *****/

void radio_test_ook(void);
//void radio_test_fsk(void);


/*---------------------------------------------------------------------------*/

int main(int argc, char **argv)
{
    radio_test_ook();
    //TODO: radio_test_fsk();
}


/*---------------------------------------------------------------------------*/

void radio_test_ook(void)
{
    //gpio_init();
    //spi_init(&spi_config);

    radio_init();
    radio_modulation(RADIO_MODULATION_OOK);

    /* The 'radio' module knows nothing about the Energenie (HS1527) bit encoding,
     * so this test code manually encodes the bits.
     * For the full Python stack, there is an encoder module that can generate
     * specific payloads. Repeats are done in radio_transmitter.
     * The HRF preamble feature is no longer used, it's more predictable to
     * put the preamble in the payload.
     */

    /* manual preamble, 20 bit encoded address, 4 encoded data bits */
    static uint8_t enc_1on[16] = {
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

    static uint8_t enc_1off[16] = {
        0x80, 0x00, 0x00, 0x00, // preamble pulse with timing violation gap
        // Energenie 'random' 20 bit address is 0x6C6C6
        // 0110 1100 0110 1100 0110
        // 0 encoded as 8 (1000)
        // 1 encoded as E (1110)
        0x8E, 0xE8,  0xEE, 0x88,  0x8E, 0xE8,  0xEE, 0x88,  0x8E, 0xE8,
        // Energenie 'switch 1 ON' command  F 1111  (0xEE, 0xEE)
        //0xEE, 0xEE
        // Energenie 'switch 1 OFF' command E 1110  (0xEE, 0xE8)
        0xEE, 0xE8
    };


    while (1)
    {
        /* Turn switch 1 on */
        TRACE_OUTS("Switch 1 ON\n");
        radio_transmit(enc_1on, sizeof(enc_1on), REPEATS);
        delaysec(1);

        TRACE_OUTS("Switch 1 OFF\n");
        radio_transmit(enc_1off, sizeof(enc_1off), REPEATS);
        delaysec(1);
    }

    radio_finished();
}


/*---------------------------------------------------------------------------*/

//void radio_test_fsk(void)
//{
//    //TODO
//}


/***** END OF FILE *****/
