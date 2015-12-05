import pickle

def saveDbase(filename, object):
    file = open(filename, 'w')
    pickle.dump(object, file)        # pickle to file
    file.close()                     # any file-like object will do

def loadDbase(filename):
    file = open(filename, 'r')
    object = pickle.load(file)       # unpickle from file
    file.close()                     # recreates object in memory
    return object
