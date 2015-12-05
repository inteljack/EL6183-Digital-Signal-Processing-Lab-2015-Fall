/****************************************************************
 * A thin wrapper around ppembed utilities, plus a
 * custom init routine that creates and exports the
 * C name interface object for use in Python scripts.
 * Also creates and manages a dummy module "runpy" as
 * a namespace for running code strings and objects.
 *
 * Note that Python code uses a global called "cvar", 
 * which is assigned to be a type instance object on start
 * up here, rather than directly refering to the importable 
 * cinterface.so module object.  We could use a simple module
 * object for the cvar interface if all C names we want to 
 * expose are known ahead of time; here, we use a type instance
 * object for the names interface instead, to allow overloading 
 * of the getattr/setattr type instance handlers, which can 
 * either access the actual C vars directly, or call more 
 * generic C lookup routines.  This type-based interface lets 
 * us get/set C vars using qualification syntax in Python 
 * (cvar.name, cvar.name = val).  With a simple module 
 * interface, we're limited to function calls (cmod.get('name'),
 * cmod.getname(), etc.), since there's no notion of operator
 * overloading.  The C extension module can also define 
 * other functions besides the name interface type instance
 * constructor function; for instance, C can exports calls to 
 * set a result instead of fetching presumably-set globals.
 *****************************************************************/

#include <Python.h>
#include <ppembed.h>
#include "runpy.h"

char *RunPyError = NULL;
static char* mynamespace = "runpy";


/********************************************************
 * Call me first, to:
 * - make a new namespace for running strings, 
 * - assign global "cvar" 
 *       to new cinterface.Cvar() type instance object,
 * - assign global "cinterface" 
 *       to preimported cinterface module object;
 * along the way, this initializes Python libs, and 
 * dynamically loads the cinterface.so extension module
 * file (it's first imported here, by Python API calls);
 * roughly the same as doing this in every Python script:
 *     >>> import cinterface
 *     >>> cvar = cinterface.Cvar()
 * but note that this code will only work in Python code
 * run from a C program that defines CnameMapTable (and
 * CnameMessage)--the cinterface module must be able to 
 * link to this C name when it is first imported;
 ********************************************************/

int RunPyInitialize()
{
    int stat;
    PyObject *cinterfaceModule = NULL;
    PyObject *cvarTypeInstance = NULL;
 
    /* fetch module, call cinterface.Cvar(); imports the .so   */
    /* can't call C funcs in cinterface.so directly from C--   */
    /* not yet loaded, so we need to go through the Python API */

    cinterfaceModule = PP_Load_Module("cinterface");
    if (cinterfaceModule == NULL) {
        RunPyError = "Can't import module cinterface";
        return -1;
    }

    stat = PP_Run_Function("cinterface", "Cvar", "O", &cvarTypeInstance, "()"); 
    if (stat != 0) {
        RunPyError = "Can't call cinterface.Cvar()";
        return -1;
    }

    /* assign global names, visible to embedded code */

    stat = PP_Make_Dummy_Module(mynamespace);
    if (stat != 0) {
        RunPyError = "Can't make module namespace";
        return -1;
    }
  
    stat = PP_Set_Global(mynamespace, "cvar", "O", cvarTypeInstance);
    if (stat != 0) {
        RunPyError = "Can't set 'cvar' name";
        return -1;
    }

    stat = PP_Set_Global(mynamespace, "cinterface", "O", cinterfaceModule);
    if (stat != 0) {
        RunPyError = "Can't set 'cinterface' name";
        return -1;
    }

    return 0;  /* success */
}


/******************************************************** 
 * Run passed-in Python code string, which can use both
 * the preimported "cinterface" module, and the prebuilt
 * "cvar" type instance object; the code is assumed to 
 * do its work and communictae any results by calling 
 * cinterface module functions, and/or by assigning to
 * attributes of the cvar type instance object;
 ********************************************************/

int RunPyExecCodeString(char *code)
{
    int stat;
    stat = PP_Run_Codestr(PP_STATEMENT, code, mynamespace, "", NULL);
    if (stat != 0) {
        RunPyError = "Can't run code string";
        return -1;
    }
    return 0;   /* success */
}


/*****************************************************
 * For efficiency, allow character strings of Python
 * code to be precompiled to bytecode, and run later
 *****************************************************/

PyObject *RunPyCompileCodeString(char *codestr)
{
    PyObject *result = PP_Compile_Codestr(PP_STATEMENT, codestr);
    if (result == NULL) {
        RunPyError = "Can't compile code string";
    }
    return result;   /* caller must xdecref */
}

int RunPyExecBytecode(PyObject *codeobj)
{
    int stat = PP_Run_Bytecode(codeobj, mynamespace, "", NULL);
    if (stat != 0) {
        RunPyError = "Can't run code object";
        return -1;
    }
    return 0;   /* success */
}


/*****************************************************
 * Print extra info about the most recent Python 
 * exception, after an error occurs; this may provide 
 * extra details, beyond the general RunPyError message;
 *****************************************************/

void RunPyPrintPythonErrorInfo()
{
    PP_Fetch_Error_Text();
    printf("Exception type:  %s\n", PP_last_error_type);
    printf("Exception data:  %s\n", PP_last_error_info);
    printf("Exception trace: %s\n", PP_last_error_trace);
}

