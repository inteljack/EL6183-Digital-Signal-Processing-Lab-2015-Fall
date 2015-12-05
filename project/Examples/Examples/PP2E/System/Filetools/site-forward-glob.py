#######################################################
# Same, but with glob.glob, not os.listdir
#######################################################

import os, string, glob
uploaddir    = 'rmi-forward'             # where to store forward files
servername   = 'starship.python.net'     # where site is relocating to
homedir      = '~lutz'                   # where site will be rooted
sitefilesdir = 'public_html'             # where site files live locally
templatename = 'template.html'           # template for generated pages

template  = open(templatename).read()
sitefiles = glob.glob(sitefilesdir + os.sep + '*')     # with directories
#print sitefiles

count = 0
for sitefile in sitefiles:
    dirname, filename = os.path.split(sitefile)        # get filename at end
    fwdname = os.path.join(uploaddir, filename)        # or + os.sep + filename
    print 'creating', dirname, filename, 'as', fwdname

    filetext = string.replace(template, '$server$', servername)   # insert text 
    filetext = string.replace(filetext, '$home$',   homedir)      # and write
    filetext = string.replace(filetext, '$file$',   filename)     # file varies
    open(fwdname, 'w').write(filetext)
    count = count + 1

print 'Last file =>\n', filetext
print 'Done:', count, 'forward files created.'

