/* hrf69.h  03/04/2016  D.J.Whale
 *
 * Interface for HopeRF RFM69 radio
 */

//# Precise register descriptions can be found in:
//# www.hoperf.com/upload/rf/RFM69W-V1.3.pdf
//# on page 63 - 74

#ifndef _HRF69_H
#define _HRF69_H

#include "system.h"

typedef uint8_t HRF_RESULT;
//consider these, so we can easily pass back a boolean too
#define HRF_RESULT_OK                   0x00
#define HRF_RESULT_OK_FALSE             0x00
#define HRF_RESULT_OK_TRUE              0x01
#define HRF_RESULT_ERR_BUFFER_TOO_SMALL 0x81

typedef struct
{
  uint8_t addr;
  uint8_t value;
} HRF_CONFIG_REC;


// Register addresses
#define HRF_ADDR_FIFO                  0x00
#define HRF_ADDR_OPMODE                0x01
#define HRF_ADDR_REGDATAMODUL          0x02
#define HRF_ADDR_BITRATEMSB            0x03
#define HRF_ADDR_BITRATELSB            0x04
#define HRF_ADDR_FDEVMSB               0x05
#define HRF_ADDR_FDEVLSB               0x06
#define HRF_ADDR_FRMSB                 0x07
#define HRF_ADDR_FRMID                 0x08
#define HRF_ADDR_FRLSB                 0x09
#define HRF_ADDR_AFCCTRL               0x0B
#define HRF_ADDR_VERSION               0x10
#define HRF_ADDR_LNA                   0x18
#define HRF_ADDR_RXBW                  0x19
#define HRF_ADDR_AFCFEI                0x1E
#define HRF_ADDR_IRQFLAGS1             0x27
#define HRF_ADDR_IRQFLAGS2             0x28
#define HRF_ADDR_RSSITHRESH            0x29
#define HRF_ADDR_PREAMBLELSB           0x2D
#define HRF_ADDR_SYNCCONFIG            0x2E
#define HRF_ADDR_SYNCVALUE1            0x2F
#define HRF_ADDR_SYNCVALUE2            0x30
#define HRF_ADDR_SYNCVALUE3            0x31
#define HRF_ADDR_SYNCVALUE4            0x32
#define HRF_ADDR_SYNCVALUE5            0x33
#define HRF_ADDR_SYNCVALUE6            0x34
#define HRF_ADDR_SYNCVALUE7            0x35
#define HRF_ADDR_SYNCVALUE8            0x36
#define HRF_ADDR_PACKETCONFIG1         0x37
#define HRF_ADDR_PAYLOADLEN            0x38
#define HRF_ADDR_NODEADDRESS           0x39
#define HRF_ADDR_FIFOTHRESH            0x3C

// Masks to set and clear bits
#define HRF_MASK_REGDATAMODUL_OOK      0x08
#define HRF_MASK_REGDATAMODUL_FSK      0x00
#define HRF_MASK_WRITE_DATA            0x80
#define HRF_MASK_MODEREADY             0x80
#define HRF_MASK_FIFONOTEMPTY          0x40
#define HRF_MASK_FIFOLEVEL             0x20
#define HRF_MASK_FIFOOVERRUN           0x10
#define HRF_MASK_PACKETSENT            0x08
#define HRF_MASK_TXREADY               0x20
#define HRF_MASK_PACKETMODE            0x60
#define HRF_MASK_MODULATION            0x18
#define HRF_MASK_PAYLOADRDY            0x04

// Radio modes
#define HRF_MODE_STANDBY               0x04	// Standby
#define HRF_MODE_TRANSMITTER           0x0C	// Transmiter
#define HRF_MODE_RECEIVER              0x10	// Receiver

// Values to store in registers
#define HRF_VAL_REGDATAMODUL_FSK       0x00	// Modulation scheme FSK
#define HRF_VAL_REGDATAMODUL_OOK       0x08	// Modulation scheme OOK
#define HRF_VAL_FDEVMSB30              0x01	// frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
#define HRF_VAL_FDEVLSB30              0xEC	// frequency deviation 5kHz 0x0052 -> 30kHz 0x01EC
#define HRF_VAL_FRMSB434               0x6C	// carrier freq -> 434.3MHz 0x6C9333
#define HRF_VAL_FRMID434               0x93	// carrier freq -> 434.3MHz 0x6C9333
#define HRF_VAL_FRLSB434               0x33	// carrier freq -> 434.3MHz 0x6C9333
#define HRF_VAL_FRMSB433               0x6C	// carrier freq -> 433.92MHz 0x6C7AE1
#define HRF_VAL_FRMID433               0x7A	// carrier freq -> 433.92MHz 0x6C7AE1
#define HRF_VAL_FRLSB433               0xE1	// carrier freq -> 433.92MHz 0x6C7AE1
#define HRF_VAL_AFCCTRLS               0x00	// standard AFC routine
#define HRF_VAL_AFCCTRLI               0x20	// improved AFC routine
#define HRF_VAL_LNA50                  0x08	// LNA input impedance 50 ohms
#define HRF_VAL_LNA50G                 0x0E	// LNA input impedance 50 ohms, LNA gain -> 48db
#define HRF_VAL_LNA200                 0x88	// LNA input impedance 200 ohms
#define HRF_VAL_RXBW60                 0x43	// channel filter bandwidth 10kHz -> 60kHz  page:26
#define HRF_VAL_RXBW120                0x41	// channel filter bandwidth 120kHz
#define HRF_VAL_AFCFEIRX               0x04	// AFC is performed each time RX mode is entered
#define HRF_VAL_RSSITHRESH220          0xDC	// RSSI threshold 0xE4 -> 0xDC (220)
#define HRF_VAL_PREAMBLELSB3           0x03	// preamble size LSB 3
#define HRF_VAL_PREAMBLELSB5           0x05	// preamble size LSB 5
#define HRF_VAL_SYNCCONFIG0            0x00     // sync word disabled
#define HRF_VAL_SYNCCONFIG1            0x80     // 1 byte  of tx sync
#define HRF_VAL_SYNCCONFIG2            0x88	// 2 bytes of tx sync
#define HRF_VAL_SYNCCONFIG3            0x90     // 3 bytes of tx sync
#define HRF_VAL_SYNCCONFIG4            0x98	// 4 bytes of tx sync
#define HRF_VAL_PAYLOADLEN255          0xFF	// max Length in RX, not used in Tx
#define HRF_VAL_PAYLOADLEN66           66	// max Length in RX, not used in Tx
#define HRF_VAL_FIFOTHRESH1            0x81	// Condition to start packet transmission: at least one byte in FIFO
#define HRF_VAL_FIFOTHRESH30           0x1E	// Condition to start packet transmission: wait for 30 bytes in FIFO


extern void HRF_writereg(uint8_t addr, uint8_t data);

extern uint8_t HRF_readreg(uint8_t addr);

extern void HRF_writefifo_burst(uint8_t* buf, uint8_t len);

extern HRF_RESULT HRF_readfifo_burst_cbp(uint8_t* buf, uint8_t buflen);

extern HRF_RESULT HRF_readfifo_burst_len(uint8_t* buf, uint8_t buflen);

extern HRF_RESULT HRF_checkreg(uint8_t addr, uint8_t mask, uint8_t value);

extern void HRF_pollreg(uint8_t addr, uint8_t mask, uint8_t value);

extern void HRF_clear_fifo(void);


#endif

/***** END OF FILE *****/

