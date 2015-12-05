########################################################
# get rid of extension examples binaries, plus all
# .pyc bytecode files anywhere in the distribution
# this isn't necessarily executable as is
#########################################################

move examples2e.tgz old-examples2e.tgz
cd examples
python PyTools\cleanpyc.py
cd ..

# if on linux:   cleanall.csh
# if on Windows: python PyTools\cleanpyc.py
# if on Linux:   find . -name "*.pyc" -print -exec rm -f {} \; 

tar -cvf examples2e.tar examples
gzip examples2e.tar
move examples2e.tar.gz examples2e.tgz

