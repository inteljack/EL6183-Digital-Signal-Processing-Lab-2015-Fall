/* simulated file/dbase of orders to be filled */

struct {
    int product;          /* or use a string if key is structured: */
    int quantity;         /* python code can split it up as needed */
    char *buyer;          /* by convention, first-initial+last */
} orders[] = 
{
    {111, 2, "GRossum"     },    /* this would usually be an orders file */
    {222, 5, "LWall"       },    /* which the python code could read too */
    {333, 3, "JOusterhout" },
    {222, 1, "4Spam"       },   
    {222, 0, "LTorvalds"   },    /* the script might live in a database too */
    {444, 9, "ERaymond"    } 
};
int numorders = 6;

