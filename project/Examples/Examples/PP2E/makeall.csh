#!/bin/csh -x
# run me to build all Python/C integration examples in the book
# you may need to source the setup-pp-embed.csh file to run some embedding 
# examples; caveat: could be more general if all makefile names were the 
# same, but I wanted filename labels to imply a file's context in the text

set root = `pwd`/Integrate

cd $root/Extend/Hello;                make -f makefile.hello
cd $root/Extend/HelloLib;             make -f makefile.hellolib-o
cd $root/Extend/HelloLib;             make -f makefile.hellolib-so
cd $root/Extend/Stacks;               make -f makefile.stack
cd $root/Extend/Swig;                 make -f makefile.hellolib-swig
cd $root/Extend/Swig/Environ;         make -f makefile.environ-swig
cd $root/Extend/Swig/Shadow;          make -f makefile.number-swig

cd $root/Embed/Basics;                make -f makefile.basics
cd $root/Embed/HighLevelApi;          make -f makefile.api
cd $root/Embed/TestApi;               make -f makefile.testapi
cd $root/Embed/TestApi/WithPackages;  make -f makefile.testapi-pkgs
cd $root/Embed/ApiClients;            make -f makefile.clients
cd $root/Embed/Inventory;             make -f makefile.inv
cd $root/Embed/Inventory/WithDbase;   make -f makefile.inv-dbase

cd $root/Mixed/Regist;                make -f makefile.regist
cd $root/Mixed/Exports;               make -f makefile.exports
cd $root/Mixed/Exports/ClassAndMod;   make -f makefile.exports-class

# old preview examples (defunct)
#cd $root/../Other/old-Integ;          make -f makefile.embed2
#cd $root/../Other/old-Integ;          make -f makefile.cenviron

