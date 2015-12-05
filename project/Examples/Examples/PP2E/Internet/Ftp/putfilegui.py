###############################################################
# launch ftp putfile function with a reusable form gui class;
# see getfilegui for notes: most of the same caveats apply;
# the get and put forms have been factored into a single 
# class such that changes need only be made in one place;
###############################################################

from Tkinter import mainloop
import putfile, getfilegui

class FtpPutfileForm(getfilegui.FtpForm):
    title = 'FtpPutfileGui'
    mode  = 'Upload'
    def do_transfer(self, filename, servername, remotedir, userinfo):
        putfile.putfile(filename, servername, remotedir, userinfo, 0)

if __name__ == '__main__':
    FtpPutfileForm()
    mainloop()    
