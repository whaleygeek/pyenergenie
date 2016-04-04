/* spi.h  D.J.Whale  19/07/2014 */


#ifndef SPI_H
#define SPI_H


/***** INCLUDES *****/

#include "system.h"


/***** CONSTANTS *****/

#define SPI_CPOL0 0
#define SPI_CPOL1 1
#define SPI_SPOL0 0
#define SPI_SPOL1 1
#define SPI_CPHA0 0
#define SPI_CPHA1 1


/***** STRUCTURES *****/

typedef struct
{
  uint8_t cs;
  uint8_t sclk;
  uint8_t mosi;
  uint8_t miso;

  uint8_t spol;
  uint8_t cpol;
  uint8_t cpha;

  //struct timespec tSettle;
  //struct timespec tHold;
  //struct timespec tFreq;
  unsigned int tSettle;
  unsigned int tHold;
  unsigned int tFreq;
} SPI_CONFIG;



/***** FUNCTION PROTOTYPES *****/

void spi_init_defaults(void);

void spi_init(SPI_CONFIG* pConfig);

void spi_select(void);

void spi_deselect(void);

int spi_byte(uint8_t txbyte);

void spi_frame(uint8_t* pTx, uint8_t* pRx, uint8_t count);

void spi_finished(void);

#endif

/***** END OF FILE *****/
