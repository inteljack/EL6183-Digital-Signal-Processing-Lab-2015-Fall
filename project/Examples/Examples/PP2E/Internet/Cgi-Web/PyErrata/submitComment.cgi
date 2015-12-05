#!/usr/bin/python

DEBUG=0
if DEBUG:
    import sys
    sys.stderr = sys.stdout
    print "Content-type: text/html"; print

import traceback
try:
    from dbswitch import DbaseComment       # dbfiles or dbshelve
    from submit   import saveAndReply       # reuse save logic

    replyStored = """
    Your comment has been entered into the comments database.
    You may view it by returning to the main errata page, and 
    selecting Browse/General comments, using your name, or any 
    other report identifying information as the browsing key."""

    replyMailed = """
    Your comment has been emailed to the author for review.
    It will not be automatically browsable, but may be added to
    the database anonymously later, if it is determined to be 
    information of general use."""

    inputs = {'Description':'',     'Submit mode':'',
              'Submitter name':'',  'Submitter email':''}

    saveAndReply(DbaseComment, inputs, replyStored, replyMailed)

except:    
    print "\n\n<PRE>" 
    traceback.print_exc()

