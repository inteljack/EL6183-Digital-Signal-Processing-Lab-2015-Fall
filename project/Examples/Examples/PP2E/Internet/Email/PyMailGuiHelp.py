#####################################################################
# PyMailGui help text string, in this seperate module only to avoid
# distracting from executable code.  As coded, we throw up this text
# in a simple scrollable text box; in the future, we might instead 
# use an HTML file opened under a web browser (e.g., run a "netscape
# help.html" or DOS "start help.html" command using os.system call
#####################################################################

# must be narrow for Linux info box popups; 
# now uses scrolledtext with buttons instead;

helptext = """
PyMail, version 1.0
February, 2000
Programming Python, 2nd Edition
O'Reilly & Associates

Click main window buttons to process email: 
- Load:\t fetch all (or newly arrived) POP mail from server
- View:\t display selected message nicely formatted
- Save:\t write selected (or all) emails to a chosen file
- Del:\t mark selected (or all) email to be deleted on exit
- Write:\t compose a new email message, send it by SMTP
- Reply:\t compose a reply to selected email, send it by SMTP
- Fwd:\t compose a forward of selected email, send by SMTP
- Quit:\t exit PyMail, delete any marked emails from server 

Click an email in the main window's listbox to select it.
Click the "All" checkbox to apply Save or Del buttons to 
all retrieved emails in the list.  Double-click on an email
in the main window's listbox to view the mail's raw text, 
including mail headers not shown by the View button.

Mail is removed from POP servers on exit only, and only mails
marked for deletion with the Del button are removed, if and 
only if you verify the deletion in a confirmation popup.  

Change the mailconfig.py module file on your own machine to 
reflect your email server names, user name, email address, 
and optional mail signature line added to all composed mails.
Miscellaneous hints:

- Passwords are requested if needed, and not stored by PyMail.
- You may put your password in a file named in mailconfig.py.
- Use ';' between multiple addresses in "To" and "Cc" headers. 
- Reply and Fwd automatically quote the original mail text.  
- Save pops up a dialog for selecting a file to hold saved mails.
- Load only fetches newly-arrived email after the first load.

This client-side program currently requires Python and Tkinter.
It uses Python threads, if installed, to avoid blocking the GUI.
Sending and loading email requires an Internet connection.
"""

if __name__ == '__main__': 
    print helptext                    # to stdout if run alone
    raw_input('Press Enter key')      # pause in DOS console popups
