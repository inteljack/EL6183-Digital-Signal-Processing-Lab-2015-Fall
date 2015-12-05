###########################################################
# on browse requests: fetch and display data in new page;
# report data is stored in dictionaries on the database;
# caveat: the '#Si' section links generated for top of page
# indexes work on a recent Internet Explorer, but have been 
# seen to fail on an older Netscape; if they fail, try 
# using 'index only' mode, which uses url links to encode 
# information for creating a new page; url links must be 
# encoded with urllib, not cgi.escape (for text embedded in
# the html reply stream; IE auto changes space to %20 when 
# url is clicked so '+' replacement isn't always needed, 
# but urllib.quote_plus is more robust; web browser adds 
# http://server-name/root-dir/PyErrata/ to indexurl;
###########################################################

import cgi, urllib, sys, string
sys.stderr = sys.stdout            # show errors in browser
indexurl = 'index.cgi'             # minimal urls in links

def generateRecord(record):
    print '<p><table border>'
    rowhtml = '<tr><th align=right>%s:<td>%s\n'
    for field in record.keys():
        if record[field] != '' and field != 'Description':
            print rowhtml % (field, cgi.escape(str(record[field])))

    print '</table></p>'
    field = 'Description'
    text  = string.strip(record[field])
    print '<p><b>%s</b><br><pre>%s</pre><hr>' % (field, cgi.escape(text))

def generateSimpleList(dbase, sortkey):
    records = dbase().loadSortedTable(sortkey)           # make list
    for record in records:
        generateRecord(record)

def generateIndexOnly(dbase, sortkey, kind):
    keys, index = dbase().loadIndexedTable(sortkey)      # make index links
    print '<h2>Index</h2><ul>'                           # for load on click
    for key in keys:               
        html = '<li><a href="%s?kind=%s&sortkey=%s&value=%s">%s</a>' 
        htmlkey    = cgi.escape(str(key))
        urlkey     = urllib.quote_plus(str(key))         # html or url escapes
        urlsortkey = urllib.quote_plus(sortkey)          # change spaces to '+'
        print html % (indexurl,
                      kind, urlsortkey, (urlkey or '(none)'), (htmlkey or '?'))
    print '</ul><hr>'
       
def generateIndexed(dbase, sortkey):
    keys, index = dbase().loadIndexedTable(sortkey)
    print '<h2>Index</h2><ul>'
    section = 0                                          # make index
    for key in keys: 
        html = '<li><a href="#S%d">%s</a>' 
        print html % (section, cgi.escape(str(key)) or '?')
        section = section + 1
    print '</ul><hr>'
    section = 0                                          # make details
    for key in keys:
        html = '<h2><a name="#S%d">Key = "%s"</a></h2><hr>' 
        print html % (section, cgi.escape(str(key)))
        for record in index[key]:
            generateRecord(record)
        section = section + 1

def generatePage(dbase, kind='Errata'):
    form = cgi.FieldStorage()
    try:
        sortkey = form['key'].value
    except KeyError:
        sortkey = None

    print 'Content-type: text/html\n'
    print '<title>PP2E %s list</title>' % kind
    print '<h1>%s list, sorted by "%s"</h1><hr>' % (kind, str(sortkey))

    if not form.has_key('display'):
        generateSimpleList(dbase, sortkey)

    elif form['display'].value == 'list':         # dispatch on display type
        generateSimpleList(dbase, sortkey)        # dict would work here too

    elif form['display'].value == 'indexonly':
        generateIndexOnly(dbase, sortkey, kind)

    elif form['display'].value == 'indexed':
        generateIndexed(dbase, sortkey)

