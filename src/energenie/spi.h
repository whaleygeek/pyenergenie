/* spi.h  D.J.Whale  19/07/2014 */


#ifndef SPI_H
#define SPI_H


/***** INCLUDES *****/

//#include <time.h>


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
  unsigned char cs;
  unsigned char sclk;
  unsigned char mosi;
  unsigned char miso;

  unsigned char spol;
  unsigned char cpol;
  unsigned char cpha;

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

int spi_byte(int txbyte);

void spi_frame(unsigned char* pTx, unsigned char* pRx, unsigned char count);

void spi_finished(void);

#endif

/***** END OF FILE *****/
