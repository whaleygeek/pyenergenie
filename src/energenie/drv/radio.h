/* radio.h  03/04/2016  D.J.Whale
 *
 * Energenie radio interface
 */

#ifndef _RADIO_H
#define _RADIO_H

typedef uint8_t RADIO_RESULT;

typedef uint8_t RADIO_MODULATION
#define RADIO_MODULATION_OOK 0
#define RADIO_MODULATION_FSK 1


// Energenie specific Values
#define RADIO_VAL_SYNCVALUE1FSK          0x2D	// 1st byte of Sync word
#define RADIO_VAL_SYNCVALUE2FSK          0xD4	// 2nd byte of Sync word
#define RADIO_VAL_SYNCVALUE1OOK          0x80	// 1nd byte of Sync word
#define RADIO_VAL_PACKETCONFIG1FSK       0xA2	// Variable length, Manchester coding, Addr must match NodeAddress
#define RADIO_VAL_PACKETCONFIG1FSKNO     0xA0	// Variable length, Manchester coding
#define RADIO_VAL_PACKETCONFIG1OOK       0		// Fixed length, no Manchester coding
#define RADIO_VAL_PAYLOADLEN_OOK         (13 + 8 * 17)	// Payload Length
//#define RADIO_VAL_NODEADDRESS01          0x01	// Node address used in address filtering
//#define RADIO_VAL_NODEADDRESS04          0x04	// Node address used in address filtering


extern void radio_init(void);

extern void radio_modulation(RADIO_MODULATION mod);

extern void radio_transmitter(RADIO_MODULATION mod);

extern void radio_transmit(uint8_t* payload, uint8_t len);

extern void radio_send_OOK_payload(uint8_t* payload, uint8_t len);

extern void radio_receiver(RADIO_MODULATION mod);

extern RADIO_RESULT radio_isReceiveWaiting(void);

extern uint8_t* radio_receive(uint8_t maxlen);

extern void radio_finished(void);

#endif

/***** END OF FILE *****/
