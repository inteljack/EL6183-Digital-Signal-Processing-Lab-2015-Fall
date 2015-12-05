/********************************************************************
 * Default cinterface lookup routine--simple array.  To use:
 * - Compile this to a .o or .so and 
 * - link with your program or cinterface.so
 * - define a CnameMapTable table to map C names to type/address;
 *
 * CnameMapTable must be defined somewhere in the process;
 * if you can't define a CnameMapTable statically, don't link
 * in this file--instead, define a CnameMapLookup() of your own,
 * and link it with your C program or cinterface.so.  Replace me
 * with something like a hashtable if there are very many names.
 * CnameMapTable is a pointer, so you can change it to point to
 * a new table if you must expand the table dynamically.
 ********************************************************************/

#include <stdlib.h>
#include "cinterface.h" 

extern cnameMapTablePtr CnameMapTable;   /* define me and link to process */

cnameMap *                               
CnameMapLookup(char *attr)               /* def func called by cinterface.so */
{                                        /* on each reference and assignment */
    cnameMap *cname;
    for (cname = *CnameMapTable; cname->name != NULL; cname++) {
        if (strcmp(attr, cname->name) == 0)
            return cname;
    }
    return NULL;   /* reached NULL = not found */
}

