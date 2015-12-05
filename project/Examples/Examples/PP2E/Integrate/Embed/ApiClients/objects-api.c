#include <stdio.h>
#include "ppembed.h"

main () {                                   /* with ppembed high-level api */
  int failflag;
  PyObject *pinst;
  char *arg1="sir", *arg2="robin", *cstr;

  failflag = PP_Run_Function("module", "klass", "O", &pinst, "()") || 
             PP_Run_Method(pinst, "method", "s", &cstr, "(ss)", arg1, arg2);

  printf("%s\n", (!failflag) ? cstr : "Can't call objects");
  Py_XDECREF(pinst); free(cstr);
}
