/* radio.h  03/04/2016  D.J.Whale
 *
 * Energenie radio interface
 */


#ifndef _RADIO_H
#define _RADIO_H

typedef uint8_t RADIO_RESULT;
#define RADIO_RESULT_IS_ERR(R)         (((R) & 0x80) != 0)
#define RADIO_RESULT_OK                0x00
#define RADIO_RESULT_OK_FALSE          0x00
#define RADIO_RESULT_OK_TRUE           0x01
#define RADIO_RESULT_ERR_UNIMPLEMENTED 0x80
#define RADIO_RESULT_ERR_LONG_PAYLOAD  0x81
#define RADIO_RESULT_ERR_READ_FAILED   0x82

typedef uint8_t RADIO_MODULATION;
#define RADIO_MODULATION_OOK 0
#define RADIO_MODULATION_FSK 1


extern void radio_init(void);

extern void radio_reset(void);

extern uint8_t radio_get_ver(void);

extern void radio_modulation(RADIO_MODULATION mod);

extern void radio_transmitter(RADIO_MODULATION mod);

extern void radio_transmit(uint8_t* payload, uint8_t len, uint8_t times);

extern void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t times);

extern void radio_receiver(RADIO_MODULATION mod);

extern RADIO_RESULT radio_is_receive_waiting(void);

extern RADIO_RESULT radio_get_payload_len(uint8_t* buf, uint8_t buflen);

extern RADIO_RESULT radio_get_payload_cbp(uint8_t* buf, uint8_t buflen);

extern void radio_standby(void);

extern void radio_finished(void);

#endif

/***** END OF FILE *****/
