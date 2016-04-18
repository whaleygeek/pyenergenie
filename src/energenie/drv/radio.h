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

extern void radio_reset(void);

extern uint8_t radio_get_ver(void);

extern void radio_modulation(RADIO_MODULATION mod);

extern void radio_transmitter(RADIO_MODULATION mod);

//TODO: This needs to include push/pop of radio state
//extern void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats);

//TODO:this assumes radio state is transmit
extern void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t times);

//extern void radio_receiver(RADIO_MODULATION mod);

//extern RADIO_RESULT radio_isReceiveWaiting(void);

//TODO:this needs to include push/pop of radio state
//extern RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len);

//TODO:this will assume radio state is already receive
//extern RADIO_RESULT radio_receive_payload(uint8_t* buf, uint8_t len);

extern void radio_standby(void);

extern void radio_finished(void);

#endif

/***** END OF FILE *****/
