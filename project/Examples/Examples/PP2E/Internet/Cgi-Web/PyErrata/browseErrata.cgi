#!/usr/bin/python

from dbswitch import DbaseErrata         # dbfiles or dbshelve
from browse   import generatePage        # reuse html formatter
generatePage(DbaseErrata)                # load data, send page

