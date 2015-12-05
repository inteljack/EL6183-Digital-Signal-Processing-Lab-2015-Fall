/******************************************************************** 
 * Define hellolib.c exports to the C namespace, not to Python
 * programs--the latter is defined by a method registration
 * table in a Python extension module's code, not by this .h;
 ********************************************************************/

extern char *message(char *label);  

