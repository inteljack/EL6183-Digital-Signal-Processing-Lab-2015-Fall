def diff(self, other):              # for list-based set
    list = self.data[:]             # copy my list
    for obj in other:               # delete other's nodes
        try:
            list.remove(obj)
        except: 
            pass
    return Set(list)

def diff(self, other):              # for dictionary-based set
    dict = {}                     
    for obj in self.data.keys():    # copy my dictionary
        dict[obj] = None
    for obj in other:               # delete other's keys
        if dict.has_key(obj):
            del dict[obj]
    return Set(dict.keys())
