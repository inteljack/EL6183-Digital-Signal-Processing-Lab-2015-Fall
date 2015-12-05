/**********************************************************
 * Export C names for use in Python programs.  Defines
 * a C extension type which maps C variables to Python 
 * object attributes ('object.attr'), so they can be 
 * fetched and assigned in Python programs.  Python code 
 * uses attributes of an instance of the exported Cvar 
 * extension type to access exported C names.  Clients
 * define an external name->address mapping table or 
 * function.  See cinterface.doc for more documentation.
 **********************************************************/

#include <Python.h>
#include <stdlib.h>
#include "cinterface.h"

extern cnameMapFunction CnameMapLookup;    /* define me and link to process */
extern char CnameMessage[];                /* simple text settable by Python */
static PyObject *ErrorObject;              /* my local exception object */


/*****************************************************************************
 * PER-INSTANCE INFORMATION
 *****************************************************************************/

typedef struct {                 /* cvar instance struct */
    PyObject_HEAD                /* python header: ref-count + &typeobject */
    int gets, sets;              /* qualification access counters */
} cvarobject;

staticforward PyTypeObject Cvartype;     /* shared type-descriptor */


/*****************************************************************************
 * INSTANCE METHODS
 *****************************************************************************/

static PyObject *             /* on "cvar-instance.stats()" */
cvar_stats(self, args)        /* 'self' is the cvar instance object */
    cvarobject *self;         /* 'args' are args passed to method */
    PyObject   *args; 
{
    if (!PyArg_ParseTuple(args, ""))      /* verify no args passed */
        return NULL;
    return Py_BuildValue("(ii)", self->gets, self->sets);
}

static struct PyMethodDef cvar_methods[] = {      /* instance methods */
 {"stats",  cvar_stats,  1},                      /* name/address table */
 {NULL,     NULL}                                 /* end, for getattr here */
};


/*****************************************************************************
 * BASIC TYPE-OPERATIONS
 *****************************************************************************/

/*
 * CnameMapLookup must be defined somewhere in the process: link in
 * defaultlookup.c with a CnameMapTable, or your own CnameMapLookup
 */

static cvarobject *                  /* on "x = cinterface.Cvar()" */
newcvarobject()                      /* instance constructor function */    
{                                    /* these don't get an 'args' input */
    cvarobject *self;
    self = PyObject_NEW(cvarobject, &Cvartype);  /* malloc, init, incref */
    if (self == NULL)
        return NULL;                 /* raise exception */
    self->gets = self->sets = 0;     /* extra constructor logic here */
    return self;                     /* a new type-instance object */
}

static void                          /* instance destructor function */
cvar_dealloc(self)                   /* when reference-count reaches zero */
    cvarobject *self;
{                                    /* do cleanup activity */
    PyMem_DEL(self);                 /* same as 'free(self)' */
}

static PyObject*
cvar_repr(self)
    cvarobject *self;                /* return print representstion object */
{                                    /* called on print and repr and str */
    char buff[128];
    sprintf(buff, "<Cvar interface instance object: %d, %d>\n",
                   self->gets, self->sets);
    return PyString_FromString(buff); 
}

static PyObject *
cvar_getattr(self, name)             /* on "instance.attr" reference  */
    cvarobject *self;                /* return var value, or bound method */
    char *name; 
{ 
    cnameMap *cname;
    self->gets++;
    cname = CnameMapLookup(name);                   /* call linked-in search */
    if (cname != NULL) {                            /* convert C to Python */
        switch (cname->typecode) {
        case INT:
            return Py_BuildValue("i", *(int*)cname->address);
        case STR1:                                  /* or PyString_FromString */
            return Py_BuildValue("s",  (char*)cname->address);
        case STR2:
            return Py_BuildValue("s", *(char**)cname->address);
        case FLT:
            return Py_BuildValue("f", *(float*)cname->address);
        }
    }
    return Py_FindMethod(cvar_methods, (PyObject *)self, name);
}

static int
cvar_setattr(self, name, value)    /* on "instance.attr = value" assignment */
    cvarobject *self;              /* set named var's value in C layer */
    char *name; 
    PyObject *value;
{                                  /* PyArg_Parse verifies type and converts */
    int stat;
    char *temp;
    cnameMap *cname;

    self->sets++;
    cname = CnameMapLookup(name);                   /* call linked-in search */
    if (cname != NULL && value != NULL) {           /* del not supported */
        switch (cname->typecode) {                  /* convert Python to C */
        case INT:
            stat = PyArg_Parse(value, "i", cname->address);
            return stat==0 ? -1 : 0;
        case STR1:
            stat = PyArg_Parse(value, "s", &temp);  /* or PyString_AsString */
            if (stat) strncpy((char*)cname->address, temp, 64);
            return stat==0 ? -1 : 0;
        case STR2:
            stat = PyArg_Parse(value, "s", &temp);             /* copy out */
            if (stat) *(char**)cname->address = strdup(temp);  /* C free's */
            return stat==0 ? -1 : 0;
        case FLT:
            stat = PyArg_Parse(value, "f", cname->address);
            return stat==0 ? -1 : 0;                           /* 0=success */
        }
    }
    PyErr_SetString(ErrorObject, "Cvar name not found");  
    return -1;                              /* -1=failure, raises exception */
}


/*****************************************************************************
 * TYPE DESCRIPTOR
 *****************************************************************************/

static PyTypeObject Cvartype = {       /* main python type-descriptor */
  /* type header */                    /* shared by all instances */
      PyObject_HEAD_INIT(&PyType_Type)         
      0,                               /* ob_size */
      "cvar",                          /* tp_name */
      sizeof(cvarobject),              /* tp_basicsize */
      0,                               /* tp_itemsize */
  /* standard methods */
      (destructor)  cvar_dealloc,      /* tp_dealloc  ref-count==0  */
      (printfunc)   0,                 /* tp_print    "print x"     */
      (getattrfunc) cvar_getattr,      /* tp_getattr  "x.attr"      */
      (setattrfunc) cvar_setattr,      /* tp_setattr  "x.attr=v"    */
      (cmpfunc)     0,                 /* tp_compare  "x > y"       */
      (reprfunc)    cvar_repr,         /* tp_repr     `x`, print x  */
  /* type categories */
      0,                               /* tp_as_number   +,-,*,/,%,&,>>,pow...*/
      0,    /* just attributes */      /* tp_as_sequence +,[i],[i:j],len, ...*/
      0                                /* tp_as_mapping  [key], len, ...*/
};  /* plus others, all zero: see Include/object.h */


/*****************************************************************************
 * MODULE LOGIC 
 *****************************************************************************/

static PyObject *
Cvar_constructor(self, args)              /* on "x = cinterface.Cvar()" */
    PyObject *self;                       /* self not used */
    PyObject *args;                       /* constructor call args */
{
    if (!PyArg_ParseTuple(args, ""))      /* Module-method function */
        return NULL;
    return (PyObject *)newcvarobject();   /* make a new type-instance object */
}                                         /* the hook from module to type */

static PyObject *
setMessage(self, args)                    /* on "cinterface.setMessage('x')" */
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

static struct PyMethodDef cinterface_methods[] = {   /* name, address table */
    {"Cvar",       Cvar_constructor,  1},            /* make Cvar instance  */
    {"setMessage", setMessage,        1},            /* set C global char[] */
    {NULL, NULL}                                     /* initmodule end marker */
};

void                             /* the only non-static in this file */
initcinterface()                 /* called automatically by Python */
{                                /* on first import of cinterface */
    PyObject *m, *d;
    m = Py_InitModule("cinterface", cinterface_methods);  /* make module */ 
    d = PyModule_GetDict(m);                            
    ErrorObject = Py_BuildValue("s", "cinterface.error");
    PyDict_SetItemString(d, "error", ErrorObject);        /* export exception */
    if (PyErr_Occurred())                                 /* for use in try's */
        Py_FatalError("can't initialize module cinterface");
}

