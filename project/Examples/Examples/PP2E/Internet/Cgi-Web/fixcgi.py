########################################################################
# run fom a unix find command to automate some cgi script install steps;
# example:  find . -name "*.cgi" -print -exec python fixcgi.py \{} \;
# which converts all cgi scripts to unix line-feed format (needed on 
# starship) and gives all cgi files executable mode, else won't be run;
# do also: chmod 777 PyErrata/DbaseFiles/*, vi Extern/Email/mailconfig*;
# related: fixsitename.py, PyTools/fixeoln*.py, System/Filetools
########################################################################

# after: ungzip, untar, cp -r Cgi-Web/* ~/public_html

import sys, string, os
fname = sys.argv[1]
old   = open(fname, 'rb').read()
new   = string.replace(old, '\r\n', '\n')
open(fname, 'wb').write(new)
if fname[-3:] == 'cgi': os.chmod(fname, 0755)       # note octal int: rwx,sgo
