/******************************************************
 * Swig module description file, for a C lib file.
 * Generate by saying "swig -python hellolib.i".   
 ******************************************************/

%module hellowrap

%{
#include <hellolib.h>
%}

extern char *message(char*);    /* or: %include "../HelloLib/hellolib.h"   */
                                /* or: %include hellolib.h, and use -I arg */
