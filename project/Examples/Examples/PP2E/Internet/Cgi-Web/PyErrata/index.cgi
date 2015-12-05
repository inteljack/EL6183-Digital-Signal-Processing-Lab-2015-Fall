#!/usr/bin/python
######################################################
# run when user clicks on a hyperlink generated for 
# index-only mode by browse.py; input parameters are
# hard-coded into the link url, but there's nothing 
# stopping someone from creating a similar link on 
# their own--don't eval() inputs (security concern);
# note that this script assumes that no data files 
# have been deleted since the index page was created;
# cgi.FieldStorage undoes any urllib escapes in the
# input parameters (%xx and '+' for spaces undone);
######################################################

import cgi, sys, dbswitch
from browse import generateRecord
sys.stderr = sys.stdout
form = cgi.FieldStorage()                                # undoes url encoding

inputs = {'kind':'?', 'sortkey':'?', 'value':'?'}
for field in inputs.keys():
    if form.has_key(field):
        inputs[field] = cgi.escape(form[field].value)    # adds html encoding

if inputs['kind'] == 'Errata':
    dbase = dbswitch.DbaseErrata      
else:
    dbase = dbswitch.DbaseComment

print 'Content-type: text/html\n'
print '<title>%s group</title>' % inputs['kind']
print '<h1>%(kind)s list<br>For "%(sortkey)s" == "%(value)s"</h1><hr>' % inputs

keys, index = dbase().loadIndexedTable(inputs['sortkey'])
key = inputs['value']
if key == '(none)': key = ''
for record in index[key]:
    generateRecord(record)

