/********************************************************* 
 * Map C variables to Python object attributes so they 
 * can be fetched/assigned in Python code; this interface
 * is used from within Python programs so there are no 
 * exported C callables defined here, but the mapping 
 * table or function described below must be defined 
 * somewhere in the enclosing C program's link namespace;
 *
 * To make this interface generally useful, it assumes 
 * that the name->address mapping table and/or function 
 * is defined by whatever C program declares the global 
 * names to be exported to Python code; this allows the 
 * exported names table or lookup function to differ in 
 * each program/process that runs Python code which 
 * accesses C names--the table or function name references
 * in cinterface may be linked dynamically, when cinterface 
 * is first imported from Python or C; any program which
 * links in a mapping table or function can reuse the
 * cinterface Cvar type; see cinterface.doc for details;
 *********************************************************/

/* table to map name string to C address and type */
typedef enum {INT, STR1, STR2, FLT} cnameMapType;

typedef struct {
    char *       name;                       /* python object attribute name */
    cnameMapType typecode;                   /* type of this C variable */
    void *       address;                    /* address of this C variable */
} cnameMap;

typedef cnameMap (*cnameMapTablePtr)[];      /* pointer to array of cnameMap */ 
typedef cnameMap* cnameMapFunction(char *);  /* lookup returns &cnameMap */

