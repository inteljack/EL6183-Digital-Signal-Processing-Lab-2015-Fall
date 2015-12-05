echo off
REM -------------------------------------------------------------------
REM adds Python interpreter directory to system search path (PATH) 
REM adds book examples package root to Python search path (PYTHONPATH)
REM change PATH to dos path of your python install directory if needed
REM change PP2EHOME to the directory containing the PP2E examples dir
REM for DOS, add path to this file in c:\autoexec.bat to set globally
REM for NT, you can set these shell vars in the system settings dialog
REM see autoexec.bat file in this directory for a startup file example
REM see also: PP2E/Launch_*.py scripts, which auto configure paths
REM -------------------------------------------------------------------


REM --add Python exe dir: 2.0 or 1.5.2
REM PATH %PATH%;c:\Python20
PATH %PATH%;C:\Python27

REM --add book module package dir
set PP2EHOME=C:\Users\Leander\Dropbox\NYU\EL6183 Digital Signal Processing Lab 2015 Fall\project\Examples\Examples
set PYTHONPATH=%PP2EHOME%;%PYTHONPATH%

echo %PATH%
echo %PYTHONPATH%
set X=%PP2EHOME%\PP2E


REM --------------------------------------------------------------------
REM each PP2E dir is a module package, with nested subpackages
REM the current directory and standard lib dirs are searched auto
REM the first setting below makes PP2E visible:    import PP2E.Gui.xxx
REM the second makes all dirs within PP2E visible: import Gui.xxx
REM --------------------------------------------------------------------
REM change: all cross-dir imports in the book's tree are now relative
REM to PP2E root, to avoid name clashes in both my imports and yours;
REM else "import Gui.xxx" anywhere depends on order in the search path!
REM you only need to add the one dir containing dir PP2E to PYTHONPATH 
REM removed: set PYTHONPATH=%PP2EHOME%\PP2E;%PYTHONPATH%
REM --------------------------------------------------------------------
REM change: Python 2.0 now installs itself and all Tkinter support
REM files in C:\Python20 by default, so you should pick either 1.5.2 
REM and 2.0 install directories to add to your PATH setting above; 
REM --------------------------------------------------------------------

