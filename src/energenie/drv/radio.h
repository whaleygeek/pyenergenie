/* radio.h  03/04/2016  D.J.Whale
 *
 * Energenie radio interface
 */


#ifndef _RADIO_H
#define _RADIO_H

typedef uint8_t RADIO_RESULT;
#define RADIO_RESULT_ERR_UNIMPLEMENTED 0x81

typedef uint8_t RADIO_MODULATION;
#define RADIO_MODULATION_OOK 0
#define RADIO_MODULATION_FSK 1


extern void radio_init(void);

extern void radio_modulation(RADIO_MODULATION mod);

extern void radio_transmitter(RADIO_MODULATION mod);

extern void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats);

extern void radio_receiver(RADIO_MODULATION mod);

extern RADIO_RESULT radio_isReceiveWaiting(void);

extern RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len);

extern void radio_standby(void);

extern void radio_finished(void);

#endif

/***** END OF FILE *****/
