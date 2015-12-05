/* run embedded module-function validations */

#include <ppembed.h>
#include <stdio.h>
#include <string.h>
#include "ordersfile.h"

run_user_validation() {
    int i, status;                /* should check status everywhere */
    char *errors, *warnings;      /* no file/string or namespace here */
    PyObject *results;

    for (i=0; i < numorders; i++) {
        printf("\n%d (%d, %d, '%s')\n", 
            i, orders[i].product, orders[i].quantity, orders[i].buyer);

        status = PP_Run_Function(                /* validate2.validate(p,q,b) */
                         "validate2", "validate",  
                         "O",          &results,
                         "(iis)",      orders[i].product, 
                                       orders[i].quantity, orders[i].buyer);
        if (status == -1) {
            printf("Python error during validation.\n");
            PyErr_Print();  /* show traceback */
            continue;
        }
        PyArg_Parse(results, "(ss)", &warnings, &errors);
        printf("errors:   %s\n", strlen(errors)? errors : "none"); 
        printf("warnings: %s\n", strlen(warnings)? warnings : "none"); 
        Py_DECREF(results);  /* ok to free strings */
        PP_Run_Function("inventory", "print_files", "", NULL, "()");    
    }
}

main(int argc, char **argv) {
    run_user_validation();
}
