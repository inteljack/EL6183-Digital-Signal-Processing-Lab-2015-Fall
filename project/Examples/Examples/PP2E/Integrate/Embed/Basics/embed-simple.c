/******************************************************* 
 * simple code strings: C acts like the interactive
 * prompt, code runs in __main__, no output sent to C;
 *******************************************************/

#include <Python.h>    /* standard API def */

main() {
    printf("embed-simple\n");
    Py_Initialize();
    PyRun_SimpleString("import usermod");                /* load .py file */
    PyRun_SimpleString("print usermod.message");         /* on python path */
    PyRun_SimpleString("x = usermod.message");           /* compile and run */
    PyRun_SimpleString("print usermod.transform(x)"); 
}
