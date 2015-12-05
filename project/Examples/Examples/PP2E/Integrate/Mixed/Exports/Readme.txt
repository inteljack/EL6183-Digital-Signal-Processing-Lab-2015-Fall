[See also: cinterface.doc, internal source file comments]

Export C variable names for use in Python programs embedded in C.
All the C example programs built in this directory load and run 
code in the Python script files here (script*.py), which in turn 
call out to the cinterface C extension type (or module) to access 
C names exported by the C main programs.  Roughly:

    [C prog]  ==>  [script.py]  ==> [cinterface]
      vars          cvar.attr         getattr     
       ^                                 |
       |                                 |
       |---------------------------------|
                            <- "attr"
                         type, address ->   

C names may be both referenced (cvar.xxx) anda ssigned (cvar.xxx = value)
in Python scripts; the C interface type catches these operations and routes
them to the enclosing C layer's names.  This is roughly similar to the way
that SWIG exports C global variables to Python programs, but the example here
provides a reusable interface type (clients provide a name->(type, address)
function or table), and the implementation here allows for more dynamic name
mapping (the table may hold arbitrary C addresses, and the function can perform
arbitrary mapping procedures).  As implemented, the system here is limited 
to simple C data types.  Example programs created in this directory:

prog1  (main-table.c)
    runs raw code strings, provides a mapping table, links the 
    default name lookup function with the cinterface.so module

prog2  (main-function.c)
    runs raw code strings, provides its own name lookup function,
    rather than a lookup table

prog3  (main-table.c)
    same as prog1, but links default name lookup function with 
    enclosing C layer (main-table.c), not the cinterface.so module

ClassAndMod/
    like prog1, but the C layer precompiles strings to bytecode, and 
    uses a Python class + C module, instead of a C type

Directory ClassAndMod is a version that implements the C name
interface using a Python-coded class plus a simpler C extension
module, rather than a C extension type.  It reuses main-table.c, 
but modifies it to find scripts in '..', and precompile the code 
strings to bytecode objects.


Outputs:
To compare the type and class+module versions, type this:
'diff output.prog1 ..' in the ClassAndMod subdirectory (which
simply compares the results of 'prog1 > output.prog1' commands).
Subtle things: 

- The get/set counts kept by the C type (here) and the Python 
  class (ClassAndMod subdir) differ by 1 after a dir() call on
  the Cvar object, because Python asks the C type for __dict__, 
  __members__, and __methods__ attributes (which go to the getattr
  handler), but does not ask the class instance for the __dict__ 
  attribute (presumably, because it's a given).  Recall that all 
  attribute references are routed to the setattr handler, even 
  ones that the Python interpreter generates itself.
- The error messages differ a bit (since the module detects getattr
  failures that the type delegates to Py_FindMethod)
- The dir() and sys.modules test differ slightly as well, because
  the class instance has a 'count' object (not a 'stats' function),
  and sys.modules includes the extra cinterfacemod for the module.


C++ notes:
To export C++ objects, either compile the cinterface module with
a C++ compiler and declared its init function extern "C", or compile
cinterface as a C file and call out from it to C++ functions declared
extern "C".  The two options are roughly:

                       extern "C"          extern "C"
   [C++ top-level] ==> [Python  C lib] ==> [C++ type,  C++ names] 
                       [ppembed C lib]

                       C-------------C

                       extern "C"                       extern "C"
   [C++ top-level] ==> [Python  C lib] ==> [C type] ==> [C++ names] 
                       [ppembed C lib]

                       C---------------------------C

Python headers and ppembed.h are automatically wrapped in extern "C" 
declarations, so calls from C++ into Python and ppembed C libs work
automatically.  The call from the C layer back to C++ must be declared
extern "C" by the application.  In terms of components, the example
looks like this, with a C-coded type:

          (C or C++)                 (C)

           ========
             main
           ========
              |
              V
           ========                =======
            runpy   -------------> ppembed
           ========                =======
                                      |
                                      V
                                   ========
                                    python
                                   ========
                                      |
                                      V
           ========               ==========
            lookup  <------------ cinterface
           ========               ==========




--------------------
Other possibilities:
If you need to convert from Python to C based in the type of the
Python object (rather than a C type), you can use code like this,
given a PyObject *pyvalue:

    long   anInt;
    char  *aString;
    double aFloat;
    if (PyString_Check(pyvalue) {
        // Python string; can contain nulls
        if (PyArg_Parse(pyvalue, "s", &aString))   // or PyString_AsString()
            ...
    }
    else
    if (PyInt_Check(pyvalue) {    
        // Python integer; a C long internally
        if (PyArg_Parse(pyvalue, "i", &anInt))
            ...
    }
    else
    if (PyLong_Check(pyvalue) {
        // Python long integer; unlimited precision
        if (PyArg_Parse(pyvalue, "l", &anInt))
            ...
    }
    else
    if (PyFloat_Check(pyvalue) {
        // Python float; a C double internally
        if (PyArg_Parse(pyvalue, "f", &aFloat))
            ...
    }
    else
    if (pyvalue == Py_None) {
        ...
    }
    and so on -- see Python header files for other type tests


Also note that there are type-specific converters for built-in
types besides PyArg_Parse (Py->C) and Py_BuildValue (C->Py).  The
latter are generic and easy to remember, but the type-specific 
functions may be faster, since they skip the convert code string
parse/analyse step.  Below is a list of some of the more useful
type-specific functions; see the Python/C API for a complete list,
and the Python abtract.h header file/interface for generic object
access functions.

Example: here's one way to iterate over an arguments tuple manually,
rather than converting them all at once with PyArg_ParseTuple:

PyObject *modulefunc(PyObject *self, PyObject *pyargs)
{
    int i;
    long aLong;
    PyObject *pyarg;

    for (i=0; i < PyTuple_Size(pyargs); i++) {
       pyarg = PyTuple_GetItem(pyargs, i);          // borrowed reference
       if (PyInt_Check(pyarg)) {                    // no need to decref
          aLong  = PyInt_AsLong(pyvalue);
          ...
       }
    }


INTEGERS:
int PyInt_Check(PyObject *) 
    Is it an integer?

PyObject* PyInt_FromLong(long ival) 
    Creates a new integer object with a value of ival. 
        Same as Py_BuildValue("i",  ival), and Py_BuildValue("l",  ival).

long PyInt_AsLong(PyObject *io) 
    Returns the value of the object io.
        Same as PyArg_Parse(pyvalue, "l", &aLong).


FLOATS:
int PyFloat_Check(PyObject *p) 
    Returns true if its argument is a PyFloatObject.

PyObject* PyFloat_FromDouble(double v) 
    Creates a PyFloatObject object from v.
        Same as Py_BuildValue("f", v) and Py_BuildValue("d", v).

double PyFloat_AsDouble(PyObject *pyfloat) 
    Returns a C double representation of the contents of pyfloat.
        Same as PyArg_Parse(pyvalue, "d", &aDouble).


STRINGS:
int PyString_Check(PyObject *o) 
    Returns true if the object o is a string object.

PyObject* PyString_FromString(const char *v) 
    Returns a new string object with the value v.
        Same as  Py_BuildValue("s", v).

PyObject* PyString_FromStringAndSize(const char *v, int len) 
    Returns a new string object with the value v and length len (allows nulls).
        Same as  Py_BuildValue("s#", v, len).

char* PyString_AsString(PyObject *string) 
    Resturns a NULL terminated representation of the contents of string.
        Same as PyArg_Parse(pyvalue, "s", &aString).

int PyString_Size(PyObject *string) 
    Returns the length of the string in string object string.


LONGS:
int PyLong_Check(PyObject *p) 
    Returns true if its argument is a PyLongObject.

PyObject* PyLong_FromLong(long v) 
    Returns a new PyLongObject object from v.

PyObject* PyLong_FromUnsignedLong(unsigned long v) 
    Returns a new PyLongObject object from an unsigned C long.

long PyLong_AsLong(PyObject *pylong) 
    Returns a C long representation of the contents of pylong.

unsigned long PyLong_AsUnsignedLong(PyObject *pylong) 
    Returns a C unsigned long representation of the contents of pylong.


LISTS:
int PyList_Check(PyObject *p) 
    Returns true if its argument is a PyListObject.

PyObject* PyList_New(int size) 
    Returns a new list of length len on success, and NULL on failure.

int PyList_Size(PyObject *list) 
    Returns the length of the list object in list.

PyObject* PyList_GetItem(PyObject *list, int index) 
    Returns the object at position pos in the list pointed to by p. 

int PyList_SetItem(PyObject *list, int index, PyObject *item) 
    Sets the item at index index in list to item.

int PyList_Insert(PyObject *list, int index, PyObject *item) 
    Inserts the item item into list list in front of index index. 

int PyList_Append(PyObject *list, PyObject *item) 
    Appends the object item at the end of list list.


TUPLES:
int PyTuple_Check(PyObject *p) 
    Return true if the argument is a tuple object.

PyObject* PyTuple_New(int s) 
    Return a new tuple object of size s.

int PyTuple_Size(PyTupleObject *p) 
    Takes a pointer to a tuple object, and returns the size of that tuple.

PyObject* PyTuple_GetItem(PyTupleObject *p, int pos) 
    Returns the object at position pos in the tuple pointed to by p. 

int PyTuple_SetItem(PyTupleObject *p, int pos, PyObject *o) 
    Inserts a reference to object o at position pos of tuple pointed to by p.

int _PyTuple_Resize(PyTupleObject *p, int new, int last_is_sticky) 
    Expands a tuple in-place (see HighLevelApi description)


DICTIONARIES:
int PyDict_Check(PyObject *p) 
    Returns true if its argument is a PyDictObject.

PyObject* PyDict_New() 
    Returns a new empty dictionary.

int PyDict_SetItem(PyDictObject *p, PyObject *key, PyObject *val) 
    Inserts value into the dictionary with a key of key. 

int PyDict_SetItemString(PyDictObject *p, char *key, PyObject *val) 
    Inserts value into the dictionary using key as a key. 

int PyDict_DelItemString(PyDictObject *p, char *key) 
    Removes the entry in dictionary p 

PyObject* PyDict_GetItem(PyDictObject *p, PyObject *key) 
    Returns the object from dictionary p which has a key key. 

PyObject* PyDict_GetItemString(PyDictObject *p, char *key) 
    This is the same as PyDict_GetItem(), but key is specified as a char *


FILES:
int PyFile_Check(PyObject *p) 
    Returns true if its argument is a PyFileObject.

PyObject* PyFile_FromString(char *name, char *mode) 
    Creates a new PyFileObject pointing to the file specified in name 
    with the mode specified in mode.

PyObject* PyFile_FromFile(FILE *fp, char *name, char *mode, int (*close)) 
    Creates a new PyFileObject from the already-open fp. 

FILE * PyFile_AsFile(PyFileObject *p) 
    Returns the file object associated with p as a FILE *.



