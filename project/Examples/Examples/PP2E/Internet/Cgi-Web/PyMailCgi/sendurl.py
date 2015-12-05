####################################################################
# Send email by building a URL like this from inputs:
# http://starship.python.net/~lutz/ 
#     PyMailCgi/onSendSubmit.cgi?site=smtp.rmi.net&
#                                From=lutz@rmi.net&
#                                To=lutz@rmi.net&
#                                Subject=test+url&
#                                text=Hello+Mark;this+is+Mark
####################################################################

from urllib import quote_plus, urlopen

url = 'http://starship.python.net/~lutz/PyMailCgi/onSendSubmit.cgi'
url = url + '?site=%s'    % quote_plus(raw_input('Site>'))    
url = url + '&From=%s'    % quote_plus(raw_input('From>'))    
url = url + '&To=%s'      % quote_plus(raw_input('To  >'))    
url = url + '&Subject=%s' % quote_plus(raw_input('Subj>'))    
url = url + '&text=%s'    % quote_plus(raw_input('text>'))    # or input loop

print 'Reply html:'
print urlopen(url).read()    # confirmation or error page html
