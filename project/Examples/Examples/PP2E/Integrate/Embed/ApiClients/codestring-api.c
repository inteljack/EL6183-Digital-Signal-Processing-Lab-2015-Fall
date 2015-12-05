#include "ppembed.h"
#include <stdio.h>
                                          /* with ppembed high-level api */
main() { 
    char *cstr;
    int err = PP_Run_Codestr(
                    PP_EXPRESSION,                       /* expr or stmt?  */
                    "upper('spam') + '!'", "string",     /* code, module   */
                    "s", &cstr);                         /* expr result    */
    printf("%s\n", (!err) ? cstr : "Can't run string");  /* and free(cstr) */
}
