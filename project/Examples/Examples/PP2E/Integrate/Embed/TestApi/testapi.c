/********************************************************************** 
* test program for basic and 'ppembed' extended API calls.
* this includes a "main" function: C is on top in this program.
**********************************************************************/

#include <ppembed.h>
#define TRACE(msg) printf("\n%s\n", msg);


main(argc, argv)
int argc;
char **argv;
{
    printf("Hello from C.\n");
    Py_Initialize();              /* initialize embedded python libraries */
    PySys_SetArgv(argc, argv);    /* optional: export command args to python */
    BASIC_EMBEDDING();
    EMBEDDED_CALL_API();
    printf("Bye from C.\n");
    Py_Exit(0);                   /* optional: runs sys.exitfunc handler */
}


BASIC_EMBEDDING()         /* test low-level interfaces */
{
    PyObject *module, *dict, *pstack;

    /********************************************************************
     * run code-strings in default namespace (module '__main__'); 
     * uses embedding + extending: os/sys use C extension modules;
     * can call PyRun_SimpleString, PyRun_String, PyEval_CallObject..
     ********************************************************************/

    TRACE("SIMPLE STRINGS")
    PyRun_SimpleString("import sys, os");
    PyRun_SimpleString("print 'Hello,', os.environ['USER'] + '.'"); 
    PyRun_SimpleString("print 'Args: ', sys.argv");
    PyRun_SimpleString("print 'Plat: ', sys.platform");
    PyRun_SimpleString("print 'Path: ', sys.path[0:3], '...'");

    /********************************************************************
     * use the stack-type extension in embedded code; PyRun_String uses
     * explicit name-spaces and parse-modes; the PyRun_String results 
     * are None, but they should really be DECREF'd  and return values 
     * should be checked for NULL (a python error/exception occurred);
     ********************************************************************/

    TRACE("STACK EXTENSION")
    module = PyImport_AddModule("__main__");             /* fetch a module */
    dict   = PyModule_GetDict(module);                   /* get its __dict__ */

    PyRun_String("from stacktype import *", Py_file_input, dict, dict);
    PyRun_String("x = Stack()", Py_file_input, dict, dict);

    PyRun_String("for c in 'SPAM':\n"                           /* multi-line */
                   "\tx.push(c)\n", Py_file_input, dict, dict); /* stmts okay */
    PyRun_String("print x, len(x)", Py_file_input, dict, dict);     

    /* make a new instance */              
    pstack = PyRun_String("Stack()", Py_eval_input, dict, dict); 
    PyObject_Print(pstack, stdout, 0);
    Py_DECREF(pstack);
}


EMBEDDED_CALL_API()                  /* test ppembed enhanced wrappers */
{
    int i, status, result;
    char *strres;                    /* actual text is stored in python */ 
    PyObject *pobject1, *pobject2;   /* raw python objects: 'O' output codes */
    
    /********************************************************************
     * use the run_codestr wrapper like PyRun_SimpleString:
     * run string in module __main__ (since the module name argument is 
     * NULL), with no result (since this is a statement: 2nd NULL arg);
     * also see inventory examples for dummy-module creation and use; 
     ********************************************************************/

    PP_Run_Codestr(PP_STATEMENT, "print 'Hello api world'", NULL, "", NULL);

    /********************************************************************
     * turn on dynamic reload-on-call mode, and call a Python function in 
     * a module file; the file can be changed between the five calls here;
     * calls "testapi.func(4, 8)": see testapi_c.py for equiv in Python;
     * note that this imports testapi in C, and adds it to sys.modules, 
     * but doesn't add the name "testapi" to any other Python module:
     ********************************************************************/

    TRACE("DYNAMIC RELOADING")
    PP_RELOAD = 1;
    for (i=0; i < 5; i++) {
        status = PP_Run_Function("testapi", "func", "i", &result, "(ii)", 4, 8);
        if (status == -1) {
            printf("Error running func\n");
            PyErr_Print();                       /* python stack dump */
        }
        else
            printf("result => %d\n", result);
        if (i < 4) {
            printf("change testapi.py now...");     /* edit in another window */
            getchar();                              /* wait for a keypress */
        }
    }

    /********************************************************************
     * turn on dynamic debugging, run string, function, bytecode, object; 
     * pdb stops execution as soon as the embedded code starts: set 
     * breakponts, step through code, etc.; all run "testapi.func(4, 8)",
     * the Python "func" function which is defined in file testapi.py;
     ********************************************************************/

#define announce(test) result=-1; printf("Debug %s--type s to step...\n", test)
#define showresult printf("C status, result => %d, %d\n\n", status, result)

    TRACE("DYNAMIC DEBUGGING")
    PP_RELOAD = 0;
    PP_DEBUG  = 1;       /* could do both at once */

    announce("code string");
    status = PP_Run_Codestr(PP_EXPRESSION, 
                           "func(4, 8)", "testapi", "i", &result);
    showresult;

    announce("module function call");
    status = PP_Run_Function("testapi", "func", "i", &result, "(ii)", 4, 8);
    showresult;

    announce("compiled bytecode");
    pobject1 = PP_Compile_Codestr(PP_EXPRESSION, "func(4, 8)");
    status   = PP_Run_Bytecode(pobject1, "testapi", "i", &result);
    Py_XDECREF(pobject1);
    showresult;

    /* could also fetch with "func" string in "testapi", or PP_Get_Global */
    announce("direct object call");
    pobject1 = PP_Load_Attribute("testapi", "func");
    status   = PP_Run_Known_Callable(pobject1, "i", &result, "(ii)", 4, 8);
    Py_XDECREF(pobject1);
    showresult;

    PP_DEBUG = 0;

    /********************************************************************
     * a few object attribute tests: fetches sys module by name, which 
     * was already imported in module __main__ by the basic embedding 
     * tests; in general, return values should be checked for errors too;
     * the interactive command line also runs in module __main__; 
     ********************************************************************/
 
    TRACE("OBJECT ATTRIBUTES")
    PP_Run_Command_Line("check sys.version");                    /* __main__ */
    PP_Run_Codestr(PP_EXPRESSION, "sys", NULL, "O", &pobject1);  /*  .sys */
    PP_Get_Member(pobject1, "version", "s", &strres);            /*  .version */
    printf("fetched sys.version => %.50s...\n", strres);
    free(strres);

    PP_Set_Member(pobject1, "version", "s", "2.0 (2001?)");      /* change it */
    PP_Run_Codestr(PP_STATEMENT, 
        "print 'changed sys.version =>', sys.version", NULL, "", NULL);

    /* run sys.modules.has_key('testapi') */
    PP_Get_Member(pobject1, "modules", "O", &pobject2);

    PP_Run_Method(pobject2, "has_key", "i", &result, "(s)", "testapi"); 
    printf("sys.modules.has_key('testapi')  result => %d\n", result);

    PP_Run_Method(pobject2, "has_key", "i", &result, "(s)", "nonesuch"); 
    printf("sys.modules.has_key('nonesuch') result => %d\n", result);
    Py_XDECREF(pobject2);

    /* run sys.stdout.write('<stdout text>\n') */
    printf("Sending text to sys.stdout.write...");
    PP_Get_Member(pobject1, "stdout", "O", &pobject2); 
    PP_Run_Method(pobject2, "write", "", NULL, "(s)", "<stdout text>\n");
   
    Py_XDECREF(pobject1);       /* in functions, free raw python objects */
    Py_XDECREF(pobject2);       /* passed out with "O" format code */
}                               /* plus any strings from "s" code  */
