PP2E\README-PP2E.txt
Examples distribution for _Programming Python_, 2nd Edition

This file describes how to use the source-code distribution
packaged with the book Programming Python 2nd Edition (all 
the files in and below this directory).  It shows how to run
programs, configure your environment, convert files from DOS 
to UNIX line-feed format, and install Python.  You need to 
read only the first few sections to start running code, but 
because the examples distribution is itself a sophisticated 
Python software system, its structure is worth studying here.

The directory containing this file, named PP2E, has source-code 
for all examples in the book.  Examples can be run right off 
the book's CD, or copied to your machine.  To copy to your 
machine, copy the entire PP2E directory tree to some directory
on your computer, and add the name of the directory containing 
PP2E to your PYTHONPATH shell setting.  Some scripts can be run 
without path configuration: see the Launch_* scripts description 
below.  For configuration hints, see the PP2E/Config directory.
Unless noted otherwise, most filenames in this document refer to 
files in the PP2E directory.

[Do not move this file: Launcher uses it to find the examples root.]



------------------------------------------------------------------------------
1. Quick Start Demos
------------------------------------------------------------------------------

This section explains how to run Python demos on the CD.


1A. The easy way
----------------
If you want to see some Python demos right away, and have access
to an installed Python with the Tkinter extension, you can run
one of the following demo scripts immediately:

    Launch_PyDemos.pyw          (starts the main demo laucher bar)
    Launch_PyGadgets.py         (starts standard utilities)
    Launch_PyGadgets_bar.pyw    (starts a utilities launcher toolbar)
    LaunchBrowser.py            (opens examples index in web browser)

These scripts only require that Python is installed first.  You don't
need to configure your environment first or tweak a Config/setup-pp
file to run them, and they may be run right off the book's CD-ROM (e.g., 
by clicking in them in Windows explorer).  LaunchBrowser will work if 
it can find a web browser on your machine, even if you don't have a 
live Internet link (though some Internet examples' features won't work
completely without a live connection).

Depending on your platform, you can start the scripts above by either:

(1) Double-clicking on the scripts' file names in your file explorer, or
(2) Running the scripts from your system command-line prompt.

The first technique is usually easiest; since Python automatically 
registers itself to open ".py" Python files when installed on Windows,
it just works.  To use the second scheme:

- Start a system command-line shell interface (e.g. a MS-DOS console 
  box on Windows, an xterm window on Linux)
- At the command-line prompt, go to the PP2E examples directory where 
  the files reside (e.g., type  a "cd C:\myexamplesdir\PP2E" command)
- At the command-line prompt, type one of the following commands:

    python Launch_PyDemos.pyw
    python Launch_PyGadgets.py
    python Launch_PyGadgets_bar.pyw
    python LaunchBrowser.py

You may need to replace 'python' with the full path to your Python
program if it is not in a directory already on your PATH setting.

All three of these Launch_* scripts are self-configuring.  They assume 
you have already installed Python (they're written in Python, afterall), 
but they automatically locate your Python program and examples root 
directory, and configure the Python module and system search paths as 
needed to run the book examples.  The Launch scripts should work both 
straight off the book's CD-ROM, or after copying the examples directory
to your hard drive; see comments in file Launcher.py for more details.


1B. The quick guide to installing Python
----------------------------------------
To run Python demos on your machine, you first need a Python interpreter.
On Windows, if there is no Python on your computer, there is a fully
executable Python with Tk GUI support on the book's CD.  It's packaged
as a self-installer program, so it's essentially just a double-click to
install.  In more detail, here is the Python installation procedure: 

(1) Go to the Python2.0 (or Python 1.5.2) directories at the top of the CD,
    from within a Windows file explorer (Python2.0 is newer and recommended)
(2) Go to the WindowsInstall subdirectory there
(3) Double-click on the "*.exe" file you see there (the self-install program)
(4) Answer 'yes', 'next', 'default', or 'continue' to all the questions
    you will be asked while the installer runs (that is, do a default install).
    In 2.0, Tk is automaticaly installed along with Python; for 1.5.2, be sure
    to say 'yes' when asked if you want to install Tcl/Tk too.

Once that's finished, you have a Python on your box.  Now, go click on the 
Launch_PyDemos.pyw file icon in the CD's top-level Examples\PP2E directory
to start some Python demos right away.  Then read on in this file to 
find out how to configure your environment permanently.  

On UNIX and Linux, you may already have a Python installed (it comes standard 
with Linux), but you can also install Python from Linux RPM files in the CD's
LinuxRpm directories, or build Python from the source code packages in the 
CD's SourceDistribution directories.  To build from source, ungzip, untar, 
config, and make.  Linux RPMs are also included for installing an executable
Python quickly on Linux; type "man rpm" on Lunix for unpacking details.  If 
you use a Macintosh, see the Macintosh directories in the Python2.0 root; 
install details are included with Mac packages there.


1C. Running demos manually
--------------------------
You can also run the demo scripts by typing these command lines, after 
cd'ing to the PP2E directory where your example files reside:

    Config\setup-pp.bat     (or "source Config\setup-pp.csh" on Linux)
    python PyDemos.pyw      (start main demo bar interface)

Or one of these:
    python PyGadgets.py
    python PyGadgets_bar.pyw

You'll want to change some of the settings in setup-pp.bat to reflect
directories on your own machine, and may want to invoke setup-pp.bat
in your C:\autoexec.bat so its settings are always available (for 
Linux users: make that setup-pp.csh and your ~/.cshrc instead).  The
advantage of this scheme is that it avoids the search and configuration 
steps performed by the Launch_* scripts mentioned above, and so may
start a bit faster.

PyDemos starts an interface from which you can run many of the 
larger GUI-based examples that appear in the book.  Since most 
of the examples are scattered throughout the PP2E subdirectories,
this file also serves as a quick locator for major GUI examples.
Another top-level script, PyGadgets.py can be started similarly; 
it runs a handful of programs in non-demo mode.  Its relative,
PyGadgets_bar.pyw pops up a button bar to start gadgets on demand.
You can find screen shots of these demo programs in action in the 
book's Preface.

The Internet examples on the PyDemos bar are started with the 
LaunchBrowser.py script, which tries to also find a web browser
on your machine; see that script for more details.  If you start
LaunchBrowser.py directly, it brings up the PyInternetDemos.html
root page by opening a local file on your machine.  In general, 
here are the major top-level programs in the PP2E directory:

PyDemos.pyw
    Button bar for starting major GUI and Internet examples 
PyGadgets.py
    Starts programs in non-demo mode for regular use 
PyGadgets_bar.pyw
    Button bar for starting PyGadgets programs on demand 
Launcher.py
    To start programs without environment settings--finds 
    Python, sets PYTHONPATH, spawns Python programs
Launch_*.py*
    Start PyDemos and PyGadgets with Launcher.py--run these 
    for a quick look without manual configuration
LaunchBrowser.py 
    Opens example web pages with an automatically-located web
    browser, either live on the net, or local web page files

Please note that all of the launcher and demo scripts are written to be
portable, but they have only been tested on Windows98 and Linux at this
time (Tk also works on the Mac, and Python runs on almost every platform
in existence).  These scripts may require minor changes on some platforms,
andmay need to be configure a bit for unique machine configurations; see 
the Larger System Examples chapter in the text for background details.


1D. More about PyDemos and PyGadgets
------------------------------------
Among other things, PyDemos lets you start a clock, calculator,
drawing tool, text-editor, slideshow, and N-across game, all 
coded in Python.  It also includes buttons which attempt to 
start a web browser automatically, for the major Internet example
start pages.  See file PyDemos.pyw for more details about the launcher,
and see the book for more details about the demo programs.

Depending on your system's configuration, you may also be able to
run the PyDemos.pyw file by double-clicking on it in your system's
file browser.  If you can't make it work using a command-line or
double click, you may need to load one of the "Config\setup" files 
first, to set the module search path; see the "Configuration" section 
below and file PyDemos.pyw for details.  To make the demos easily
accessible, you can also drag out a double-clickable shortcut to 
PyDemos.pyw (or Launch_PyDemos.pyw) onto your Windows desktop
(shortcuts work on other platforms as well, though this is very 
platform specific).  The PyGadgets script starts a subset of the 
programs the PyDemos can; PyGadgets starts programs for real use, 
not demonstration.


1E. More about the Internet Demos
---------------------------------
Finally, if you don't have a Python with Tkinter installed (or don't
have Python at all, for that matter), you may also visit the site 
where the book's browser-based Internet examples are maintained.
Simply point your favorite Internet browser to the following URL, 
to see Python CGI scripts at work: 

    http://starship.python.net/~lutz/PyInternetDemos.html

Among other things, this page includes a link to the PyErrata demo
program.  These demos use HTML to build user interfaces, and work by 
running Python programs a remote server machine (CGI scripts), so you
don't need to have Python installed on your own computer to run them.  

You can also find these examples in the PyDemos launcher bar as well 
as the Examples\PP2E\Internet\Cgi-Web directory in this examples 
distribution.  However, they need to be run from the URL above to be 
fully operational (running web page files locally may display a CGI 
script's text instead of running it).  Naturally, many examples in the
book aren't GUI or browser-based; see the text and PP2E directory for 
additional example files, Linux build scripts, and so on.

NOTE: The PyDemos and PyGadgets demo launcher bars ship with their
web page mode set to "-file", such that web demo buttons open local
page files, and do not connect to the Internet.  This is a lowest
common denominator policy, but if you have an Internet link, you 
can change both launchers to view web examples live on the net 
instead, as follows:

- PyDemos: change the variable InternetMode near the top of file 
  PyDemos.pyw to be assigned the value "-live" (not "-file").  

- PyGadgets: edit the LaunchBrowser commandline in the PyNet button's
  entry of mytools, near the bottom of file PyGadgets.py.

This only impacts web demos started by the top-level PyDemos and
PyGadgets launchers; you can always visit demo sites directly. 



------------------------------------------------------------------------------
2. Directory Organization
------------------------------------------------------------------------------

The example files in this distribution are organized by major topics
in the book (one directory for Internet code, one for System examples,
and so on).  The subdirectories within each topics directory usually 
correspond to a particular section or chapter in the book (e.g., the
Internet\Sockets directory contains Network Scripting chapter code).
See the "*.txt" files at the top of subdirectories for more pointers.
There is also a top-level PyTools directory in PP2E, which conatains
Python scripts used to manage the entire tree (described ahead).

Most example tree directories are module packages, to allow qualified
cross-directory imports (__init__.py files identify a containing directory
as a Python module package).  In fact, the entire examples distribution is
one big module package, to make it easy for examples to specify modules 
used elsewhere in the book, and to avoid filename clashes with other 
Python code on your system.  

In general, imports in all examples refer to a file in the same directory
as the importer, or are fully-qualified package import paths rooted at PP2E.
For instance, if an example in PP2E\Integrate\Extend uses a module defined
in PP2E\Gui, it runs an import of one of these forms: 

in PP2E\Integrate\Extend\somefile.py:
    import PP2E.Gui.somemodule
    from   PP2E.Gui.somemodule import name

Your code outside the examples tree can do likewise to reuse example code.
No book tree directories other than PP2E are added to the PYTHONPATH search
path setting.  This is by design: although added nested subdirectories may
allow simpler imports like:

    import Gui.somemodule
    import somemodule

this would also cause potential clashes if you install another package
with a "Gui" package directory or "somemodule" name--either the book 
examples ot that other package would find the wrong code.

By placing all book examples under the PP2E directory, such name clashes
are avoided.  Because of this structure, the examples directory is fairly
self-contained, but the PYTHONPATH setting must generally include the the 
name of the directory containing the PP2E directory (see Config\setup files,
and Lancher.py auto-configuration script). 

See file ..\README-root.txt (that is, in the parent directoy of PP2E)
for more details.



------------------------------------------------------------------------------
3. Configuration Details
------------------------------------------------------------------------------

--------
LATE-BREAKING NEWS: by default on Windows, the Python 2.0 self-installer
installs Python and all Tk support files in directory "C:\Python20", not
in "C:\Program Files\Python" (used by earlier releases including 1.5.2).
Because of that, you may need to edit the PP2E\Config\setup-pp.bat file
to pick either the Python 1.5.2 or 2.0 directories for your PATH setting.
The Launcher.py file has been updated to pick either the 2.0 or 1.5.2 
install directory schemes automatically, and so needs no manual edits or
configuration (unless you've installed Python in a non-standard place).  
--------

Because the PP2E examples directory is used as a module package library by 
various programs, you will eventually want to set your PYTHONPATH search-path
to find it correctly.  Here's what I used while developing the book:

  Config\setup-pp.bat: 
    On MS-Windows, you can run setup-pp.bat from your c:\autoexec.bat
    file, to setup the Python module search path.  On NT, you may also
    be able to set these variables in the system settings dialog (see below).
    Change PP2EHOME to the directory containing the PP2E examples directory.
    This adds only one directory to PYTHONPATH (the one containing PP2E).

  Config\setup-pp.csh:
    The equivalent of setup-pp.bat, but for Unix and Linux systems.
    Add it to or run it from your .login or .cshrc file to make these
    settings always available. Note that you may need to first translate
    this to your system shell's syntax (if you don't use csh), and might
    need to convert to Unix line-ends; see this file for details.

  Config\setup-pp-embed.csh
    Extra path settings which may need to be source'd on Linux and UNIX 
    platforms to get the Python-in-C embedding examples to work (required 
    for embedding examples only: setup-pp.csh is sufficient for all others).

  Config\autoexec.bat (copy of my A:\autoexec.bat on Windows)
  Config\.cshrc       (copy of my ~/.cshrc on Linux)
    Top-level system configuration files I use on my Windows and Linux
    machines.  They invoke setup-pp* files on system start-up; .cshrc adds
    a few extra setting on Linux.  Use, copy, and tweak as appropriate.

  Launch_*
  LaunchBrowser.py:
    These Python scripts are used to start book examples even if you have 
    not configured one of the setup-pp files yet; they automatically find
    paths and configure PYTHONPATH, and locate a web browser on your machine.
    They are an option to the Config files; see above for details.

The settings in the setup-pp files are not necessarily the only ways
to configure the module search path.  In general, you can either 
be more specific in PYTHONPATH, or in package qualifier lists 
within programs.  In some cases, the choice is arbitrary, since 
I've added __init__.py files at multiple levels in a directory 
path, but be careful about adding PP2E subdirectpries to your
PYTHONPATH--it can lead to name clases with other installed files.

I should add that the browser-based internet examples show up in
the PP2E\Internet\Cgi-Web directory in this distribution, but they
really live in a public_html top-level directory on a server machine.
In fact, the CGI script examples cannot be run out of the PP2E  
directory itself, due to the special requirements of CGI scripts. 
The PP2E\Internet\Cgi-Web directory here is a just a copy of the 
public_html directory on a server machine.

Speaking of which: I used (at least) 3 platforms to develop the 
examples in this book.  For instance, Tkinter examples were developed
on Windows98 and later run on Linux, Python/C integration code was 
developed on Red Hat Linux6.0, and Internet work was done on Linux
and other Unix server machineis.  Your configuration details will 
probably vary, but should be similar; PYTHONPATH works the same on 
all Pythons.  On some platforms, though, there are other ways to set
the search path.  Here are a few platform-specific hints:

Windows port
    The Windows port allows the Windows registry to be used, in addition 
    to setting PYTHONPATH in DOS.  On some versions of Windows, rather than 
    changing C:\autoexec.bat and rebooting, you can may also set your path
    by selecting the Control Panel, picking the System icon, clicking on the 
    Environment Settings tab, and typing PYTHONPATH and the path you want 
    (e.g., C:\mypythondir) in the resulting dialog box.  Such settings are 
    permanent, just like autoexec.bat.

JPython
    Under JPython, the Java implementation of Python, the path may take 
    the form of -Dpath command-line arguments on the Java command used 
    to launch a program, or python.path assignments in Java registry files. 
    See JPython documentation for more details.



------------------------------------------------------------------------------
4. Utilities: File Line-end and Permission Conversions
------------------------------------------------------------------------------

This section describes some useful utilities in PP2E\PyTools.


4A. Converting DOS end-of-line format
-------------------------------------
For simplicity, I am no longer shipping two copies of the examples tree 
(one in MS-DOS \r\n line-end format, one in Unix \n line-end format).  
Instead, the CD contains a single copy of the tree in MS-DOS format, 
along with a portable Python script for converting all text files in 
the tree to and from Unix line-end format automatically.

See the Systems chapter for background details on the format difference.
You probably don't care because most text editors do the right thing with
either form, with the notable exception of Notepad on Windows (it doesn't 
handle Unix format).  If these files look like one long line on Windows 
or if you see odd characters at the end of lines under UNIX/Linux, you 
can convert all the text files in this distribution to one or the other 
format all at once, by doing this:

1) Install Python if you haven't already
2) Copy the PP2E root directory to your hard-drive
3) Double-click on the copied file PP2E\tounix.py in a file explorer

   or
   3) cd to the copied PP2E root directory in a console/shell
   4) Type command "python PyTools/fixeoln_all.py tounix"
      or
   4) Type command "python tounix.py" (this simply runs fixeoln_all.py)

Change "tounix" to "todos" in all of the above to convert to MS-DOS 
end-of-line format instead.  The fixeoln_all.py script runs a find to 
locate all text files and converts those that need to be converted to
the target linefeed format.  It can be run over and over without 
problems--it converts only files and lines that need conversion, so
it won't trash files already in the target format.

Also note that files run as executable programs (using the #! trick)
or installed on web server sometimes _must_ be converted from DOS
to Unix line-feed format to work properly (this may vary a bit).
If in doubt, always run the tounix.py conversion utility over the 
whole examples tree as described above, after copying it onto a 
Unix or Linux machine.


4B. Fixing read-only file permissions
-------------------------------------
If you copy the examples off of the book's CD-ROM using standard
Windows drag-and-drop, they may be stored on your hard drive with
read-only persmission settings (since that's what they are marked
as on the CD).  That makes it difficult to edit and change them on
your machine.  If your files are not writeable after copying off
the CD, bring up a DOS console box (or equivalent), go to the top
level PP2E example directory in your hard-drive copy (with a cd 
command), and type either of these command lines:

    python towriteable.py
    python PyTools\fixreadonly-all.py

You may also double-click towriteable (it runs fixreadonly-all).
This automatically makes all example files in the distribution's
directory tree writeable.  You have to install Python before running 
this Python script, of course.  See the systems chapters for more 
details on how this script does its work.  On Unix and Linux, you 
can also fix permissions with a "find" command that does a "chmod" 
to each file, but the Python script above is more portable.


4C. Other tree maintenance tools
--------------------------------
In general, there are a handful of commonly-useful utilities in 
the PP2E\PyTools subdirectory of this distribution:

  fixeoln_all.py: 
     Described above: Convert to/from Unix-style line terminators, so 
     you can use standard text file editors on the target platform.

  fixreadonly-all.py
     Described above: Make all files in a tree writeable again if a 
     drag-and-drop copy marks them as read-only.

  cleanpyc-py.py
     Remove all '*.pyc' byte-code files in a directory tree. 
     Useful for cleaning up before shipping source code files,
     and for removing old .pyc files left from a prior Python
     release (in case they are no longer forward compatible, 
     and in case the book CD ships with any lurking pyc files).
     Run like this in PP2E dir: python PyTools\cleanpyc-py.py

  fixnames_all.py
     Tries to repair file names that became all upper-case in 
     transit.  You shouldn't need it (old DOS-style names in this 
     distribution were fixed with this script awhile ago), but 
     if you ever do, you know where to look. By convention, 
     simple files in the distribution start with a lower case 
     letter; directories start with an upper case.

  search_all.py
     Find all files in the examples distribution containing a 
     given string, portably.  Related tools: see scripts for 
     comparing and copying directory trees in the System examples
     directory; see scripts for installing CGI scripts and fixing
     the site name in web examples in the Internet directory; see 
     PyTools\visitor_edit.py to automatically edit matched files.

  renamer.py: 
     Change file names to lower case in one dir, in order to avoid 
     case-sensitive file system issues; you may also need to change
     import statements if you do this, and should  probably use the
     newer script tree-wide fixnames_all.py instead.



-------------------------------------------------------------------------------
5. Getting Python
-------------------------------------------------------------------------------

If you have access to an already-installed Python, skip this 
section.  If not, you can find Python releases on the enclosed 
CD that were current as of this book's publictaion, but later 
releases must be fecthed off the net.  Here is a quick overview
of what to get, and where to get it:

- If you're using a MS-Windows machine, I recommend the standard
  Python+Tk package currently available at www.python.org, for this
  book.  It's a self-installing executable that you simply download
  and double-click to install.  This package includes the latest
  Python release, the Tkinter GUI extension (and all required Tcl/Tk
  components), the IDLE development GUI, and standard extensions.
  
  If you'll be using Windows-specific extensions (e.g., COM), you 
  will probably want to install the win32all extension package too
  (sometimes called PythonWin); it includes Windows-specific tools
  that supplement the standard Windows Python install, and is also
  available via a link at www.python.org.  See the Downloads link
  at the top of www.python.org for both Windows packages.  It's 
  possible to build Python from its source code on Windows too, 
  but I won't describe how here.

  Finally, you can also find both Python and the Windows extensions
  in other distributions, such as the ActivePython distribution 
  available from ActiveState (see www.activestate.com for details).
  ActiveState will also likely release additional Window tools for
  Python in the near future.

- If you're using a Linux machine, chances are that Python is 
  already availble on your system.  It may or may not have Tkinter
  support, though.  If you need to add Tkinter, try fetching the 
  latest Python Linux RPM from www.python.org (see the Downloads 
  link at the top of that page).  Then, run the appropriate 'rpm'
  command on your machine to install.  You can also fetch the full
  Python source-code package from www.python.org, ungzip, untar,
  and build with 'config' and 'make' commands.  You'll probably
  want to edit Python's Modules/Setup to enable the Tkinter 
  extension and re-make too.  See the Extending chapter for details.

- If you're on a Unix machine, the usual install procedure is to
  fetch and build the full source-code distribution, as described
  above for Linux.

- If you're on a Macintosh, please see the Mac-specific information
  at www.python.org (sorry; I don't use a Mac, so I'm not inclined
  to tell you how you should ;-).  If you're on other platforms,
  see www.python.org too; chances are you'll want to build from the
  source dustribution, but there other packages and documentation for
  various platforms at Python's web site (e.g., Amiga, DOS, OS/2, etc.).
  Ports for Windows CE handhelds are available at python.org, and a 
  PalmPilot port is reportedly in the works as well.



------------------------------------------------------------------------------
6. Updates
------------------------------------------------------------------------------

Watch for updates, supplements, and patches, at this site:

    http://www.rmi.net/~lutz/about-pp.html

Suggested changes, corrections, and other comments, can be 
made and viewed by visiting this site, which runs a CGI 
example in the book:

    http://starship.python.net/~lutz/PyErrata/pyerrata.html

The www.rmi.net site has a link to the pyerrata page as well, so
I suggest stopping there first.  You'll probably be able to get 
to either of the above from Python's site, or O'Reilly's:

    http://www.python.org
    http://www.oreilly.com


Happy Pythoneering.
--Mark Lutz, January 2001

