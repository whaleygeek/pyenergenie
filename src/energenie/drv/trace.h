/* trace.h  04/04/2016  D.J.Whale
 *
 * Simple trace output.
 *
 * On some platforms this is just printf.
 * On others it might write to a serial port
 * On others it might write to a trace buffer viewed in an emulator
 * It could be configured to do nothing.
 */

#ifndef _TRACE_H
#define _TRACE_H

/* POSIX IMPLEMENTATION */
/* Printf is not available on some platforms, or not very efficient.
 * These macros make it possible to re-map I/O to more efficient functions.
 */

#include <stdio.h>

#define TRACE_OUTS(s)  printf("%s", s)
#define TRACE_OUTN(n)  printf("%d", (unsigned int)n)
#define TRACE_OUTC(c)  putc(c, stdout)
#define TRACE_NL()     TRACE_OUTC('\n')

#define TRACE_FAIL(msg) do { \
  fprintf(stderr, "%s", msg); \
  exit(-1); \
} while (0)

#endif

/***** END OF FILE *****/

