/**********************************************************
 * Export C names for use in Python programs.  Defines
 * a C extension module which maps C variables to Python 
 * object attributes ('object.attr'), so they can be 
 * fetched and assigned in Python programs.  Python code 
 * may use attributes and functions of the exported C 
 * cinterfacemod extension module to access exported C 
 * names, and/or the cinterface.Cvar Python-coded class.
 * Clients (the enclosing C programs) define an external 
 * name->address mapping table or function as for the type.  
 *
 * This is backward-compatible with the original type-based
 * version in .., but may run a bit slower due to the extra
 * Python class layer in between Python scripts and C names.
 * On the other hand, it's generaly easier to experiment 
 * with a Python-coded class and simpler C module, than 
 * a C type (e.g., to extend the interface to support nested
 * object references, we would tweak a Python-coded class).  
 * 
 * This version is also similar to the 'shadow class' 
 * notion in SWIG, but SWIG generates a Python class and 
 * C type (not a C module), and the reusable table/function
 * scheme used here differs from SWIG code generation.  
 * Also see ../cinterface.doc, and the C type-based 
 * version in ../cinterface.c.
 **********************************************************/

#include <Python.h>
#include <stdlib.h>
#include "cinterface.h"

extern cnameMapFunction CnameMapLookup;     /* define me and link to process */
extern char CnameMessage[];                 /* simple text settable by Python */
static PyObject *ErrorObject;               /* my local exception object */


/*****************************************************************************
 * MODULE FUNCTIONS
 *****************************************************************************/

/* 
 * CnameMapLookup must be defined somewhere in the process: link in
 * defaultlookup.c with a CnameMapTable, or your own CnameMapLookup 
 */

static PyObject *
cvar_getname(self, args)           /* on "cinterfacemod.getname()" */
    PyObject *self;                /* return var's value in C layer */
    PyObject *args;                /* self unused here--a module */
{ 
    char *name;
    cnameMap *cname;

    if (!PyArg_ParseTuple(args, "s", &name))        /* convert Python to C */
        return NULL;
    cname = CnameMapLookup(name);                   /* call linked-in search */
    if (cname != NULL) {                            /* convert C to Python */
        switch (cname->typecode) {
        case INT:
            return Py_BuildValue("i", *(int*)cname->address);
        case STR1: 
            return Py_BuildValue("s",  (char*)cname->address);
        case STR2:
            return Py_BuildValue("s", *(char**)cname->address);
        case FLT:
            return Py_BuildValue("f", *(float*)cname->address);
        }
    }
    PyErr_SetString(ErrorObject, "Cvar name not found");  
    return NULL;  /* trigger exception */
}

static PyObject*
cvar_setname(self, args)           /* on "cinterfacemod.setname()" */
    PyObject *self;                /* set named var's value in C layer */
    PyObject *args;                /* self unused here--a module */
{                                  /* PyArg_Parse verifies type and converts */
    char *name;
    PyObject *value;
    int stat;
    char *temp;
    cnameMap *cname;

    if (!PyArg_ParseTuple(args, "sO", &name, &value)) 
        return NULL;
    cname = CnameMapLookup(name);                   /* call linked-in search */
    if (cname != NULL && value != NULL) {           /* convert Python to C */
        stat = 0;
        switch (cname->typecode) { 
        case INT:
            stat = PyArg_Parse(value, "i", cname->address);
            break;
        case STR1:
            stat = PyArg_Parse(value, "s", &temp);  /* or PyString_AsString */
            if (stat) strncpy((char*)cname->address, temp, 64);
            break;
        case STR2:
            stat = PyArg_Parse(value, "s", &temp);             /* copy out */
            if (stat) *(char**)cname->address = strdup(temp);  /* C free's */
            break;
        case FLT:
            stat = PyArg_Parse(value, "f", cname->address);
            break;
        }
        if (stat == 0) {
            PyErr_SetString(PyExc_TypeError, "Cvar type conversion");  
            return NULL;               /* trigger exception */
        }
        else {
            Py_INCREF(Py_None); 
            return Py_None;            /* return None: success */
        }
    }
    PyErr_SetString(ErrorObject, "Cvar name not found");  
    return NULL;                       /* trigger exception */
}

static PyObject *
setMessage(self, args)                    /* on "cinterfacemod.setMessage()" */
    PyObject *self;                       /* self not used in module funcs */
    PyObject *args;                       /* method call args */
{
    char *text;
    if (!PyArg_ParseTuple(args, "s", &text)) 
        return NULL;
    strcpy(CnameMessage, text);           /* save Py string object text*/ 
    Py_INCREF(Py_None);                   /* return 'None': success */
    return Py_None;
}


/*****************************************************************************
 * DISPATCH LOGIC
 *****************************************************************************/

static struct PyMethodDef cinterfacemod_methods[] = {
    {"getname",    cvar_getname, 1}, 
    {"setname",    cvar_setname, 1},              /* name, address table */ 
    {"setMessage", setMessage,   1},              /* module functions */
    {NULL, NULL}                                  /* initmodule end marker */
};

void                                 /* the only non-static in this file */
initcinterfacemod()                  /* called automatically by Python */
{                                    /* on first import of cinterfacemod */
    PyObject *m, *d;
    m = Py_InitModule("cinterfacemod", cinterfacemod_methods); 
    d = PyModule_GetDict(m);                            
    ErrorObject = Py_BuildValue("s", "cinterfacemod.error");
    PyDict_SetItemString(d, "error", ErrorObject);
    if (PyErr_Occurred())
        Py_FatalError("can't initialize module cinterfacemod");
}

