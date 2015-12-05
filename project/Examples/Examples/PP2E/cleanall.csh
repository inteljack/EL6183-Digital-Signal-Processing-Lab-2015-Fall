#!/bin/csh -x
# run me to remove all Python/C integration example binary files
# this can be used before packaging, or to force recompiles

set root = `pwd`/Integrate

cd $root/Extend/Hello;                make -f makefile.hello clean
cd $root/Extend/HelloLib;             make -f makefile.hellolib-o clean
cd $root/Extend/HelloLib;             make -f makefile.hellolib-so clean
cd $root/Extend/Stacks;               make -f makefile.stack clean
cd $root/Extend/Swig;                 make -f makefile.hellolib-swig clean
cd $root/Extend/Swig/Environ;         make -f makefile.environ-swig clean
cd $root/Extend/Swig/Shadow;          make -f makefile.number-swig clean

cd $root/Embed/Basics;                make -f makefile.basics clean
cd $root/Embed/HighLevelApi;          make -f makefile.api clean
cd $root/Embed/TestApi;               make -f makefile.testapi clean
cd $root/Embed/TestApi/WithPackages;  make -f makefile.testapi-pkgs clean
cd $root/Embed/ApiClients;            make -f makefile.clients clean
cd $root/Embed/Inventory;             make -f makefile.inv clean
cd $root/Embed/Inventory/WithDbase;   make -f makefile.inv-dbase clean

cd $root/Mixed/Regist;                make -f makefile.regist clean
cd $root/Mixed/Exports;               make -f makefile.exports clean
cd $root/Mixed/Exports/ClassAndMod;   make -f makefile.exports-class clean

# old Part1 preview examples (deprecated)
#cd $root/../Other\old-Integ;          make -f makefile.embed2 clean
#cd $root/../Other\old-Integ;          make -f makefile.cenviron clean

