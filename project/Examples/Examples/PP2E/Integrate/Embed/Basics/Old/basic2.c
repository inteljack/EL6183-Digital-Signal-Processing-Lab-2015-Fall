#include <Python.h>

main() {
    char *cstr;
    PyObject *pstr, *pmod, *pdict;
    printf("basic2\n");
    Py_Initialize();

    /* get string.uppercase */
    pmod  = PyImport_ImportModule("string");
    pdict = PyModule_GetDict(pmod);
    pstr  = PyRun_String("uppercase", Py_eval_input, pdict, pdict);

    /* convert to C */
    PyArg_Parse(pstr, "s", &cstr);
    printf("%s\n", cstr);

    /* assign string.X */
    PyObject_SetAttrString(pmod, "X", pstr);

    /* print string.lower */
    (void) PyRun_String("print lower(X)", Py_file_input, pdict, pdict);
    Py_DECREF(pmod);
    Py_DECREF(pstr);
}
