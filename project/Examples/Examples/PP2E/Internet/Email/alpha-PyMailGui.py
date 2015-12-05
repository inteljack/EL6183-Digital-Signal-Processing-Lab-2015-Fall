######################################################
# PyMailGui 1.0 - A Python/Tkinter email client.
# Early/experimental version of this program.
#
# Adds a simple Tkinter GUI interface to the pymail
# script's functionality.  Works for pop/smtp based
# email accounts using sockets on the machine on 
# which this script is run.  
#
# I like this script for two main reasons:
# 1) It's scriptable--you control its evolution
# from this point forward, and can easily customize
# and program it by editing the Python code in this
# file, unlike canned products like MS-Outlook.
# 2) It's portable--this script can be used to 
# process your email on any machine with internet
# sockets where Python and Tkinter are installed; 
# use the simple command-line based pymail.py if 
# you have sockets and Python but not Tkinter.
# E.g., I use this to read my pop email account
# from UNIX machines when I'm away from home PC.
#
# There is much room for improvement and new features
# here--left as exercises.  Example extensions: 
# - Add an automatic spam filter, which matches 
#   from/to hdrs etc. with a regex and auto deletes
#   matching messages as they are being downloaded;
# - Auto decoding/unpacking for multi-part emails:
#   see decode*.py scripts here for pointers;
# - Fields in the main list box could be padded to 
#   a standard length or put in distinct widgets.
# - Make me a class to avoid global vars, and make
#   it easier to attach this GUI to another one;
#   that would also allow creation of more than one
#   mail client gui per process, but this won't work
#   as currently designed (deletes in one gui can
#   invalidate others, due to new pop msg numbers); 
# - Inherit from GuiMaker here to get menu/toolbars;
# - In onViewMail, pop up a full-blown TextEditor;
# - Handle wait states better (e.g., use threads);
# - Strip some headers from displayed mail text;
# - Only fetch new mail on 'Load' button--keep the
#   last mbox size, and retrieve oldsize+1..newsize;
######################################################


import pymail, mailconfig
import rfc822, StringIO, string, sys
from Tkinter import *
from tkFileDialog  import asksaveasfilename
from tkMessageBox  import showinfo, showerror, askyesno

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

def selectedMsg():
    # get msg selected in main listbox
    # print listBox.curselection()
    if listBox.curselection() == ():
        return 0                                     # empty tuple:no selection
    else:                                            # else zero-based index
        return eval(listBox.curselection()[0]) + 1   # in a 1-item tuple of str

def modalinfobox(message):
    # popup wait message box
    new = Toplevel()
    new.title('PyMail Wait')
    Label(new, text=message+'...', height=10, width=40, cursor='watch').pack()
    new.focus()
    new.update()
    return new   # new.focus/grab?, new.destroy to erase

def onLoadMail():
    # load all pop email
    getpassword()
    win = modalinfobox('Retrieving mail')
    global msgList
    try:
        msgList = pymail.loadmessages(mailserver, mailuser, mailpswd)
    except:
        excinfo = '\n' + str(sys.exc_type) + '\n' + str(sys.exc_value)
        showerror('PyMail', 'Error loading mail\n' + excinfo)
    fillIndex(msgList)
    win.destroy()

def onViewMail():
    # view selected message
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        text = msgList[msgnum-1]                # or put in a TextEditor
        from ScrolledText import ScrolledText
        window  = Toplevel()
        window.title('PyMail message viewer #' + str(msgnum))
        browser = ScrolledText(window)
        browser.insert('0.0', text)
        browser.pack(expand=YES, fill=BOTH)

def onSaveMail():
    # save selected message in file
    mailfile = asksaveasfilename(title='PyMail Save File', initialdir='.')
    if mailfile:
        if allModeVar.get():
            for i in range(1, len(msgList)+1):
                pymail.savemessage(i, mailfile, msgList)
        else:
            msgnum = selectedMsg()
            if not (1 <= msgnum <= len(msgList)):
                showerror('PyMail', 'No message selected')
            else:
                pymail.savemessage(msgnum, mailfile, msgList)    

def onDeleteMail():
    # delete selected message on exit
    global toDelete
    if allModeVar.get():
        toDelete = range(1, len(msgList)+1)
    else:
        msgnum = selectedMsg()
        if not (1 <= msgnum <= len(msgList)):
            showerror('PyMail', 'No message selected')
        else:
            toDelete.append(msgnum)

def sendMail(From, To, Cc, Subj, text):
    # send completed email
    import smtplib, time
    from mailconfig import smtpservername
    date  = time.ctime(time.time())
    cchdr = (Cc and 'Cc: %s\n' % Cc) or ''
    hdrs  = ('From: %s\nTo: %s\n%sDate: %s\nSubject: %s\n' 
                     % (From, To, cchdr, date, Subj))
    hdrs = hdrs + 'X-Mailer: PyMail Version 1.0 (Python)\n'
    Tos  = string.split(To, ',') + string.split(Cc, ',')
    win  = modalinfobox('Sending mail')
    print 'Connecting...'
    server = smtplib.SMTP(smtpservername) 
    errors = server.sendmail(From, Tos, hdrs + text)
    server.quit()
    win.destroy()
    if errors:
        showerror('PyMail', 'Error on send:\n' + str(errors))

def onWriteReplyFwdSend(window, editor, hdrs):
    # mail edit window send button press
    From, To, Cc, Subj = hdrs
    sendtext = editor.getAllText()
    sendMail(From.get(), To.get(), Cc.get(), Subj.get(), sendtext)
    window.destroy()

def editmail(mode, From, To='', Subj='', origtext=''):
    # create a mail edit window
    win = Toplevel()
    win.title('PyMail - '+ mode)
    win.iconname('PyMail')

    # header entry fields
    frm =  Frame(win); frm.pack( side=TOP,   fill=X)
    lfrm = Frame(frm); lfrm.pack(side=LEFT,  expand=NO,  fill=BOTH)
    mfrm = Frame(frm); mfrm.pack(side=LEFT,  expand=NO,  fill=NONE)
    rfrm = Frame(frm); rfrm.pack(side=RIGHT, expand=YES, fill=BOTH)
    hdrs = []
    for (label, start) in [('From:', From), 
                           ('To:',   To), 
                           ('Cc:',   ''), 
                           ('Subj:', Subj)]:
        lab = Label(mfrm, text=label, justify=LEFT)
        ent = Entry(rfrm)
        lab.pack(side=TOP, expand=YES, fill=X)
        ent.pack(side=TOP, expand=YES, fill=X)
        ent.insert('0', start)
        hdrs.append(ent)

    # send, cancel buttons
    epatch = [None]
    sendit = (lambda w=win, e=epatch, h=hdrs: onWriteReplyFwdSend(w, e[0], h))
    for (label, callback) in [('Cancel', win.destroy), ('Send', sendit)]:
        b = Button(lfrm, text=label, command=callback)
        b.config(bg='beige', relief=RIDGE, bd=2)
        b.pack(side=TOP, expand=YES, fill=BOTH)

    # body text editor - make,pack last=clip first
    from PP2E.Gui.TextEditor.textEditor import TextEditorComponentMinimal
    editor = epatch[0] = TextEditorComponentMinimal(win)
    editor.pack(side=BOTTOM)
    if mailconfig.mysignature:      # add signature text?
        origtext = ('\n%s\n' % mailconfig.mysignature) + origtext
    editor.setAllText(origtext)

def onWriteMail():
    # compose new email
    editmail('Write', From=mailconfig.myaddress)

def quoteorigtext(msgnum):
    origtext = '\n-----Original Message-----\n' + msgList[msgnum-1]
    origtext = '\n' + string.replace(origtext, '\n', '\n> ')
    return origtext

def onReplyMail():
    # reply to selected email
    msgnum = selectedMsg()
    if not (1 <= msgnum <= len(msgList)):
        showerror('PyMail', 'No message selected')
    else:
        text = quoteorigtext(msgnum)
        hdrs = rfc822.Message(StringIO.StringIO(msgList[msgnum-1]))
        To   = '%s <%s>' % hdrs.getaddr('From')
        From = mailconfig.myaddress or '%s <%s>' % hdrs.getaddr('To')
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
        From = mailconfig.myaddress or '%s <%s>' % hdrs.getaddr('To') 
        Subj = 'Fwd: ' + hdrs.get('Subject', '(no subject)')
        editmail('Forward', From, '', Subj, text)

def onQuitMail():
    # exit mail tool, delete now
    if askyesno('PyMail Verify', 'Verify Quit?'):
        if toDelete:
            showinfo('PyMail', 'Deleting mail from server...')
            getpassword()
            pymail.deletemessages(mailserver, mailuser, mailpswd, toDelete, 0)
            showinfo('PyMail', 'Mail deleted from server...')
        rootWin.quit()

def getpassword():
    # prompt for pop password
    global mailpswd
    if mailpswd:                # getpass.getpass uses stdin, not GUI
        return                  # tkSimpleDialog.askstring echos input
    else:
        win = Toplevel()
        win.title('PyMail Prompt')
        prompt = 'Password for %s on %s?' % (mailuser, mailserver)
        Label(win, text=prompt).pack(side=LEFT)
        entvar = StringVar()
        ent = Entry(win, textvariable=entvar, show='*')
        ent.pack(side=RIGHT)
        ent.bind('<Return>', lambda event, savewin=win: savewin.destroy())
        win.focus_set(); win.grab_set(); win.wait_window()
        win.update()
        mailpswd = entvar.get()    # ent widget is gone

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
    actions = [ ('Load',  onLoadMail),  ('View',  onViewMail),
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
    listBox.bind('<Double-1>', lambda event: onViewMail())
    frame2.pack(side=TOP, expand=YES, fill=BOTH)
    vscroll.pack(side=RIGHT, fill=BOTH)
    listBox.pack(side=LEFT, expand=YES, fill=BOTH)
    return rootWin

helptext = """
PyMail, version 1.0
February, 2000
Programming Python, 2nd Ed.

Click buttons to process email: 
Load retrieves all your POP mail,
Write sends new mail by SMTP.
Click All to apply Save or Del 
to all retrieved messages.
Click Del to delete selected (or
all) mail from POP server on exit.
Change mailconfig.py to reflect
your email servers, address, and 
optional signature.
"""

def container():
    # use attachment to add help button
    # this is a bit easier with classes
    root  = Tk()
    title = Button(root, text='PyMail - a Python/Tkinter email client')
    title.config(bg='steelblue', fg='white', relief=RIDGE)
    title.config(command=(lambda: showinfo('PyMail', helptext)))
    title.pack(fill=X)
    decorate(root)
    return root
    
# init global/module vars
msgList    = []                          # list of retrieved emails text
toDelete   = []                          # msgnums to be deleted on exit
listBox    = None                        # main window's scrolled msg list 
rootWin    = None                        # the main window of this program
allModeVar = None                        # for All mode checkbox value

mailserver = mailconfig.popservername    # where to read pop email from
mailuser   = mailconfig.popusername      # smtp server in mailconfig too
mailpswd   = None                        # passwd input via a popup here
#mailfile  = mailconfig.savemailfile     # from a file select dialog here

if __name__ == '__main__':
   #run stand-alone or attached
   #rootWin = makemainwindow() 
    rootWin = makemainwindow(container()) 
    rootWin.mainloop()

