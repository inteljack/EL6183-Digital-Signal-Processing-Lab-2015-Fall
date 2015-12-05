/* run embedded module-function validations */
/* reuse python file-load routine: returns list of tuples, */
/* so use Python PyObject object access functions to process */
/* also see abstract.h and lower-level Python object .h files */

#include <ppembed.h>
#include <stdio.h>
#include <string.h>

run_user_validation(char *ofile)
{
    int i, status;                /* should also check status everywhere */
    char *errors, *warnings;
    PyObject *results, *orders, *nextorder=NULL;
    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('..')");
    PP_Run_Function("inventory", "load_orders", "O", &orders, "(s)", ofile);

    PP_Run_Function("inventory", "print_files", "", NULL, "()");    
    for (i=0; i < PyObject_Length(orders); i++) {                   /* len(x) */
        Py_XDECREF(nextorder);
        nextorder = PyObject_GetItem(orders, PyInt_FromLong(i));    /* x[i] */
        printf("\n%d ", i);
        PyObject_Print(nextorder, stdout, 0);
        printf("\n");

        status = PP_Run_Function(                /* validate2.validate(p,q,b) */
                         "validate2", "validate",  
                         "O",          &results,
                         "O",          nextorder);
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

main(int argc, char **argv)
{
    char ofile[64];
    if (argc == 1)
        strcpy(ofile, "Data/ordersfile.data");
    else {
        strcpy(ofile, "Data/");
        strcat(ofile, argv[1]);
    }
    run_user_validation(ofile);
}
