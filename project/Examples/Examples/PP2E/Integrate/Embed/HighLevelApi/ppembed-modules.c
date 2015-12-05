/*****************************************************************************
 * MODULE INTERFACE 
 * make/import/reload a python module by name
 * Note that Make_Dummy_Module could be implemented to keep a table
 * of generated dictionaries to be used as namespaces, rather than 
 * using low level tools to create and mark real modules; this 
 * approach would require extra logic to manage and use the table;
 * see basic example of using dictionaries for string namespaces;
 *****************************************************************************/

#include "ppembed.h"

int PP_RELOAD = 0;    /* reload modules dynamically? */
int PP_DEBUG  = 0;    /* debug embedded code with pdb? */

char *PP_Init(char *modname) {
    Py_Initialize();                               /* init python if needed */
    return modname == NULL? "__main__" : modname;  /* default to '__main__' */
}


int
PP_Make_Dummy_Module(char *modname)   /* namespace for strings, if no file */
{                                     /* instead of sharing __main__ for all */
    PyObject *module, *dict;          /* note: __main__ is created in py_init */
    Py_Initialize();
    module = PyImport_AddModule(modname);    /* fetch or make, no load */
    if (module == NULL)                      /* module not incref'd */
        return -1;                  
    else {                                            /* module.__dict__ */
        dict = PyModule_GetDict(module);              /* ['__dummy__'] = None */
        PyDict_SetItemString(dict, "__dummy__", Py_None); 
        PyDict_SetItemString(dict, "__builtins__", PyEval_GetBuiltins());
        return 0;
    }
}


PyObject *                          /* returns module object named modname  */
PP_Load_Module(char *modname)       /* modname can be "package.module" form */
{                                   /* reload just resets C extension mods  */
    /* 
     * 4 cases:
     * - module "__main__" has no file, and not prebuilt: fetch or make
     * - dummy modules have no files: don't try to reload them
     * - reload=on and already loaded (on sys.modules): "reload()" before use
     * - not loaded yet, or loaded but reload=off: "import" to fetch or load 
     */

    PyObject *module, *sysmods;                  
    modname = PP_Init(modname);                       /* default to __main__ */

    if (strcmp(modname, "__main__") == 0)             /* main: no file */
        return PyImport_AddModule(modname);           /* not increfd */

    sysmods = PyImport_GetModuleDict();               /* get sys.modules dict */
    module  = PyDict_GetItemString(sysmods, modname); /* mod in sys.modules? */
    
    if (module != NULL &&                             /* dummy: no file */
        PyModule_Check(module) && 
        PyDict_GetItemString(PyModule_GetDict(module), "__dummy__")) {
        return module;                                /* not increfd */
    }
    else
    if (PP_RELOAD && module != NULL && PyModule_Check(module)) {
        module = PyImport_ReloadModule(module);       /* reload file,run code */
        Py_XDECREF(module);                           /* still on sys.modules */
        return module;                                /* not increfd */
    }
    else {  
        module = PyImport_ImportModule(modname);      /* fetch or load module */
        Py_XDECREF(module);                           /* still on sys.modules */
        return module;                                /* not increfd */
    }
}


PyObject *
PP_Load_Attribute(char *modname, char *attrname)
{
    PyObject *module;                         /* fetch "module.attr" */
    modname = PP_Init(modname);               /* use before PyEval_CallObject */
    module  = PP_Load_Module(modname);        /* not incref'd, may reload */
    if (module == NULL)
        return NULL;
    return PyObject_GetAttrString(module, attrname);  /* func, class, var,.. */
}                                                     /* caller must xdecref */


/* extra ops */
int 
PP_Run_Command_Line(char *prompt)
{
    int res;               /* interact with python, in "__main__" */
    Py_Initialize();       /* in the program's "stdio" window     */
    if (prompt != NULL)
        printf("[%s <ctrl-d exits>]\n", prompt);
    res = PyRun_InteractiveLoop(stdin, "<stdin>");
    return res;
}
