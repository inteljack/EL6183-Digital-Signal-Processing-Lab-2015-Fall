/*****************************************************************************
 * RUN EMBEDDED CODE-STRINGS 
 * handles debugging, module (re)loading, namespaces, output conversions;
 * pbd.runeval returns a value: "eval(expr + '\n', globals, locals)";
 * pdb.run is just a statement: "exec cmd + '\n' in globals, locals"
 * New tools: precompiling strings to bytecode, running bytecode; 
 *****************************************************************************/

#include "ppembed.h"
#include <compile.h>
#include <eval.h>


int
PP_Run_Codestr(PPStringModes mode, char *code,  /* expr or stmt string */
               char *modname,                   /* loads module if needed */
               char *resfmt, void *cresult)     /* converts expr result to C */
{
    /* run a string of Python code */
    int parse_mode;                             /* "eval(code, d, d)", or */
    PyObject *module, *dict, *presult;          /* "exec code in d, d" */

    module = PP_Load_Module(modname);           /* get module, init python */
    if (module == NULL)                         /* not incref'd */
        return -1;
    dict = PyModule_GetDict(module);            /* get dict namespace */
    if (dict == NULL)                           /* not incref'd */
        return -1;

    parse_mode = (mode == PP_EXPRESSION ? Py_eval_input : Py_file_input);
    if (PP_DEBUG) 
        presult = PP_Debug_Codestr(mode, code, dict);         /* run in pdb */
    else 
        presult = PyRun_String(code, parse_mode, dict, dict); /* eval direct */
                                                              /* increfs res */
    if (mode == PP_STATEMENT) {
        int result = (presult == NULL? -1 : 0);          /* stmt: 'None' */
        Py_XDECREF(presult);                             /* ignore result */
        return result;
    }
    return PP_Convert_Result(presult, resfmt, cresult);  /* expr val to C */
}


PyObject *
PP_Compile_Codestr(PPStringModes mode,    /* precompile string to bytecode */
                   char *codestr)         /* pass result to PP_Run_Bytecode */
{
    int start;
    Py_Initialize();
    switch (mode) {
    case PP_STATEMENT:
        start = Py_file_input; break;
    case PP_EXPRESSION:
        start = Py_eval_input; break;
    default:
        start = Py_single_input;  /* prints expr results */
    }
    return Py_CompileString(codestr, "<PP_Compile_Codestr>", start);
}


int
PP_Run_Bytecode(PyObject *codeobj,           /* run compiled bytecode object */
                char     *modname,           /* in named module's namespace */
                char     *resfmt, void *restarget)
{
    PyObject *presult, *module, *dict;

    if (! PyCode_Check(codeobj))             /* make sure it's bytecode */
        return -1;
    module = PP_Load_Module(modname);        /* get module, init python */
    if (module == NULL)                      /* not incref'd */
        return -1;
    dict = PyModule_GetDict(module);         /* get dict namespace */
    if (dict == NULL)                        /* not incref'd */
        return -1;
    if (PP_DEBUG)
        presult = PP_Debug_Bytecode(codeobj, dict);        /* run in pdb */
    else
        presult = PyEval_EvalCode((PyCodeObject *)codeobj, dict, dict);
    return PP_Convert_Result(presult, resfmt, restarget);  /* expr val to C */
}


/**************************************************************************
 * subtle things:
 * 1) pdb.run and pdb.runeval both accept either a string or a
 * compiled code object, just because they call the built in exec and 
 * eval(), which allow either form;  further, eval() works on code
 * objects compiled as either expressions or statements, but returns
 * None as the result of statements, so we don't need to distinguish 
 * between expressions and statements here again for bytecode (we 
 * did when compiling); the equivalents in Python code:
 *     >>> a = 1
 *     >>> s = compile('x = 1', '', 'exec')
 *     >>> e = compile('a + 1', '', 'eval')
 *     >>> print eval(e)
 *     2
 *     >>> print eval(s)
 *     None
 * on the other hand, we can't blindly use pdb.runeval when dealing  
 * with uncompiled strings, because eval() fails on statement strings;
 *
 * 2) in 1.5, if you debug a string or bytecode object in a module's
 * namespace where you've already debugged once, you may see a bogus
 * return value on entry which is left over from a prior debug; this
 * is because pdb leaves a '__return__' attribute in the module's
 * dictionary, which may be a pdb bug, but we work around it here by
 * manually deleting __return__ if present before starting pdb again;
 * only happens for strings--function namespaces aren't persistent;
 **************************************************************************/


static void fixPdbRetval(PyObject *moddict) 
    { if (PyDict_DelItemString(moddict, "__return__")) PyErr_Clear(); }


PyObject *
PP_Debug_Codestr(PPStringModes mode, char *codestring, PyObject *moddict)
{
    int res;
    PyObject *presult;
    char *pdbname = (mode == PP_EXPRESSION ? "runeval" : "run");
    fixPdbRetval(moddict);
                                      /* pass code to a pbd.py function    */
    res = PP_Run_Function(            /* "pdb.run(stmt, gdict, ldict)"     */
             "pdb",    pdbname,       /* "pdb.runeval(expr, gdict, ldict)" */
             "O",      &presult,
             "(sOO)",  codestring, moddict, moddict); 
    return (res != 0) ? NULL : presult;     /* return null or increfd object */
}


PyObject *
PP_Debug_Bytecode(PyObject *codeobject, PyObject *moddict)
{
    int res;
    PyObject *presult;
    fixPdbRetval(moddict);
    res = PP_Run_Function(            /* "pdb.runeval(codeobj, gdict, ldict)" */
             "pdb",    "runeval",     /* accepts string|code, code=stmt|expr  */
             "O",      &presult,
             "(OOO)",  codeobject, moddict, moddict); 
    return (res != 0) ? NULL : presult;     /* null if error in run_function */
}

