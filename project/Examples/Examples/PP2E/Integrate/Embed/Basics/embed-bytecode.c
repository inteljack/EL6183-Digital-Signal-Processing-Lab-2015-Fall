/* precompile code strings to bytecode objects */

#include <Python.h>    
#include <compile.h>
#include <eval.h>
 
main() {
    int i;
    char *cval;
    PyObject *pcode1, *pcode2, *pcode3, *presult, *pdict;
    char *codestr1, *codestr2, *codestr3;
    printf("embed-bytecode\n");

    Py_Initialize();
    codestr1 = "import usermod\nprint usermod.message";     /* statements */
    codestr2 = "usermod.transform(usermod.message)";        /* expression */
    codestr3 = "print '%d:%d' % (X, X ** 2),";              /* use input X */

    /* make new namespace dictionary */
    pdict = PyDict_New();
    if (pdict == NULL) return -1;
    PyDict_SetItemString(pdict, "__builtins__", PyEval_GetBuiltins());
 
    /* precompile strings of code to bytecode objects */
    pcode1 = Py_CompileString(codestr1, "<embed>", Py_file_input); 
    pcode2 = Py_CompileString(codestr2, "<embed>", Py_eval_input); 
    pcode3 = Py_CompileString(codestr3, "<embed>", Py_file_input); 

    /* run compiled bytecode in namespace dict */
    if (pcode1 && pcode2 && pcode3) {
        (void)    PyEval_EvalCode((PyCodeObject *)pcode1, pdict, pdict);
        presult = PyEval_EvalCode((PyCodeObject *)pcode2, pdict, pdict);
        PyArg_Parse(presult, "s", &cval); 
        printf("%s\n", cval);            
        Py_DECREF(presult);

        /* rerun code object repeatedly */
        for (i = 0; i <= 10; i++) {
            PyDict_SetItemString(pdict, "X", PyInt_FromLong(i)); 
            (void) PyEval_EvalCode((PyCodeObject *)pcode3, pdict, pdict);
        }
        printf("\n");
    }

    /* free referenced objects */
    Py_XDECREF(pdict);
    Py_XDECREF(pcode1);
    Py_XDECREF(pcode2);
    Py_XDECREF(pcode3);
}
