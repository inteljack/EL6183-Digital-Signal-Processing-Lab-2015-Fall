#######################################################
# Create forward link pages for relocating a web site.
# Generates one page for every existing site file;
# upload the generated files to your old web site.
# Performance note: the first 2 string.replace calls
# could be moved out of the for loop, but this runs 
# in < 1 second on my Win98 machine for 150 site files.
# Lib note: the os.listdir call can be replaced with:
# sitefiles = glob.glob(sitefilesdir + os.sep + '*') 
# but then the file/directory names must be split
# with: dirname, filename = os.path.split(sitefile); 
#######################################################

import os, string
servername   = 'starship.python.net'     # where site is relocating to
homedir      = '~lutz/home'              # where site will be rooted
sitefilesdir = 'public_html'             # where site files live locally
uploaddir    = 'isp-forward'             # where to store forward files
templatename = 'template.html'           # template for generated pages

try: 
    os.mkdir(uploaddir)                  # make upload dir if needed
except OSError: pass

template  = open(templatename).read()    # load or import template text 
sitefiles = os.listdir(sitefilesdir)     # filenames, no directory prefix

count = 0
for filename in sitefiles:
    fwdname = os.path.join(uploaddir, filename)        # or + os.sep + filename
    print 'creating', filename, 'as', fwdname

    filetext = string.replace(template, '$server$', servername)   # insert text 
    filetext = string.replace(filetext, '$home$',   homedir)      # and write
    filetext = string.replace(filetext, '$file$',   filename)     # file varies
    open(fwdname, 'w').write(filetext)
    count = count + 1

print 'Last file =>\n', filetext
print 'Done:', count, 'forward files created.'
