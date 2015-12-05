/***********************************************************
[your copyright notice here]
******************************************************************/

#include "Python.h"

static PyObject *ErrorObject;

/* ----------------------------------------------------- */

/* Declarations for objects of type SetType */

typedef struct {
	PyObject_HEAD
	/* XXXX Add your own stuff here */
} settobject;

staticforward PyTypeObject Setttype;



/* ---------------------------------------------------------------- */

static char sett_intersect__doc__[] = 
""
;

static PyObject *
sett_intersect(self, args)
	settobject *self;
	PyObject *args;
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}


static char sett_union__doc__[] = 
""
;

static PyObject *
sett_union(self, args)
	settobject *self;
	PyObject *args;
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}


static char sett_difference__doc__[] = 
""
;

static PyObject *
sett_difference(self, args)
	settobject *self;
	PyObject *args;
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}


static char sett_concat__doc__[] = 
""
;

static PyObject *
sett_concat(self, args)
	settobject *self;
	PyObject *args;
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}


static struct PyMethodDef sett_methods[] = {
	{"intersect",	sett_intersect,	1,	sett_intersect__doc__},
 {"union",	sett_union,	1,	sett_union__doc__},
 {"difference",	sett_difference,	1,	sett_difference__doc__},
 {"concat",	sett_concat,	1,	sett_concat__doc__},
 
	{NULL,		NULL}		/* sentinel */
};

/* ---------- */


static settobject *
newsettobject()
{
	settobject *self;
	
	self = PyObject_NEW(settobject, &Setttype);
	if (self == NULL)
		return NULL;
	/* XXXX Add your own initializers here */
	return self;
}


static void
sett_dealloc(self)
	settobject *self;
{
	/* XXXX Add your own cleanup code here */
	PyMem_DEL(self);
}

static PyObject *
sett_getattr(self, name)
	settobject *self;
	char *name;
{
	/* XXXX Add your own getattr code here */
	return Py_FindMethod(sett_methods, (PyObject *)self, name);
}

static int
sett_compare(v, w)
	settobject *v, *w;
{
	/* XXXX Compare objects and return -1, 0 or 1 */
}

static PyObject *
sett_repr(self)
	settobject *self;
{
	PyObject *s;

	/* XXXX Add code here to put self into s */
	return s;
}

/* Code to handle accessing SetType objects as sequence objects */

static int
sett_length(self)
	settobject *self;
{
	/* XXXX Return the size of the object */
}

static PyObject *
sett_concat(self, bb)
	settobject *self;
	PyObject *bb;
{
	/* XXXX Return the concatenation of self and bb */
}

static PyObject *
sett_repeat(self, n)
	settobject *self;
	int n;
{
	/* XXXX Return a new object that is n times self */
}

static PyObject *
sett_item(self, i)
	settobject *self;
	int i;
{
	/* XXXX Return the i-th object of self */
}

static PyObject *
sett_slice(self, ilow, ihigh)
	settobject *self;
	int ilow, ihigh;
{
	/* XXXX Return the ilow..ihigh slice of self in a new object */
}

static int
sett_ass_item(self, i, v)
	settobject *self;
	int i;
	PyObject *v;
{
	/* XXXX Assign to the i-th element of self */
	return 0;
}

static int
sett_ass_slice(self, ilow, ihigh, v)
	PyListObject *self;
	int ilow, ihigh;
	PyObject *v;
{
	/* XXXX Replace ilow..ihigh slice of self with v */
	return 0;
}

static PySequenceMethods sett_as_sequence = {
	(inquiry)sett_length,		/*sq_length*/
	(binaryfunc)sett_concat,		/*sq_concat*/
	(intargfunc)sett_repeat,		/*sq_repeat*/
	(intargfunc)sett_item,		/*sq_item*/
	(intintargfunc)sett_slice,		/*sq_slice*/
	(intobjargproc)sett_ass_item,	/*sq_ass_item*/
	(intintobjargproc)sett_ass_slice,	/*sq_ass_slice*/
};

/* -------------------------------------------------------------- */

static char Setttype__doc__[] = 
""
;

static PyTypeObject Setttype = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,				/*ob_size*/
	"SetType",			/*tp_name*/
	sizeof(settobject),		/*tp_basicsize*/
	0,				/*tp_itemsize*/
	/* methods */
	(destructor)sett_dealloc,	/*tp_dealloc*/
	(printfunc)0,		/*tp_print*/
	(getattrfunc)sett_getattr,	/*tp_getattr*/
	(setattrfunc)0,	/*tp_setattr*/
	(cmpfunc)sett_compare,		/*tp_compare*/
	(reprfunc)sett_repr,		/*tp_repr*/
	0,			/*tp_as_number*/
	&sett_as_sequence,		/*tp_as_sequence*/
	0,		/*tp_as_mapping*/
	(hashfunc)0,		/*tp_hash*/
	(binaryfunc)0,		/*tp_call*/
	(reprfunc)0,		/*tp_str*/

	/* Space for future expansion */
	0L,0L,0L,0L,
	Setttype__doc__ /* Documentation string */
};

/* End of code for SetType objects */
/* -------------------------------------------------------- */


static char setm_newset__doc__[] =
""
;

static PyObject *
setm_newset(self, args)
	PyObject *self;	/* Not used */
	PyObject *args;
{

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char setm_asList__doc__[] =
""
;

static PyObject *
setm_asList(self, args)
	PyObject *self;	/* Not used */
	PyObject *args;
{

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char setm_asString__doc__[] =
""
;

static PyObject *
setm_asString(self, args)
	PyObject *self;	/* Not used */
	PyObject *args;
{

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char setm_statistics__doc__[] =
""
;

static PyObject *
setm_statistics(self, args)
	PyObject *self;	/* Not used */
	PyObject *args;
{

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

/* List of methods defined in the module */

static struct PyMethodDef setm_methods[] = {
	{"newset",	setm_newset,	1,	setm_newset__doc__},
 {"asList",	setm_asList,	1,	setm_asList__doc__},
 {"asString",	setm_asString,	1,	setm_asString__doc__},
 {"statistics",	setm_statistics,	1,	setm_statistics__doc__},
 
	{NULL,		NULL}		/* sentinel */
};


/* Initialization function for the module (*must* be called initSetMod) */

static char SetMod_module_documentation[] = 
""
;

void
initSetMod()
{
	PyObject *m, *d;

	/* Create the module and add the functions */
	m = Py_InitModule4("SetMod", setm_methods,
		SetMod_module_documentation,
		(PyObject*)NULL,PYTHON_API_VERSION);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);
	ErrorObject = PyString_FromString("SetMod.error");
	PyDict_SetItemString(d, "error", ErrorObject);

	/* XXXX Add constants here */
	
	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("can't initialize module SetMod");
}

