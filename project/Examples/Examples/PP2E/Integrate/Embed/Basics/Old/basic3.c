#include <Python.h>

main() {
    char *cstr;
    PyObject *pstr, *pmod, *pfunc, *pargs;
    printf("basic3\n");
    Py_Initialize();

    /* get string.uppercase */
    pmod = PyImport_ImportModule("string");
    pstr = PyObject_GetAttrString(pmod, "uppercase");

    /* convert string to C */
    PyArg_Parse(pstr, "s", &cstr);
    printf("%s\n", cstr);
    Py_DECREF(pstr);

    /* call string.lower(string.uppercase) */
    pfunc = PyObject_GetAttrString(pmod, "lower");
    pargs = Py_BuildValue("(s)", cstr);
    pstr  = PyEval_CallObject(pfunc, pargs);
    PyArg_Parse(pstr, "s", &cstr);
    printf("%s\n", cstr);

    /* free owned objects */
    Py_DECREF(pmod);
    Py_DECREF(pstr);
    Py_DECREF(pfunc);        /* not really needed in main() */
    Py_DECREF(pargs);        /* since all memory goes away */
}
