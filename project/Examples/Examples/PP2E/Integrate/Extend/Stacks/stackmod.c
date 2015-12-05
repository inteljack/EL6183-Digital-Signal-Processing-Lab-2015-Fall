/*****************************************************
 * stackmod.c: a shared stack of character-strings;
 * a C extension module for use in Python programs;
 * linked into python libraries or loaded on import;
 *****************************************************/

#include "Python.h"             /* Python header files */
#include <stdio.h>              /* C header files */
#include <string.h>

static PyObject *ErrorObject;   /* locally-raised exception */

#define onError(message) \
       { PyErr_SetString(ErrorObject, message); return NULL; }

/******************************************************************************
* LOCAL LOGIC/DATA (THE STACK)
******************************************************************************/

#define MAXCHARS 2048
#define MAXSTACK MAXCHARS

static int  top = 0;                 /* index into 'stack' */
static int  len = 0;                 /* size of 'strings' */
static char *stack[MAXSTACK];        /* pointers into 'strings' */
static char strings[MAXCHARS];       /* string-storage area */

/******************************************************************************
* EXPORTED MODULE METHODS/FUNCTIONS
******************************************************************************/

static PyObject *
stack_push(PyObject *self, PyObject *args)       /* args: (string) */
{
    char *pstr;
    if (!PyArg_ParseTuple(args, "s", &pstr))     /* convert args: Python->C */
        return NULL;                             /* NULL triggers exception */
    if (top == MAXSTACK)                         /* python sets arg-error msg */
        onError("stack overflow")                /* iff maxstack < maxchars */
    if (len + strlen(pstr) + 1 >= MAXCHARS)
        onError("string-space overflow")
    else {
        strcpy(strings + len, pstr);             /* store in string-space */
        stack[top++] = &(strings[len]);          /* push start address */
        len += (strlen(pstr) + 1);               /* new string-space size */
        Py_INCREF(Py_None);                      /* a 'procedure' call */
        return Py_None;                          /* None: no errors */
    }
}

static PyObject *
stack_pop(PyObject *self, PyObject *args)
{                                                /* no arguments for pop */
    PyObject *pstr;
    if (!PyArg_ParseTuple(args, ""))             /* verify no args passed */
        return NULL;
    if (top == 0)
        onError("stack underflow")               /* return NULL = raise */
    else {
        pstr = Py_BuildValue("s", stack[--top]); /* convert result: C->Py */
        len -= (strlen(stack[top]) + 1);
        return pstr;                             /* return new python string */
    }                                            /* pstr ref-count++ already */
}

static PyObject *
stack_top(PyObject *self, PyObject *args)        /* almost same as item(-1) */
{                                                /* but different errors */
    PyObject *result = stack_pop(self, args);    /* get top string */
    if (result != NULL)
        len += (strlen(stack[top++]) + 1);       /* undo pop */
    return result;                               /* NULL or string object */
}

static PyObject *
stack_empty(PyObject *self, PyObject *args)      /* no args: '()' */
{
    if (!PyArg_ParseTuple(args, ""))             /* or PyArg_NoArgs */
        return NULL;
    return Py_BuildValue("i", top == 0);         /* boolean: a python int */
}

static PyObject *
stack_member(PyObject *self, PyObject *args)
{
    int i;
    char *pstr;
    if (!PyArg_ParseTuple(args, "s", &pstr))
        return NULL;      
    for (i = 0; i < top; i++)                /* find arg in stack */
        if (strcmp(pstr, stack[i]) == 0)
            return PyInt_FromLong(1);        /* send back a python int */
    return PyInt_FromLong(0);                /* same as Py_BuildValue("i" */
}

static PyObject *
stack_item(PyObject *self, PyObject *args)    /* return Python string or NULL */
{                                             /* inputs = (index): Python int */
    int index;
    if (!PyArg_ParseTuple(args, "i", &index))    /* convert args to C */
        return NULL;                             /* bad type or arg count? */
    if (index < 0)
        index = top + index;                     /* negative: offset from end */
    if (index < 0 || index >= top)
        onError("index out-of-bounds")           /* return NULL = 'raise' */
    else 
        return Py_BuildValue("s", stack[index]); /* convert result to Python */
}                                                /* no need to INCREF new obj */

static PyObject *
stack_len(PyObject *self, PyObject *args)     /* return a Python int or NULL */
{                                             /* no inputs */
    if (!PyArg_ParseTuple(args, ""))          
        return NULL;      
    return PyInt_FromLong(top);               /* wrap in python object */
}

static PyObject *
stack_dump(PyObject *self, PyObject *args)    /* not "print": reserved word */
{
    int i;
    if (!PyArg_ParseTuple(args, ""))
        return NULL;
    printf("[Stack:\n");
    for (i=top-1; i >= 0; i--)                   /* formatted output */
        printf("%d: '%s'\n", i, stack[i]);
    printf("]\n");
    Py_INCREF(Py_None);
    return Py_None;
}

/******************************************************************************
* METHOD REGISTRATION TABLE: NAME-STRING -> FUNCTION-POINTER
******************************************************************************/

static struct PyMethodDef stack_methods[] = {
 {"push",       stack_push,     1},                /* name, address */
 {"pop",        stack_pop,      1},                /* '1'=always tuple args */
 {"top",        stack_top,      1},
 {"empty",      stack_empty,    1},
 {"member",     stack_member,   1},
 {"item",       stack_item,     1},
 {"len",        stack_len,      1},
 {"dump",       stack_dump,     1},
 {NULL,         NULL}                              /* end, for initmodule */
};

/******************************************************************************
* INITIALIZATION FUNCTION (IMPORT-TIME)
******************************************************************************/

void
initstackmod()
{
    PyObject *m, *d;

    /* create the module and add the functions */
    m = Py_InitModule("stackmod", stack_methods);        /* registration hook */

    /* add symbolic constants to the module */
    d = PyModule_GetDict(m);
    ErrorObject = Py_BuildValue("s", "stackmod.error");  /* export exception */
    PyDict_SetItemString(d, "error", ErrorObject);       /* add more if need */
    
    /* check for errors */
    if (PyErr_Occurred())
        Py_FatalError("can't initialize module stackmod");
}
