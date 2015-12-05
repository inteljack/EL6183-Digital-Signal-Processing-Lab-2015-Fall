#!/usr/bin/python
# On 'send' click in main root window

import commonhtml
from externs import mailconfig

commonhtml.editpage(kind='Write', headers={'From': mailconfig.myaddress})
