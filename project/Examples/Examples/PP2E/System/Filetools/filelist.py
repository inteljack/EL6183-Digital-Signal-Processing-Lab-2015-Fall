class FileList:
    def __init__(self, filename):
        self.file = open(filename, 'r')     # open and save file
    def __getitem__(self, i):               # overload indexing
        line = self.file.readline()
        if line:
            return line                     # return the next line
        else:
            raise IndexError                # end 'for' loops, 'in'
    def __getattr__(self, name):
        return getattr(self.file, name)     # other attrs from real file