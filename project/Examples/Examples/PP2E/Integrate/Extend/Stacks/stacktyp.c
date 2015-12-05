/****************************************************
 * stacktyp.c: a character-string stack data-type;
 * a C extension type, for use in Python programs;
 * stacktype module clients can make multiple stacks;
 * similar to stackmod, but 'self' is the instance,
 * and we can overload sequence operators here;
 ****************************************************/

#include "Python.h"

static PyObject *ErrorObject;      /* local exception */
#define onError(message) \
       { PyErr_SetString(ErrorObject, message); return NULL; }

/*****************************************************************************
 * STACK-TYPE INFORMATION
 *****************************************************************************/

#define MAXCHARS 2048
#define MAXSTACK MAXCHARS

typedef struct {                 /* stack instance object */
    PyObject_HEAD                /* python header: ref-count + &typeobject */
    int top, len;  
    char *stack[MAXSTACK];       /* per-instance state info */
    char strings[MAXCHARS];      /* same as stackmod, but multiple copies */
} stackobject;

staticforward PyTypeObject Stacktype;     /* shared type-descriptor */

#define is_stackobject(v)  ((v)->ob_type == &Stacktype)

/*****************************************************************************
 * INSTANCE METHODS
 *****************************************************************************/

static PyObject *             /* on "instance.push(arg)" */
stack_push(self, args)        /* 'self' is the stack instance object */
    stackobject *self;        /* 'args' are args passed to self.push method */
    PyObject    *args; 
{
    char *pstr;
    if (!PyArg_ParseTuple(args, "s", &pstr))     /* convert args: Python->C */
        return NULL;                             /* NULL raises exception,  */
    if (self->top == MAXSTACK)                   /* with arg-error message  */
        onError("stack overflow") 
    if (self->len + strlen(pstr) + 1 >= MAXCHARS)
        onError("string-space overflow")
    else {
        strcpy(self->strings + self->len, pstr);  
        self->stack[self->top++] = &(self->strings[self->len]);  
        self->len += (strlen(pstr) + 1);     
        Py_INCREF(Py_None);  
        return Py_None;                          /* return None: no errors */
    }
}

static PyObject *
stack_pop(self, args)
    stackobject *self;
    PyObject    *args;                           /* on "instance.pop()" */
{
    PyObject *pstr;
    if (!PyArg_ParseTuple(args, ""))             /* verify no args passed */
        return NULL;
    if (self->top == 0)
        onError("stack underflow")               /* return NULL = raise */
    else {
        pstr = Py_BuildValue("s", self->stack[--self->top]);
        self->len -= (strlen(self->stack[self->top]) + 1);
        return pstr;                          
    }
}

static PyObject *
stack_top(self, args)
    stackobject *self;
    PyObject    *args;
{
    PyObject *result = stack_pop(self, args);     /* pop and undo */
    if (result != NULL)
        self->len += (strlen(self->stack[self->top++]) + 1);
    return result;    
}

static PyObject *
stack_empty(self, args)
    stackobject *self;
    PyObject    *args;
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;
    return Py_BuildValue("i", self->top == 0);    /* boolean: a python int */
}

static struct PyMethodDef stack_methods[] = {     /* instance methods */
 {"push",       stack_push,     1},               /* name/address table */
 {"pop",        stack_pop,      1},               /* like list append, sort */
 {"top",        stack_top,      1},         
 {"empty",      stack_empty,    1},               /* extra ops besides optrs */
 {NULL,         NULL}                             /* end, for getattr here */
};

/*****************************************************************************
 * BASIC TYPE-OPERATIONS
 *****************************************************************************/

static stackobject *             /* on "x = stacktype.Stack()" */
newstackobject()                 /* instance constructor function */    
{                                /* these don't get an 'args' input */
    stackobject *self;
    self = PyObject_NEW(stackobject, &Stacktype);  /* malloc, init, incref */
    if (self == NULL)
        return NULL;            /* raise exception */
    self->top = 0;              /* extra constructor logic here */
    self->len = 0;
    return self;                /* a new type-instance object */
}

static void                     /* instance destructor function */
stack_dealloc(self)             /* when reference-count reaches zero */
    stackobject *self;
{                               /* do cleanup activity */
    PyMem_DEL(self);            /* same as 'free(self)' */
}

static int
stack_print(self, fp, flags)
    stackobject *self;
    FILE *fp;
    int flags;                      /* print self to file */
{                                   /* or repr or str */
    int i; 
    fprintf(fp, "[Stack:\n");       
    for (i=self->top - 1; i >= 0; i--)         
        fprintf(fp, "%d: '%s'\n", i, self->stack[i]);
    fprintf(fp, "]\n");
    return 0;                       /* return status, not object */
}

static PyObject *
stack_getattr(self, name)           /* on "instance.attr" reference  */
    stackobject *self;              /* make a bound-method or member */
    char *name; 
{                                                /* exposed data-members */
    if (strcmp(name, "len") == 0)                /* really C struct fields */
        return Py_BuildValue("i", self->len); 
    if (strcmp(name, "__members__") == 0)        /* __methods__ is free */
        return Py_BuildValue("[s]", "len");      /* make a list of 1 string */
    else
        return Py_FindMethod(stack_methods, (PyObject *)self, name);
}

static int
stack_compare(v, w)
    stackobject *v, *w;
{
    int i, test;              /* compare objects and return -1, 0 or 1 */
    if (v->top < w->top)      /* check stack-size, then stacked strings */
        return -1;
    if (v->top > w->top)
        return 1;
    else 
        for (i=0; i < v->top; i++) 
            if ((test = strcmp(v->stack[i], w->stack[i])) != 0)
                return test;
    return 0;
}

/*****************************************************************************
 * SEQUENCE TYPE-OPERATIONS
 *****************************************************************************/

static int
stack_length(self)
    stackobject *self;            /* called on "len(instance)" */
{
    return self->top;             /* don't wrap in a python object */
}

static PyObject *
stack_concat(self, other)
    stackobject *self;                          /* on "instance + other" */
    PyObject    *other;                         /* 'self' is the instance */
{
    int i, len, top;
    stackobject *new, *right;
    if (! is_stackobject(other))
        onError("'+' requires two stacks")      /* no mixed types */
    right = (stackobject *)other;
    if (self->top + right->top > MAXSTACK)
        onError("stack overflow")               /* will the sum fit? */
    if (self->len + right->len > MAXCHARS)
        onError("string-space overflow")
    else {                                      /* '+' makes new stack object */
        new = newstackobject();                 /* instead of in-place change */
        len = top = 0;                      
        for (i=0; i < self->top; i++) {
            new->stack[top++] = &(new->strings[len]);
            strcpy(new->strings + len, self->stack[i]);      /* copy self */
            len += (strlen(self->stack[i]) + 1);
        }
        for (i=0; i < right->top; i++) { 
            new->stack[top++] = &(new->strings[len]);
            strcpy(new->strings + len, right->stack[i]);     /* copy right */
            len += (strlen(right->stack[i]) + 1);
        }
        new->top = top; new->len = len;
        return (PyObject *)new;
    }
}

static PyObject *
stack_repeat(self, n)                /* on "instance * N" */
    stackobject *self;               /* new stack = repeat self n times */
    int n;                           /* XXXX very inefficient! improve me */
{
    int i;                     
    stackobject *next, *temp;        /* copy self N times */
    temp = newstackobject();         /* start with new, empty stack */
    for (i=0; i < n; i++) {
        next = (stackobject *)stack_concat(temp, self);    
        if (next == NULL) { 
            Py_XDECREF(temp);               /* delete result so-far */
            return NULL;                    /* propogate exception */
        }
        else {
            Py_XDECREF(temp);               /* delete result-so-far */
            temp = next;                    /* set new result */
        }
    }
    return (PyObject *)temp;
}

static PyObject *
stack_item(self, index)                    /* on "instance[offset]", "in/for" */
    stackobject *self;                     /* return the i-th item of self */
    int index;                             /* negative index pre-adjusted */
{  
    if (index < 0 || index >= self->top) { 
        PyErr_SetString(PyExc_IndexError, "index out-of-bounds"); 
        return NULL;                                     /* not local error: */
    }                                                    /* else 'in' whines */
    else                                
        return Py_BuildValue("s", self->stack[index]);   /* convert output */
}

static PyObject *
stack_slice(self, ilow, ihigh)
    stackobject *self;                     /* on "instance[ilow:ihigh]" */
    int ilow, ihigh;                       /* negative-adjusted, not scaled */
{
    /* XXXX return the ilow..ihigh slice of self in a new object */
    onError("slicing not yet implemented")
}

/*****************************************************************************
 * TYPE DESCRIPTORS
 *****************************************************************************/

static PySequenceMethods stack_as_sequence = {  /* sequence supplement     */
      (inquiry)       stack_length,             /* sq_length    "len(x)"   */
      (binaryfunc)    stack_concat,             /* sq_concat    "x + y"    */
      (intargfunc)    stack_repeat,             /* sq_repeat    "x * n"    */
      (intargfunc)    stack_item,               /* sq_item      "x[i], in" */
      (intintargfunc) stack_slice,              /* sq_slice     "x[i:j]"   */
      (intobjargproc)     0,                    /* sq_ass_item  "x[i] = v" */
      (intintobjargproc)  0,                    /* sq_ass_slice "x[i:j]=v" */
};

static PyTypeObject Stacktype = {      /* main python type-descriptor */
  /* type header */                    /* shared by all instances */
      PyObject_HEAD_INIT(&PyType_Type)         
      0,                               /* ob_size */
      "stack",                         /* tp_name */
      sizeof(stackobject),             /* tp_basicsize */
      0,                               /* tp_itemsize */

  /* standard methods */
      (destructor)  stack_dealloc,   /* tp_dealloc  ref-count==0  */
      (printfunc)   stack_print,     /* tp_print    "print x"     */
      (getattrfunc) stack_getattr,   /* tp_getattr  "x.attr"      */
      (setattrfunc) 0,               /* tp_setattr  "x.attr=v"    */
      (cmpfunc)     stack_compare,   /* tp_compare  "x > y"       */
      (reprfunc)    0,               /* tp_repr     `x`, print x  */

  /* type categories */
      0,                             /* tp_as_number   +,-,*,/,%,&,>>,pow...*/
      &stack_as_sequence,            /* tp_as_sequence +,[i],[i:j],len, ...*/
      0,                             /* tp_as_mapping  [key], len, ...*/

  /* more methods */
      (hashfunc)     0,              /* tp_hash    "dict[x]" */
      (ternaryfunc)  0,              /* tp_call    "x()"     */
      (reprfunc)     0,              /* tp_str     "str(x)"  */

};  /* plus others: see Include/object.h */

/*****************************************************************************
 * MODULE LOGIC 
 *****************************************************************************/

static PyObject *
stacktype_new(self, args)                 /* on "x = stacktype.Stack()" */
    PyObject *self;                       /* self not used */
    PyObject *args;                       /* constructor args */
{
    if (!PyArg_ParseTuple(args, ""))      /* Module-method function */
        return NULL;
    return (PyObject *)newstackobject();  /* make a new type-instance object */
}                                         /* the hook from module to type... */

static struct PyMethodDef stacktype_methods[] = {
    {"Stack",  stacktype_new,  1},             /* one function: make a stack */ 
    {NULL,     NULL}                           /* end marker, for initmodule */
};

void
initstacktype()                 /* on first "import stacktype" */
{
    PyObject *m, *d;
    m = Py_InitModule("stacktype", stacktype_methods);   /* make the module, */
    d = PyModule_GetDict(m);                             /* with 'Stack' func */
    ErrorObject = Py_BuildValue("s", "stacktype.error");
    PyDict_SetItemString(d, "error", ErrorObject);       /* export exception */
    if (PyErr_Occurred())
        Py_FatalError("can't initialize module stacktype");
}
