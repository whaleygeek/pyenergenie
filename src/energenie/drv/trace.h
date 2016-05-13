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

//#define TRACE_POSIX

/* POSIX IMPLEMENTATION */
/* Printf is not available on some platforms, or not very efficient.
 * These macros make it possible to re-map I/O to more efficient functions.
 */

#if defined(TRACE_POSIX)
#include <stdio.h>
#include <stdlib.h>

#define TRACE
#define TRACE_OUTS(S)   do{printf("%s", S);fflush(stdout);} while (0)
#define TRACE_OUTN(N)   do{printf("%d", (unsigned int)N);fflush(stdout);} while (0)
#define TRACE_OUTC(C)   putc(C, stdout)
#define TRACE_NL()      do{TRACE_OUTC('\n');fflush(stdout);} while (0)
#define TRACE_FAIL(msg) do{fprintf(stderr, "%s", msg);exit(-1);} while (0)

#else // no trace defined

#define TRACE_OUTS(S)
#define TRACE_OUTN(N)
#define TRACE_OUTC(C)
#define TRACE_NL()
#define TRACE_FAIL(M)
#endif
#endif

/***** END OF FILE *****/

