/* precompile and run code-string validations, manual error messages */

#include <ppembed.h>
#include <stdio.h>
#include <string.h>
#include "ordersfile.h"

run_user_validation()
{                                 /* python's initialized automaticaly */
    int i, status, nbytes;        /* XXX should check status everywhere */
    char script[4096];            /* XXX should malloc a big-enough block */
    char *errors, *warnings;
    FILE *file;
    PyObject *bytecode;

    file = fopen("validate1.py", "r");        /* customizable validations */
    nbytes = fread(script, 1, 4096, file);    /* load python file text */
    script[nbytes] = '\0';
    bytecode = PP_Compile_Codestr(PP_STATEMENT, script);   /* precompile */
    if (bytecode == NULL) {
        printf("Python error during compilation.\n");
        PyErr_Print();  /* show traceback */
        return;
    }

    status = PP_Make_Dummy_Module("orders");  /* application's own namespace */
    for (i=0; i < numorders; i++) {
        printf("\n%d (%d, %d, '%s')\n", 
            i, orders[i].product, orders[i].quantity, orders[i].buyer);

        PP_Set_Global("orders", "PRODUCT",  "i", orders[i].product);   /* int */
        PP_Set_Global("orders", "QUANTITY", "i", orders[i].quantity);  /* int */
        PP_Set_Global("orders", "BUYER",    "s", orders[i].buyer);     /* str */

        status = PP_Run_Bytecode(bytecode, "orders", "", NULL);
        if (status == -1) {
            printf("Python error during validation.\n");
            PP_Fetch_Error_Text();
            printf("type  = '%s'\ninfo  = '%s'\ntrace = '%s'", 
                PP_last_error_type, PP_last_error_info, PP_last_error_trace);
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

main(int argc, char **argv)        /* C's on-top, Python's embedded */
{                                  /* but Python uses C extensions too */
    run_user_validation();         /* don't need argv in embedded code */
}
