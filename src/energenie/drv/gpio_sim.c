/* gpio_sim.c  D.J.Whale  04/04/2016
 * 
 * A very simple interface to a simulated GPIO port with minimal platform dependencies.
 */

/***** INCLUDES *****/

#include <stdio.h> // OPTIONAL
#include "gpio.h"


/***** CONFIGURATION *****/

#define GPIO_MAX      20
#define GPIO_DEBUG
//#define GPIO_LOOPBACK


/* Printf is not available on some platforms, or not very efficient.
 * These macros make it possible to re-map I/O to more efficient functions.
 */

#define OUTS(s)  printf("%s", s)
#define OUTN(n)  printf("%d", (unsigned int)n)
#define OUTC(c)  putc(c, stdout)
#define NL()     OUTC('\n')


/***** VARIABLES *****/

static uint8_t gpio_out[GPIO_MAX] = {0};
static uint8_t gpio_in[GPIO_MAX]  = {0};


void gpio_init()
{
  // Nothing to do
}


void gpio_setin(uint8_t g)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:in:%d\n", g);
    OUTS("gpio:in");
    OUTN(g);
    NL();
#endif
}


void gpio_setout(uint8_t g)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:out:%d\n", g);
    OUTS("gpio:out:");
    OUTN(g);
    NL();
#endif
}


void gpio_high(uint8_t g)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:high:%d\n", g);
    OUTS("gpio:high:");
    OUTN(g);
    NL();
#endif

    gpio_out[g] = 1;

#if defined(GPIO_LOOPBACK)
    gpio_in[g] = 1;
#endif
}


void gpio_low(uint8_t g)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:low:%d\n", g);
    OUTS("gpio:low");
    OUTN(g);
    NL();
#endif

    gpio_out[g] = 0;

#if defined(GPIO_LOOPBACK)
    gpio_in[g] = 0;
#endif
}


void gpio_write(uint8_t g, uint8_t v)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:write:%d=%d\n", g, v);
    OUTS("gpio:write:");
    OUTN(g);
    OUTC('=');
    OUTN(v);
    NL();
#endif

    gpio_out[g] = v;

#if defined(GPIO_LOOPBACK)
    gpio_in[g] = v;
#endif
}


uint8_t gpio_read(uint8_t g)
{
#if defined(GPIO_DEBUG)
    //printf("gpio:read:%d=%d\n")
    OUTS("gpio:read:");
    OUTN(g);
    OUTC('=');
    OUTN(gpio_in[g]);
    NL();
#endif
    return gpio_in[g];
}


void gpio_finished(void)
{
    // Nothing to do
}


void gpio_mock_set_in(uint8_t g, uint8_t v)
{
    gpio_in[g] = v;
}


uint8_t gpio_mock_get_out(uint8_t g)
{
    return gpio_out[g];
}


/***** END OF FILE *****/
