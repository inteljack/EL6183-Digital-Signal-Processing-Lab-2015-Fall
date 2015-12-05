/*****************************************************************************
 * RUN EMBEDDED MODULE FUNCTIONS 
 * handles module (re)import, debugging, input/output conversions;  
 * note: also useful for calling classes (and C type constructors) at the 
 * top-level of a module to make Python instances: use class-name (or type
 * constructor function name) and 'O' result convert-code to get raw object;
 * use argfmt="()" for no args, cresult='NULL' for no result (procedure);
 * New tools: support for calling known Python objects directly;
 *****************************************************************************/

#include "ppembed.h"
#include <stdarg.h>


int
PP_Run_Function(char *modname, char *funcname,          /* load from module */
                char *resfmt,  void *cresult,           /* convert to c/c++ */
                char *argfmt,  ... /* arg, arg... */ )  /* convert to python */
{
    /* call a function or class in a module */
    PyObject *func, *args, *presult;
    va_list argslist;
    va_start(argslist, argfmt);                   /* "modname.funcname(args)" */

    func = PP_Load_Attribute(modname, funcname);  /* may reload; incref'd */
    if (func == NULL)                             /* func or class or C type */
        return -1;
    args = Py_VaBuildValue(argfmt, argslist);     /* convert args to python */
    if (args == NULL) {                           /* args incref'd */
        Py_DECREF(func);
        return -1;
    }
    if (PP_DEBUG && strcmp(modname, "pdb") != 0)    /* debug this call? */
        presult = PP_Debug_Function(func, args);    /* run in pdb; incref'd */
    else
        presult = PyEval_CallObject(func, args);    /* run function; incref'd */

    Py_DECREF(func);
    Py_DECREF(args);                                    /* result may be None */
    return PP_Convert_Result(presult, resfmt, cresult); /* convert result to C*/
}


PyObject *
PP_Debug_Function(PyObject *func, PyObject *args)
{
    int oops, res;
    PyObject *presult;

    /* expand tuple at front */
    oops = _PyTuple_Resize(&args, (1 + PyTuple_Size(args)), 1); 
    oops |= PyTuple_SetItem(args, 0, func);   
    if (oops) 
        return NULL;                        /* "args = (funcobj,) + (arg,..)" */

    res = PP_Run_Function(                  /* "pdb.runcall(funcobj, arg,..)" */
                 "pdb",  "runcall",         /* recursive run_function */
                 "O",    &presult,
                 "O",     args);            /* args already is a tuple */
    return (res != 0) ? NULL : presult;     /* errors in run_function? */
}                                           /* presult not yet decref'd */


int
PP_Run_Known_Callable(PyObject *object,               /* func|class|method */
                      char *resfmt, void *cresult,    /* skip module fetch */
                      char *argfmt, ... /* arg,.. */) /* convert args, result */
{
    /* call a known callable object */
    PyObject *args, *presult;
    va_list argslist;
    va_start(argslist, argfmt);                     /* "return object(args)" */

    Py_Initialize(); 
    args = Py_VaBuildValue(argfmt, argslist);       /* convert args to python */
    if (args == NULL)                               /* args incref'd */
        return -1;
    if (PP_DEBUG)                                   /* debug this call? */
        presult = PP_Debug_Function(object, args);  /* run in pdb; incref'd */
    else
        presult = PyEval_CallObject(object, args);  /* run function; incref'd */

    Py_DECREF(args);                                    /* result may be None */
    return PP_Convert_Result(presult, resfmt, cresult); /* convert result to C*/
}

