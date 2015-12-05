/*****************************************************************************
 * GET/SET MODULE-LEVEL (GLOBAL) PYTHON VARIABLES BY NAME
 * handles module (re)loading, input/output conversions;
 * useful for passing data to/from codestrings (no args or return 
 * val)--load module, set inputs, run codestring, get outputs;
 * subtle thing: Python "s" output conversion code sets a C char* to 
 * the text in the middle of a Python string object, which may be
 * returned to the heap if decref'd--this api copies the text to a new
 * char array (with strdup) that the caller must free() when possible,
 * rather than assuming the caller can and will copy the result out;
 * could postpone the decref till next api call, but that's too subtle;
 *****************************************************************************/

#include "ppembed.h"
#include <stdarg.h>

int
PP_Convert_Result(PyObject *presult, char *resFormat, void *resTarget)
{
    if (presult == NULL)                /* error when run: fail */
        return -1;
    else
    if (resTarget == NULL) {            /* passed target=NULL: ignore result */
        Py_DECREF(presult);             /* procedures and stmts return None  */
        return 0;
    }
    else
    if (! PyArg_Parse(presult, resFormat, resTarget)) {  /* convert Python->C */
        Py_DECREF(presult);                              /* need not be tuple */
        return -1;                                       /* error in convert  */
    }
    else {
        if (strcmp(resFormat, "O") != 0) {     /* free object unless exported */
            if (strcmp(resFormat, "s") == 0) { /* copy string: caller owns it */
                char **target = resTarget;
                *target = strdup(*target); 
            }
            Py_DECREF(presult);
        }
        return 0;                     /* returns 0=success, -1=failure */
    }                                 /* if 0: C result in *resTarget  */
}                                     /* caller must decref if fmt="O" */
                                      /* caller must free() if fmt="s" */

int
PP_Get_Global(char *modname, char *varname, char *resfmt, void *cresult)
{
    PyObject *var;                                   /* "x = modname.varname" */
    var = PP_Load_Attribute(modname, varname);       /* var is incref'd */
    return PP_Convert_Result(var, resfmt, cresult);  /* convert var to C form */
}


int
PP_Set_Global(char *modname, char *varname, char *valfmt, ... /* cval(s) */) 
{
    int result;
    PyObject *module, *val;                     /* "modname.varname = val" */
    va_list cvals;
    va_start(cvals, valfmt);                    /* C args after valfmt */

    module = PP_Load_Module(modname);           /* get/load module */
    if (module == NULL) 
        return -1;
    val = Py_VaBuildValue(valfmt, cvals);       /* convert input to Python */
    va_end(cvals);
    if (val == NULL) 
        return -1;
    result = PyObject_SetAttrString(module, varname, val); 
    Py_DECREF(val);                             /* set global module var */
    return result;                              /* decref val: var owns it */
}                                               /* 0=success, varname set */
