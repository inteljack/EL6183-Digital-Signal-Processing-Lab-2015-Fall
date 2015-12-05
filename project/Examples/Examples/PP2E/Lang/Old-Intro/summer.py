import string, sys

def summer(numCols, fileName):
    sums = [0] * numCols                             # make list of zeros
    for line in open(fileName, 'r').readlines():     # scan file's lines
        cols = string.split(line)                    # split up columns
        for i in range(numCols):                     # around blanks/tabs
            sums[i] = sums[i] + eval(cols[i])        # add numbers to sums
    return sums

if __name__ == '__main__':
    print summer(eval(sys.argv[1]), sys.argv[2])     # '% summer.py cols file'
