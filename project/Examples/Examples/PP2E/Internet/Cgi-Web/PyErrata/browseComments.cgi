#!/usr/bin/python

from dbswitch import DbaseComment        # dbfiles or dbshelve
from browse   import generatePage        # reuse html formatter
generatePage(DbaseComment, 'Comment')    # load data, send page

