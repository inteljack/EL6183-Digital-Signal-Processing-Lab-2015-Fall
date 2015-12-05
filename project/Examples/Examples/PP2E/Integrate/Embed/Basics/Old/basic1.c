#include <Python.h>    /* standard API def */

main() {
    /* acts like the interactive prompt */
    printf("basic1\n");
    Py_Initialize();
    PyRun_SimpleString("import string");
    PyRun_SimpleString("print string.uppercase"); 
    PyRun_SimpleString("x = string.uppercase"); 
    PyRun_SimpleString("print string.lower(x)"); 
}
