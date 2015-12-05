/********************************************************************** 
* Package reference/reload version (see ../testapi.c for details).
* Replaces "testapi" module name string with name "pkgdir.testapi".
**********************************************************************/

#include <ppembed.h>
#define TRACE(msg) printf("\n%s\n", msg);


main(argc, argv)
int argc;
char **argv;
{
    printf("Hello from C.\n");
    EMBEDDED_CALL_API();          /* basic embedding works the same way */
    printf("Bye from C.\n");
    Py_Exit(0);                   /* optional: runs sys.exitfunc handler */
}


EMBEDDED_CALL_API()                  /* test ppembed enhanced wrappers */
{
    int i, status, result;
    char *strres;                    /* actual text is stored in python */ 
    PyObject *pobject1, *pobject2;   /* raw python objects: 'O' output codes */
    
    /********************************************************************
     * use the run_codestr wrapper like PyRun_SimpleString:
     ********************************************************************/

    PP_Run_Codestr(PP_STATEMENT, "print 'Hello api world'", NULL, "", NULL);
    PP_Run_Codestr(PP_STATEMENT, "import sys", NULL, "", NULL);

    /********************************************************************
     * turn on dynamic reload-on-call mode, and call a Python function in 
     * a module file; the file can be changed between the five calls here;
     ********************************************************************/

    TRACE("DYNAMIC RELOADING")
    PP_RELOAD = 1;
    for (i=0; i < 5; i++) {
        status = PP_Run_Function("pkgdir.testapi", 
                                 "func", "i", &result, "(ii)", 4, 8);
        if (status == -1) {
            printf("Error running func\n");
            PyErr_Print();                       /* python stack dump */
        }
        else
            printf("result => %d\n", result);
        if (i < 4) {
            printf("change pkgdir/testapi.py now...");  /* edit in  window */
            getchar();                                  /* wait for keypress */
        }
    }

    /********************************************************************
     * turn on dynamic debugging, run string, function, bytecode, object; 
     ********************************************************************/

#define announce(test) result=-1; printf("Debug %s--type s to step...\n", test)
#define showresult printf("C status, result => %d, %d\n\n", status, result)

    TRACE("DYNAMIC DEBUGGING")
    PP_RELOAD = 0;
    PP_DEBUG  = 1;       /* could do both at once */

    announce("code string");
    status = PP_Run_Codestr(PP_EXPRESSION, 
                           "func(4, 8)", "pkgdir.testapi", "i", &result);
    showresult;

    announce("module function call");
    status = PP_Run_Function("pkgdir.testapi", 
                             "func", "i", &result, "(ii)", 4, 8);
    showresult;

    announce("compiled bytecode");
    pobject1 = PP_Compile_Codestr(PP_EXPRESSION, "func(4, 8)");
    status   = PP_Run_Bytecode(pobject1, "pkgdir.testapi", "i", &result);
    Py_XDECREF(pobject1);
    showresult;

    /* could also fetch with "func" string in "pkgdir.testapi" */
    announce("direct object call");
    pobject1 = PP_Load_Attribute("pkgdir.testapi", "func");
    status   = PP_Run_Known_Callable(pobject1, "i", &result, "(ii)", 4, 8);
    Py_XDECREF(pobject1);
    showresult;

    PP_DEBUG = 0;

    /********************************************************************
     * a few object attribute tests
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

    /* run sys.modules.has_key('pkgdir.testapi') */
    PP_Get_Member(pobject1, "modules", "O", &pobject2);

    PP_Run_Method(pobject2, "has_key", "i", &result, "(s)", "pkgdir.testapi"); 
    printf("sys.modules.has_key('pkgdir.testapi') result => %d\n", result);

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
