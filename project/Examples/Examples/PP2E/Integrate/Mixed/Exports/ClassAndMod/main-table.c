/*********************************************************
 * main program - loads embedded Python code from files;
 * same as ../main1.c, except that the script files are
 * loaded from '..' now, and code strings are precompiled
 * to bytecode objects rather than being run directly.
 * the runpy.c interface in unchanged in this version.
 *********************************************************/
 
#include <stdio.h>
#include "runpy.h"
#include "cinterface.h"

/* Python programs to run */
#define MAXFILE 4096
static char *tests[] = 
       {"../script1.py", "../script2.py", "../script3.py", NULL};

/* names that this C program exports to Python programs */
static int   aa = 0; 
static int   bb = 42;
static char  cc[64] = "";
static char *dd = "Cspam";
static float ee = 3.14159;  

/* mapping table used in cinterface.c */
static cnameMap myCnameMapTable[] = {
    {"aa", INT,  &aa},
    {"bb", INT,  &bb},         /* names exported to Python code */
    {"cc", STR1,  cc},         /* in python code: "cvar.cc" */
    {"dd", STR2, &dd},         /* linked to cinterface.so on import */
    {"ee", FLT,  &ee},
    {NULL, INT,  NULL}
};

/* cinterface names */
char CnameMessage[128];
cnameMapTablePtr CnameMapTable = &myCnameMapTable;

static void 
dumpall()
{ 
    printf("vars in C:\taa=%d bb=%d cc=%s dd=%s ee=%f\n", aa, bb, cc, dd, ee); 
}

static void
run_user_code()                   
{                                 /* load/run Python code from text files */
    int status, nbytes;           /* XXX should also check status everywhere */
    char script[MAXFILE];         /* XXX should malloc a big-enough block */
    FILE *file;
    PyObject *bytecode;

    char **test = tests;
    dumpall();
    while (*test != NULL) {
        printf("\nStarting %s\n", *test);

        file = fopen(*test, "r");                  /* load Python file text */
        nbytes = fread(script, 1, MAXFILE, file);  /* customizable actions */
        script[nbytes] = '\0';

        bytecode = RunPyCompileCodeString(script);
        if (bytecode == NULL) {
            printf("%s\n", RunPyError);
            RunPyPrintPythonErrorInfo();
        }
        
        status = RunPyExecBytecode(bytecode);   /* run compiled code object */
        Py_DECREF(bytecode);                    /* cinterface handles names */
        if (status != 0) {
            printf("%s\n", RunPyError);
            RunPyPrintPythonErrorInfo();
        }
        dumpall();
        test++;
    }
}

main(int argc, char **argv)              /* C's on-top, Python's embedded */
{                                        /* but Python uses C extensions  */
    int status = RunPyInitialize();      /* RunPy routines unchanged here */
    if (status != 0) {
        printf("%s\n", RunPyError);
        RunPyPrintPythonErrorInfo();
    }
    run_user_code(); 
    printf(CnameMessage);
}
