#!/bin/csh
# -------------------------------------------------------------------
# adds Python interpreter directory to system search path (PATH) 
# adds book examples package root to Python search path (PYTHONPATH)
# change PATH to unix path of your python install directory if needed
# change PP2EHOME to the directory containing the PP2E examples dir
# for unix/linux, run this from (or add it to) your .login or .cshrc
# this is csh code: covert to your unix shell's syntax as necessary
# see the .cshrc file in this directory for a startup file example
# see also: PP2E/Launch_*.py scripts, which auto configure paths
# -------------------------------------------------------------------


setenv PATH $PATH:/usr/bin
setenv PP2EHOME /home/mark/PP2ndEd/examples
setenv PYTHONPATH $PP2EHOME:$PYTHONPATH

echo $PATH
echo $PYTHONPATH
setenv X $PP2EHOME/PP2E


# -------------------------------------------------------------------
# each PP2E dir is a module package, with nested subpackages
# the current directory and standard lib dirs are searched auto
# the first setting below makes PP2E visible:    import PP2E.Gui.xxx
# the second makes all dirs within PP2E visible: import Gui.xxx
# --------------------------------------------------------------------
# change: all cross-dir imports in the book's tree are now relative
# to PP2E root, to avoid name clashes in both my imports and yours;
# else "import Gui.xxx" anywhere depends on order in the search path!
# you only need to add the one dir containing dir PP2E to PYTHONPATH 
# removed: setenv PYTHONPATH $PP2EHOME/PP2E:$PYTHONPATH
# -------------------------------------------------------------------
# unix note: you may need to convert this to unix line-feed format
# if it's in dos format; if you get errors, cd to PP2E and run
# this: 'python PyTools/fixeoln_one.py Config/setup-pp.csh', or
# run the 'PP2E/tounix.py' script convert all text files at once;
# you can also simply "source" this file in your shell to set paths
# --------------------------------------------------------------------
# integration note: you may also need to source setup-pp-embed.csh 
# for some of the examples which embed Python in C (since python is
# then a linked-in lib instead of the 'python' program, which tends
# to throws off auto lib paths in 1.5.2); see that file for details
# --------------------------------------------------------------------
