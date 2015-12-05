import string
def replace(str, old, new):                  # global substitution
    list = string.splitfields(str, old)      # split around old's
    return string.joinfields(list, new)      # rejoin, inserting new's
