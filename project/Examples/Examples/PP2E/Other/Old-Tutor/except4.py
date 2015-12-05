speak = 'speak'

def hacker():
    try:
        raise speak              # go to hacker's except 
        print 'not reached'
    except speak:
        print 'Hello world!'
        raise speak              # go to primate's except

def primate():
    try:
        hacker()
        print 'not reached'
    except speak:
        print 'Huh?'
        raise speak              # go to mammal's except

def mammal():
    try:
        primate()
        print 'not reached'
    except speak:
        print 'Spam!'
