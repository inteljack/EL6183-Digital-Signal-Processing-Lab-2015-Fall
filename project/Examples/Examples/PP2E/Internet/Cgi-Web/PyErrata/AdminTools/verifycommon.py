#################################################################
# put common verify code in a shared module for consistency and
# reuse; could also generalize dbase update scan, but this helps
#################################################################

def markAsVerify(report):
    report['Report state'] = 'Verified by author'

def markAsReject(report):
    reason = ''                               # input reject reason text
    while 1:                                  # prepend to original desc
        try:
            line = raw_input('reason>')
        except EOFError:
            break
        reason = reason + line + '\n'
    report['Report state'] = 'Rejected - not a real bug'
    report['Description']  = ('Reject reason: ' + reason + 
                 '\n[Original description=>]\n' + report['Description'])
