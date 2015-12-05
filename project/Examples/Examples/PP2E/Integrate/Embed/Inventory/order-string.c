/* run embedded code-string validations */

#include <ppembed.h>
#include <stdio.h>
#include <string.h>
#include "ordersfile.h"

run_user_validation()
{                                 /* python is initialized automatically */
    int i, status, nbytes;        /* caveat: should check status everywhere */
    char script[4096];            /* caveat: should malloc a big-enough block */
    char *errors, *warnings;
    FILE *file;

    file = fopen("validate1.py", "r");        /* customizable validations */
    nbytes = fread(script, 1, 4096, file);    /* load python file text */
    script[nbytes] = '\0';

    status = PP_Make_Dummy_Module("orders");  /* application's own namespace */
    for (i=0; i < numorders; i++) {           /* like making a new dictionary */
        printf("\n%d (%d, %d, '%s')\n", 
            i, orders[i].product, orders[i].quantity, orders[i].buyer);

        PP_Set_Global("orders", "PRODUCT",  "i", orders[i].product);   /* int */
        PP_Set_Global("orders", "QUANTITY", "i", orders[i].quantity);  /* int */
        PP_Set_Global("orders", "BUYER",    "s", orders[i].buyer);     /* str */

        status = PP_Run_Codestr(PP_STATEMENT, script, "orders", "", NULL);
        if (status == -1) {
            printf("Python error during validation.\n");
            PyErr_Print();  /* show traceback */
            continue;
        }

        PP_Get_Global("orders", "ERRORS",   "s", &errors);     /* can split */
        PP_Get_Global("orders", "WARNINGS", "s", &warnings);   /* on blanks */

        printf("errors:   %s\n", strlen(errors)? errors : "none"); 
        printf("warnings: %s\n", strlen(warnings)? warnings : "none"); 
        free(errors); free(warnings);
        PP_Run_Function("inventory", "print_files", "", NULL, "()"); 
    }
}

main(int argc, char **argv)        /* C is on top, Python is embedded */
{                                  /* but Python can use C extensions too */
    run_user_validation();         /* don't need sys.argv in embedded code */
}
