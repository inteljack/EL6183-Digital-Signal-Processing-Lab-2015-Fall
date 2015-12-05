######################################################
# PyMailGui 1.0 - A Python/Tkinter email client.
# Adds a Tkinter-based GUI interface to the pymail
# script's functionality.  Works for POP/SMTP based
# email accounts using sockets on the machine on 
# which this script is run.  Uses threads if 
# installed to run loads, sends, and deletes with
# no blocking; threads are standard on Windows.
# GUI updates done in main thread only (Windows).
# Reuses and attaches TextEditor class object.
# Run from command-line to see status messages.
# See use notes in help text in PyMailGuiHelp.py.
# To do: support attachments, shade deletions.
######################################################

# get services
import pymail, mailconfig
import rfc822, StringIO, string, sys
from Tkinter       import *
from tkFileDialog  import asksaveasfilename, SaveAs
from tkMessageBox  import showinfo, showerror, askyesno
from PP2E.Gui.TextEditor.textEditor import TextEditorComponentMinimal

# run if no threads
try:                                     # raise ImportError to
    import thread                        # run with gui blocking
except ImportError:                      # no wait popups appear 
    class fakeThread:
        def start_new_thread(self, func, args):
            apply(func, args)
    thread = fakeThread()

# init global/module vars
msgList       = []                       # list of retrieved emails text
toDelete      = []                       # msgnums to be deleted on exit
listBox       = None                     # main window's scrolled msg list 
rootWin       = None                     # the main window of this program
allModeVar    = None                     # for All mode checkbox value
threadExitVar = 0                        # used to signal child thread exit
debugme       = 0                        # enable extra status messages

mailserver = mailconfig.popservername    # where to read pop email from
mailuser   = mailconfig.popusername      # smtp server in mailconfig too
mailpswd   = None                        # pop passwd via file or popup here
#mailfile  = mailconfig.savemailfile     # from a file select dialog here


def fillIndex(msgList):
    # fill all of main listbox
    listBox.delete(0, END)
    count = 1
    for msg in msgList:
        hdrs = rfc822.Message(StringIO.StringIO(msg))
        msginfo = '%02d' % count
        for key in ('Subject', 'From', 'Date'):
            if hdrs.has_key(key): msginfo = msginfo + ' | ' + hdrs[key][:30]
        listBox.insert(END, msginfo)
        count = count+1
    listBox.see(END)         # show most recent mail=last line 


def selectedMsg():
    # get msg selected in main listbox
    # print listBox.curselection()
    if listBox.curselection() == ():
        return 0                                     # empty tuple:no selection
    else:                                            # else zero-based index
        return eval(listBox.curselection()[0]) + 1   # in a 1-item tuple of str


def waitForThreadExit(win):
    import time
    global threadExitVar          # in main thread, watch shared global var
    delay = 0.0                   # 0.0=no sleep needed on Win98 (but hogs cpu)
    while not threadExitVar:
        win.update()              # dispatch any new GUI events during wait
        time.sleep(delay)         # if needed, sleep so other thread can run
    threadExitVar = 0             # at most one child thread active at once


def busyInfoBoxWait(message):
    # popup wait message box, wait for a thread exit
    # main gui event thread stays alive during wait
    # as coded returns only after thread has finished
    # popup.wait_variable(threadExitVar) may work too

    popup = Toplevel()
    popup.title('PyMail Wait')
    popup.protocol('WM_DELETE_WINDOW', lambda:0)       # ignore deletes    
    label = Label(popup, text=message+'...')
    label.config(height=10, width=40, cursor='watch')  # busy cursor
    label.pack()
    popup.focus_set()                                  # grab application
    popup.grab_set()                                   # wait for thread exit
    waitForThreadExit(popup)                           # gui alive during wait
    print 'thread exit caught'
    popup.destroy() 


def loadMailThread():
    # load mail while main thread handles gui events
    global msgList, errInfo, threadExitVar
    print 'load start'
    errInfo = ''
    try:
        nextnum = len(msgList) + 1
        newmail = pymail.loadmessages(mailserver, mailuser, mailpswd, nextnum)
        msgList = msgList + newmail
    except:
        exc_type, exc_value = sys.exc_info()[:2]                # thread exc
        errInfo = '\n' + str(exc_type) + '\n' + str(exc_value)
    print 'load exit'
    threadExitVar = 1   # signal main thread


def onLoadMail():
    # load all (or new) pop email
    getpassword()
    thread.start_new_thread(loadMailThread, ())
    busyInfoBoxWait('Retrieving mail')
    if errInfo:
        global mailpswd            # zap pswd so can reinput
        mailpswd = None
        showerror('PyMail', 'Error loading mail\n' + errInfo)
    fillIndex(msgList)


def onViewRawMail():
    # view selected message - raw mail text with header lines
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        text = msgList[msgnum-1]                # put in ScrolledText
        from ScrolledText import ScrolledText
        window  = Toplevel()
        window.title('PyMail raw message viewer #' + str(msgnum))
        browser = ScrolledText(window)
        browser.insert('0.0', text)
        browser.pack(expand=YES, fill=BOTH)


def onViewFormatMail():
    # view selected message - popup formatted display
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        mailtext = msgList[msgnum-1]            # put in a TextEditor form
        textfile = StringIO.StringIO(mailtext)
        headers  = rfc822.Message(textfile)     # strips header lines
        bodytext = textfile.read()              # rest is message body
        editmail('View #%d' % msgnum,
                  headers.get('From', '?'), 
                  headers.get('To', '?'), 
                  headers.get('Subject', '?'), 
                  bodytext,
                  headers.get('Cc', '?')) 


# use objects that retain prior directory for the next
# select, instead of simple asksaveasfilename() dialog

saveOneDialog = saveAllDialog = None

def myasksaveasfilename_one():
    global saveOneDialog
    if not saveOneDialog:
        saveOneDialog = SaveAs(title='PyMail Save File')
    return saveOneDialog.show()


def myasksaveasfilename_all():
    global saveAllDialog
    if not saveAllDialog:
        saveAllDialog = SaveAs(title='PyMail Save All File')
    return saveAllDialog.show()


def onSaveMail():
    # save selected message in file
    if allModeVar.get():
        mailfile = myasksaveasfilename_all()
        if mailfile:
            try:
                # maybe this should be a thread
                for i in range(1, len(msgList)+1):
                    pymail.savemessage(i, mailfile, msgList)
            except:
                showerror('PyMail', 'Error during save')
    else:
        msgnum = selectedMsg()
        if not (1 <= msgnum <= len(msgList)):
            showerror('PyMail', 'No message selected')
        else:
            mailfile = myasksaveasfilename_one()
            if mailfile:
                try:
                    pymail.savemessage(msgnum, mailfile, msgList)    
                except:
                    showerror('PyMail', 'Error during save')


def onDeleteMail():
    # mark selected message for deletion on exit
    global toDelete
    if allModeVar.get():
        toDelete = range(1, len(msgList)+1)
    else:
        msgnum = selectedMsg()
        if not (1 <= msgnum <= len(msgList)):
            showerror('PyMail', 'No message selected')
        elif msgnum not in toDelete:
            toDelete.append(msgnum)    # fails if in list twice


def sendMailThread(From, To, Cc, Subj, text):
    # send mail while main thread handles gui events
    global errInfo, threadExitVar
    import smtplib, time
    from mailconfig import smtpservername
    print 'send start'

    date  = time.ctime(time.time())
    Cchdr = (Cc and 'Cc: %s\n' % Cc) or ''
    hdrs  = ('From: %s\nTo: %s\n%sDate: %s\nSubject: %s\n' 
                     % (From, To, Cchdr, date, Subj))
    hdrs  = hdrs + 'X-Mailer: PyMailGui Version 1.0 (Python)\n'

    Ccs = (Cc and string.split(Cc, ';')) or []     # some servers reject ['']
    Tos = string.split(To, ';') + Ccs              # cc: hdr line, and To list
    Tos = map(string.strip, Tos)                   # some addrs can have ','s
    print 'Connecting to mail...', Tos             # strip spaces around addrs

    errInfo = ''
    failed  = {}                                   # smtplib may raise except 
    try:                                           # or return failed Tos dict
        server = smtplib.SMTP(smtpservername) 
        failed = server.sendmail(From, Tos, hdrs + text)
        server.quit()
    except:
        exc_type, exc_value = sys.exc_info()[:2]   # thread exc
        excinfo = '\n' + str(exc_type) + '\n' + str(exc_value)
        errInfo = 'Error sending mail\n' + excinfo
    else:
        if failed: errInfo = 'Failed recipients:\n' + str(failed)

    print 'send exit'
    threadExitVar = 1                              # signal main thread


def sendMail(From, To, Cc, Subj, text):
    # send completed email
    thread.start_new_thread(sendMailThread, (From, To, Cc, Subj, text))
    busyInfoBoxWait('Sending mail') 
    if errInfo:
        showerror('PyMail', errInfo)


def onWriteReplyFwdSend(window, editor, hdrs):
    # mail edit window send button press
    From, To, Cc, Subj = hdrs
    sendtext = editor.getAllText()
    sendMail(From.get(), To.get(), Cc.get(), Subj.get(), sendtext)
    if not errInfo: 
        window.destroy()    # else keep to retry or save   


def editmail(mode, From, To='', Subj='', origtext='', Cc=''):
    # create a new mail edit/view window
    win = Toplevel()
    win.title('PyMail - '+ mode)
    win.iconname('PyMail')
    viewOnly = (mode[:4] == 'View')

    # header entry fields
    frm =  Frame(win); frm.pack( side=TOP,   fill=X)
    lfrm = Frame(frm); lfrm.pack(side=LEFT,  expand=NO,  fill=BOTH)
    mfrm = Frame(frm); mfrm.pack(side=LEFT,  expand=NO,  fill=NONE)
    rfrm = Frame(frm); rfrm.pack(side=RIGHT, expand=YES, fill=BOTH)
    hdrs = []
    for (label, start) in [('From:', From),
                           ('To:',   To),           # order matters on send
                           ('Cc:',   Cc), 
                           ('Subj:', Subj)]:
        lab = Label(mfrm, text=label, justify=LEFT)
        ent = Entry(rfrm)
        lab.pack(side=TOP, expand=YES, fill=X)
        ent.pack(side=TOP, expand=YES, fill=X)
        ent.insert('0', start)
        hdrs.append(ent)

    # send, cancel buttons (need new editor)
    editor = TextEditorComponentMinimal(win)
    sendit = (lambda w=win, e=editor, h=hdrs: onWriteReplyFwdSend(w, e, h))

    for (label, callback) in [('Cancel', win.destroy), ('Send', sendit)]:
        if not (viewOnly and label == 'Send'): 
            b = Button(lfrm, text=label, command=callback)
            b.config(bg='beige', relief=RIDGE, bd=2)
            b.pack(side=TOP, expand=YES, fill=BOTH)

    # body text editor: pack last=clip first
    editor.pack(side=BOTTOM)                         # may be multiple editors
    if (not viewOnly) and mailconfig.mysignature:    # add auto signature text?
        origtext = ('\n%s\n' % mailconfig.mysignature) + origtext
    editor.setAllText(origtext)


def onWriteMail():
    # compose new email
    editmail('Write', From=mailconfig.myaddress)


def quoteorigtext(msgnum):
    origtext = msgList[msgnum-1]
    textfile = StringIO.StringIO(origtext)
    headers  = rfc822.Message(textfile)           # strips header lines
    bodytext = textfile.read()                    # rest is message body
    quoted   = '\n-----Original Message-----\n'
    for hdr in ('From', 'To', 'Subject', 'Date'):
        quoted = quoted + ( '%s: %s\n' % (hdr, headers.get(hdr, '?')) )
    quoted   = quoted + '\n' + bodytext
    quoted   = '\n' + string.replace(quoted, '\n', '\n> ')
    return quoted 


def onReplyMail():
    # reply to selected email
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        text = quoteorigtext(msgnum)
        hdrs = rfc822.Message(StringIO.StringIO(msgList[msgnum-1]))
        toname, toaddr = hdrs.getaddr('From')
        if toname and ',' in toname: toname = '"%s"' % toname
        To   = '%s <%s>' % (toname, toaddr)
        From = mailconfig.myaddress or ('%s <%s>' % hdrs.getaddr('To'))
        Subj = 'Re: ' + hdrs.get('Subject', '(no subject)')
        editmail('Reply', From, To, Subj, text)


def onFwdMail():
    # forward selected email
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        text = quoteorigtext(msgnum)
        hdrs = rfc822.Message(StringIO.StringIO(msgList[msgnum-1]))
        From = mailconfig.myaddress or ('%s <%s>' % hdrs.getaddr('To')) 
        Subj = 'Fwd: ' + hdrs.get('Subject', '(no subject)')
        editmail('Forward', From, '', Subj, text)


def deleteMailThread(toDelete):
    # delete mail while main thread handles gui events
    global errInfo, threadExitVar
    print 'delete start'
    try:
        pymail.deletemessages(mailserver, mailuser, mailpswd, toDelete, 0)
    except:
        exc_type, exc_value = sys.exc_info()[:2]
        errInfo = '\n' + str(exc_type) + '\n' + str(exc_value)
    else:
        errInfo = ''
    print 'delete exit'
    threadExitVar = 1   # signal main thread


def onQuitMail():
    # exit mail tool, delete now
    if askyesno('PyMail', 'Verify Quit?'):
        if toDelete and askyesno('PyMail', 'Really Delete Mail?'):
            getpassword()
            thread.start_new_thread(deleteMailThread, (toDelete,))
            busyInfoBoxWait('Deleting mail')
            if errInfo:
                showerror('PyMail', 'Error while deleting:\n' + errInfo)
            else:
                showinfo('PyMail', 'Mail deleted from server')
        rootWin.quit()


def askpassword(prompt, app='PyMail'):    # getpass.getpass uses stdin, not GUI
    win = Toplevel()                      # tkSimpleDialog.askstring echos input
    win.title(app + ' Prompt')
    Label(win, text=prompt).pack(side=LEFT)
    entvar = StringVar()
    ent = Entry(win, textvariable=entvar, show='*')
    ent.pack(side=RIGHT, expand=YES, fill=X)
    ent.bind('<Return>', lambda event, savewin=win: savewin.destroy())
    ent.focus_set(); win.grab_set(); win.wait_window()
    win.update()
    return entvar.get()    # ent widget is now gone


def getpassword():
    # unless known, set global pop password 
    # from client-side file or popup dialog
    global mailpswd
    if mailpswd:                
        return                  
    else:
        try:
            localfile = open(mailconfig.poppasswdfile)
            mailpswd  = localfile.readline()[:-1]
            if debugme: print 'local file password', repr(mailpswd)
        except:
            prompt    = 'Password for %s on %s?' % (mailuser, mailserver)
            mailpswd  = askpassword(prompt)
            if debugme: print 'user input password', repr(mailpswd)


def decorate(rootWin):
    # window manager stuff for main window
    rootWin.title('PyMail 1.0')
    rootWin.iconname('PyMail')
    rootWin.protocol('WM_DELETE_WINDOW', onQuitMail)


def makemainwindow(parent=None):
    # make the main window
    global rootWin, listBox, allModeVar
    if parent:
        rootWin = Frame(parent)             # attach to a parent
        rootWin.pack(expand=YES, fill=BOTH)
    else:       
        rootWin = Tk()                      # assume I'm standalone
        decorate(rootWin)

    # add main buttons at bottom
    frame1 = Frame(rootWin)
    frame1.pack(side=BOTTOM, fill=X)
    allModeVar = IntVar()
    Checkbutton(frame1, text="All", variable=allModeVar).pack(side=RIGHT)
    actions = [ ('Load',  onLoadMail),  ('View',  onViewFormatMail),
                ('Save',  onSaveMail),  ('Del',   onDeleteMail),
                ('Write', onWriteMail), ('Reply', onReplyMail), 
                ('Fwd',   onFwdMail),   ('Quit',  onQuitMail) ]
    for (title, callback) in actions:
        Button(frame1, text=title, command=callback).pack(side=LEFT, fill=X)

    # add main listbox and scrollbar
    frame2  = Frame(rootWin)
    vscroll = Scrollbar(frame2)
    fontsz  = (sys.platform[:3] == 'win' and 8) or 10
    listBox = Listbox(frame2, bg='white', font=('courier', fontsz))
    
    # crosslink listbox and scrollbar
    vscroll.config(command=listBox.yview, relief=SUNKEN)
    listBox.config(yscrollcommand=vscroll.set, relief=SUNKEN, selectmode=SINGLE)
    listBox.bind('<Double-1>', lambda event: onViewRawMail())
    frame2.pack(side=TOP, expand=YES, fill=BOTH)
    vscroll.pack(side=RIGHT, fill=BOTH)
    listBox.pack(side=LEFT, expand=YES, fill=BOTH)
    return rootWin


# load text block string
from PyMailGuiHelp import helptext

def showhelp(helptext=helptext, appname='PyMail'):   # show helptext in
    from ScrolledText import ScrolledText            # a non-modal dialog 
    new  = Toplevel()                                # make new popup window
    bar  = Frame(new)                                # pack first=clip last
    bar.pack(side=BOTTOM, fill=X)
    code = Button(bar, bg='beige', text="Source", command=showsource)
    quit = Button(bar, bg='beige', text="Cancel", command=new.destroy)
    code.pack(pady=1, side=LEFT)
    quit.pack(pady=1, side=LEFT)
    text = ScrolledText(new)                         # add Text + scrollbar
    text.config(font='system',  width=70)            # too big for showinfo
    text.config(bg='steelblue', fg='white')          # erase on btn or return
    text.insert('0.0', helptext)
    text.pack(expand=YES, fill=BOTH)
    new.title(appname + " Help")
    new.bind("<Return>", (lambda event, new=new: new.destroy()))


def showsource():
    # tricky, but open
    try:                                            # like web getfile.cgi
        source = open('PyMailGui.py').read()        # in cwd or below it?
    except: 
        try:                                        # or use find.find(f)[0],
            import os                               # $PP2EHOME, guessLocation
            from PP2E.Launcher import findFirst     # or spawn pyedit with arg
            here   = os.curdir
            source = open(findFirst(here, 'PyMailGui.py')).read()
        except:
            source = 'Sorry - cannot find my source file'
    subject = 'Main script [see also: PyMailGuiHelp, pymail, mailconfig]'
    editmail('View Source Code', 'PyMailGui', 'User', subject, source)


def container():
    # use attachment to add help button
    # this is a bit easier with classes
    root  = Tk()
    title = Button(root, text='PyMail - a Python/Tkinter email client')
    title.config(bg='steelblue', fg='white', relief=RIDGE)
    title.config(command=showhelp)
    title.pack(fill=X)
    decorate(root)
    return root


if __name__ == '__main__':
    # run stand-alone or attach
    rootWin = makemainwindow(container())    # or makemainwindow()
    rootWin.mainloop()
