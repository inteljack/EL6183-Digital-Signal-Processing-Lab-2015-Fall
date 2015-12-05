#!/usr/bin/python

DEBUG=0
if DEBUG:
    import sys
    sys.stderr = sys.stdout
    print "Content-type: text/html"; print

import traceback
try:
    from dbswitch import DbaseErrata        # dbfiles or dbshelve
    from submit   import saveAndReply       # reuse save logic

    replyStored = """
    Your report has been entered into the errata database.
    You may view it by returning to the main errata page, and 
    selecting Browse/Errata reports, using your name, or any 
    other report identifying information as the browsing key."""

    replyMailed = """
    Your report has been emailed to the author for review.
    It will not be automatically browsable, but may be added to
    the database anonymously later, if it is determined to be 
    information of general interest."""

    # 'Report state' and 'Submit date' are added when written

    inputs = {'Type':'',            'Severity':'', 
              'Page number':'',     'Chapter number':'',   'Part number':'',
              'Printing Date':'',   'Description':'',      'Submit mode':'',
              'Submitter name':'',  'Submitter email':''}

    saveAndReply(DbaseErrata, inputs, replyStored, replyMailed)

except:
    print "\n\n<pre>"
    traceback.print_exc()

