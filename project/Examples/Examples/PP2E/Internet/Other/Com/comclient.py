####################################################################
# a COM client coded in Python: talk to MS-Word via its COM object
# model; uses either dynamic dispatch (run-time lookup/binding), 
# or the static and faster type-library dispatch if makepy.py has 
# been run; install the windows win32all extensions package to use 
# this interface; Word runs hidden unless Visible is set to 1 (and
# Visible lets you watch, but impacts interactive Word sessions);
####################################################################

from sys import argv
docdir = 'C:\\temp\\'
if len(argv) == 2: docdir = argv[1]              # ex: comclient.py a:\

from win32com.client import Dispatch             # early or late binding
word  = Dispatch('Word.Application')             # connect/start word
word.Visible = 1                                 # else word runs hidden

# create and save new doc file
newdoc = word.Documents.Add()                    # call word methods
spot   = newdoc.Range(0,0)
spot.InsertBefore('Hello COM client world!')     # insert some text
newdoc.SaveAs(docdir + 'pycom.doc')              # save in doc file
newdoc.SaveAs(docdir + 'copy.doc')   
newdoc.Close()

# open and change a doc file
olddoc = word.Documents.Open(docdir + 'copy.doc')
finder = word.Selection.Find
finder.text = 'COM'
finder.Execute()
word.Selection.TypeText('Automation')
olddoc.Close()

# and so on: see Word's COM interface specs
