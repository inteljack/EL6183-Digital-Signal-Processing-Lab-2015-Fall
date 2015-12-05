# list file tree with os.path.walk
import sys, os

def lister(dummy, dirName, filesInDir):              # called at each dir
    print '[' + dirName + ']'
    for fname in filesInDir:                         # includes subdir names
        path = os.path.join(dirName, fname)          # add dir name prefix
        if not os.path.isdir(path):                  # print simple files only
            print path

if __name__ == '__main__':
    os.path.walk(sys.argv[1], lister, None)          # dir name in cmdline