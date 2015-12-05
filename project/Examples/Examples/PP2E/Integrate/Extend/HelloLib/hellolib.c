/********************************************************************* 
 * A simple C library file, with a single function, "message",
 * which is to be made available for use in Python programs.
 * There is nothing about Python here--this C function can be 
 * called from a C program, as well as Python (with glue code).
 *********************************************************************/

#include <string.h>
#include <hellolib.h>

static char result[64];                  /* this isn't exported */

char *
message(char *label)                     /* this is exported */
{                
    strcpy(result, "Hello, ");           /* build up C string */
    strcat(result, label);               /* add passed-in label */
    return result;                       /* return a temporary */
}

