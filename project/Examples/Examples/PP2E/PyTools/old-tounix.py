#!/usr/local/bin/python
# --SEE FIXEOLN FOR A BETTER SOLUTION--

import old_toboth                               # dos->unix in current dir
old_toboth.convert(From="\r\n", To="\n")        # it's okay to run me > once
