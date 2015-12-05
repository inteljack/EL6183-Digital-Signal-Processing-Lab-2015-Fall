#!/bin/csh -x
# to package all the integration examples code (only)
# used during development to copy over to Windows  

cleanall.csh

mv exlinux.tgz old-exlinux
cp ~/.cshrc .
cp ~/bin/buildlog ./buildlog.linux

tar -cvf exlinux.tar \
    xferall.linux \
    makeall.csh cleanall.csh makeall.log cleanall.log package.csh \
    pkgimports.py pkgimports-trace.py \
    .cshrc setup-pp.csh setup-pp-embed.csh buildlog.linux \
    Integrate Other/old-Integ

gzip exlinux.tar
mv exlinux.tar.gz exlinux.tgz


# su root
# mount -t msdos /dev/hda1 /mnt/windows
# cp exlinux.tgz /mnt/windows/stuff/mark/writing/pp2nded/dev

