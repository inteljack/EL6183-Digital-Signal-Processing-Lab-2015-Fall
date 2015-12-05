/*****************************************************************************
 * PYTHON EXCEPTION INFORMATION ACCESS
 * fetch Python-related error info (type, value);
 * after an API call returns an exception indicator, call 
 * PP_Fetch_Error_Text, then get text from the 3 char[]'s;
 * note: calling PyErr_Fetch() clears/erases the current 
 * exception in the Python system, as does PyErr_Print(), 
 * so you should call one of these, one time, per exception:
 * caveats: not thread-specific since saves data in globals,
 * and only exports traceback object (the exception type and 
 * data are converted to text strings and disgarded);  the 
 * PyErr_Print() built-in also does a bit more on syntax errors,
 * and sends its text to sys.stderr: in principle, we could
 * assign stderr to a StringIO object and call PyErr_Print, but
 * the code here makes the 3 exception components more distinct;
 *****************************************************************************/

#include <Python.h>
#include <string.h>
#define MAX 1024

/* exception text is here after PP_Fetch_Error_Text call */
char PP_last_error_type[MAX];           /* exception name text */
char PP_last_error_info[MAX];           /* exception data text */
char PP_last_error_trace[MAX];          /* exception traceback text */
PyObject *PP_last_traceback = NULL;     /* saved exception traceback object */


void PP_Fetch_Error_Text()
{
    char *tempstr;
    PyObject *errobj, *errdata, *errtraceback, *pystring;

    /* get latest python exception information */
    /* this also clears the current exception  */

    PyErr_Fetch(&errobj, &errdata, &errtraceback);       /* all 3 incref'd */


    /* convert type and data to strings */
    /* calls str() on both to stringify */

    pystring = NULL;
    if (errobj != NULL &&
       (pystring = PyObject_Str(errobj)) != NULL &&      /* str(errobj) */
       (PyString_Check(pystring)) )                      /* str() increfs */
    {
        strncpy(PP_last_error_type, PyString_AsString(pystring), MAX); /*Py->C*/
        PP_last_error_type[MAX-1] = '\0';
    }
    else 
        strcpy(PP_last_error_type, "<unknown exception type>");
    Py_XDECREF(pystring);


    pystring = NULL;
    if (errdata != NULL &&
       (pystring = PyObject_Str(errdata)) != NULL &&     /* str(): increfs */
       (PyString_Check(pystring)) )
    {
        strncpy(PP_last_error_info, PyString_AsString(pystring), MAX); /*Py->C*/
        PP_last_error_info[MAX-1] = '\0';
    }
    else 
        strcpy(PP_last_error_info, "<unknown exception data>");
    Py_XDECREF(pystring);


    /* convert traceback to string */ 
    /* print text to a StringIO.StringIO() internal file object, then */
    /* fetch by calling object's .getvalue() method (see lib manual); */

    pystring = NULL;
    if (errtraceback != NULL &&
       (PP_Run_Function("StringIO", "StringIO", "O", &pystring, "()") == 0) &&
       (PyTraceBack_Print(errtraceback, pystring) == 0) &&
       (PP_Run_Method(pystring, "getvalue", "s", &tempstr, "()") == 0) )
    {
        strncpy(PP_last_error_trace, tempstr, MAX); 
        PP_last_error_trace[MAX-1] = '\0';
        free(tempstr);  /* it's a strdup */
    }
    else 
        strcpy(PP_last_error_trace, "<unknown exception traceback>"); 
    Py_XDECREF(pystring);


    Py_XDECREF(errobj);
    Py_XDECREF(errdata);               /* this function owns all 3 objects */
    Py_XDECREF(PP_last_traceback);     /* they've been NULL'd out in Python */ 
    PP_last_traceback = errtraceback;  /* save/export raw traceback object */
}

