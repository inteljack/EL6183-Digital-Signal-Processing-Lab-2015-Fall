/******************************************************
 * Wraps ppembed API, sets up names for Python code;
 * Include in main C program files, and link C objects
 * with runpy.o and Python lib .a to make an executable;
 * to run the executable, set PYTHONPATH to include the
 * Python standard library (if a non-standard install),
 * plus the directory where cinterface.so is installed.
 * to route code strings and byte code to the pdb Python
 * debugger, simply set PP_DEBUG (in libppembed.a) to 1;
 *
 * Executable build requirements: 
 *    headers: Python.h, runpy.h
 *    objects: runpy.o, libpython1.5.a, libppembed.a,
 *    others:  additional app C files, with a main() function.
 *
 * Intallation/run requirements: 
 *    modules: cinterface.co
 *    others:  executable, Python standard lib
 ******************************************************/

#ifndef RUNPY_H
#define RUNPY_H  

#include <Python.h>

extern char     *RunPyError;
extern int       RunPyInitialize();
extern int       RunPyExecCodeString(char *code);
extern PyObject *RunPyCompileCodeString(char *codestr);
extern int       RunPyExecBytecode(PyObject *codeobj);
extern void      RunPyPrintPythonErrorInfo();

#endif
