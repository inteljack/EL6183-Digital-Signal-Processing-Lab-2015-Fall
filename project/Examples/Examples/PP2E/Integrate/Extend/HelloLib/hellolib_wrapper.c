/******************************************************************** 
 * A simple C extension module for Python, called "hellowrap". 
 * Wraps an existing C library function (coded in hellolib.c),
 * instead of embedding processing logic within the method
 * functions here.  This is typical of integrating existing 
 * C services for use by Python programs.  It's also exactly
 * the sort of wrapper code that SWIG was designed to generate 
 * automatically; see ..\Swig, or the extending chapter;
 ********************************************************************/

#include <Python.h>
#include <hellolib.h>

/* module functions */
static PyObject *                                 /* returns object */
wrap_message(PyObject *self, PyObject *args)      /* self unused in modules */
{                                                 /* args from python call */
    char *fromPython, *result;
    if (! PyArg_Parse(args, "(s)", &fromPython))  /* convert Python -> C */
        return NULL;                              /* null=raise exception */
    else {
        result = message(fromPython);             /* <== call C lib function */
        return Py_BuildValue("s", result);        /* convert C -> Python */
    }
}

/* registration table  */
static struct PyMethodDef mymethods[] = {
    {"message", wrap_message, 1},      /* method name, C func ptr */
    {NULL, NULL}                       /* end of table marker */
};

/* module initializer */
void inithellowrap()                   /* called on first import */
{                                      /* names here must match .so file name */
    (void) Py_InitModule("hellowrap", mymethods); 
}
