
#include <arduino.h>
#include "system.h"
#include "delay.h"

void delaysec(uint8_t s)
{
  int i;
  for (i=0; i<s; i++)
  {
    delay(1000); // ms
  }
}


void delayus(unsigned int us)
{
  delayMicroseconds(us);
}

/***** END OF FILE *****/


