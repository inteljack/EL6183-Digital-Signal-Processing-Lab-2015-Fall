/*****************************************************************************
 * RUN EMBEDDED OBJECT METHODS, ACCESS OBJECT ATTRIBUTES 
 * handles attribute fetch, debugging, input/output conversions; 
 * there is no module to reload here: assumes a known object;
 *****************************************************************************/

#include "ppembed.h"
#include <stdarg.h>

int
PP_Run_Method(PyObject *pobject,  char *method,
                  char *resfmt,   void *cresult,        /* convert to c/c++ */
                  char *argfmt,   ... /* arg,... */ )   /* convert to python */
{
    PyObject *pmeth, *pargs, *presult;
    va_list argslist;                              /* "pobject.method(args)" */
    va_start(argslist, argfmt);

    Py_Initialize();                               /* init if first time */
    pmeth = PyObject_GetAttrString(pobject, method);  
    if (pmeth == NULL)                             /* get callable object */
        return -1;                                 /* bound method? has self */
    pargs = Py_VaBuildValue(argfmt, argslist);     /* args: c->python */
    if (pargs == NULL) {
        Py_DECREF(pmeth);
        return -1;
    }
    if (PP_DEBUG)                                    /* debug it too? */ 
        presult = PP_Debug_Function(pmeth, pargs); 
    else 
        presult = PyEval_CallObject(pmeth, pargs);   /* run interpreter */

    Py_DECREF(pmeth);
    Py_DECREF(pargs);
    return PP_Convert_Result(presult, resfmt, cresult);    /* to C format */
}
 

int
PP_Get_Member(PyObject *pobject, char *attrname,
                  char *resfmt,  void *cresult)         /* convert to c/c++ */
{
    PyObject *pmemb;                                    /* "pobject.attrname" */
    Py_Initialize();                        
    pmemb = PyObject_GetAttrString(pobject, attrname);  /* incref'd */
    return PP_Convert_Result(pmemb, resfmt, cresult);   /* to C form, decrefs */
}
 

int
PP_Set_Member(PyObject *pobject, char *attrname,
                  char *argfmt,  ... /* arg,... */ )    /* convert to python */
{
    int result;
    PyObject *pval;
    va_list argslist;                             /* "pobject.attrname = v" */
    va_start(argslist, argfmt);
    Py_Initialize();                              /* init if first time */
    pval = Py_VaBuildValue(argfmt, argslist);     /* input: C->Python */
    if (pval == NULL) 
        return -1;
    result = PyObject_SetAttrString(pobject, attrname, pval);     /* setattr */
    Py_DECREF(pval); 
    return result;
}
