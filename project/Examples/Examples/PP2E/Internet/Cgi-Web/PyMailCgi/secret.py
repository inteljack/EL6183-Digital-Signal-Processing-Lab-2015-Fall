###############################################################################
# PyMailCgi encodes the pop password whenever it is sent to/from client over
# the net with a user name as hidden text fields or explicit url params; uses 
# encode/decode functions in this module to encrypt the pswd--upload your own
# version of this module to use a different encryption mechanism; pymail also 
# doesn't save the password on the server, and doesn't echo pswd as typed, but
# this isn't 100% safe--this module file itself might be vulnerable to some
# malicious users; Note: in Python 1.6, the socket module will include standard
# (but optional) support for openSSL sockets on the server, for programming 
# secure Internet transactions in Python; see 1.6 socket module docs;
###############################################################################

forceReadablePassword = 0 
forceRotorEncryption  = 1

import time, string
dayofweek = time.localtime(time.time())[6]

###############################################################################
# string encoding schemes
###############################################################################

if not forceReadablePassword:
    # don't do anything by default: the urllib.quote or
    # cgi.escape calls in commonhtml.py will escape the 
    # password as needed to embed in in URL or HTML; the 
    # cgi module undoes escapes automatically for us;

    def stringify(old):   return old
    def unstringify(old): return old

else:
    # convert encoded string to/from a string of digit chars,
    # to avoid problems with some special/nonprintable chars,
    # but still leave the result semi-readable (but encrypted);
    # some browser had problems with escaped ampersands, etc.;

    separator = '-'

    def stringify(old):
        new = ''
        for char in old:
            ascii = str(ord(char)) 
            new   = new + separator + ascii       # '-ascii-ascii-ascii'
        return new

    def unstringify(old):
        new = ''
        for ascii in string.split(old, separator)[1:]:
            new = new + chr(int(ascii))
        return new 

###############################################################################
# encryption schemes
###############################################################################

if (not forceRotorEncryption) and (dayofweek % 2 == 0):
    # use our own scheme on evenly-numbered days (0=monday)
    # caveat: may fail if encode/decode over midnite boundary
 
    def do_encode(pswd):
        res = ''
        for char in pswd:
            res = res + chr(ord(char) + 1)        # add 1 to each ascii code
        return str(res)

    def do_decode(pswd):
        res = ''
        for char in pswd:
            res = res + chr(ord(char) - 1)
        return res

else:
    # use the standard lib's rotor module to encode pswd
    # this does a better job of encryption than code above

    import rotor
    mykey = 'pymailcgi'

    def do_encode(pswd):
        robj = rotor.newrotor(mykey)              # use enigma encryption
        return robj.encrypt(pswd)        
    
    def do_decode(pswd):
        robj = rotor.newrotor(mykey)
        return robj.decrypt(pswd)        

###############################################################################
# top-level entry points
###############################################################################

def encode(pswd):
    return stringify(do_encode(pswd))             # encrypt plus string encode

def decode(pswd):
    return do_decode(unstringify(pswd))
