/*********************************************/
/* embed (call) Python code from a C program */
/*********************************************/

#include <Python.h>

main(argc, argv)                          /* compile and link with python */
int argc;                                 /* libs to create an executable */
char **argv;                              /* add '.' to PYTHONPATH for .so */
{
    printf("Hello from C.\n");
    Py_Initialize();                                      /* init python */
    PyRun_SimpleString("print 'Hello from Python!'");     /* call python api */
    PyRun_SimpleString("import sys; print sys.platform"); /* run Python code */

    /* use our C extension module */
    PyRun_SimpleString("from cenviron import *");         /* loads .so now */
    PyRun_SimpleString(                                   /* tab to indent */
           "for i in range(5):\n"
                "\tputenv('USER', 'T.Howle the ' + `i`)\n"
                "\tprint getenv('USER')\n\n" );

    PyRun_SimpleString("print 'Bye from Python!'");
    printf("Bye from C.\n");
}

