import types

def status(module):
    print 'reloading', module.__name__

def transitive_reload(module, visited):
    if not visited.has_key(module):              # trap cycles, dups
        status(module)                           # reload this module
        reload(module)                           # and visit children
        visited[module] = None
        for attrobj in module.__dict__.values():    # for all attrs
            if type(attrobj) == types.ModuleType:   # recur if module
                transitive_reload(attrobj, visited)
        
def reload_all(*args):
    visited = {}
    for arg in args:
        if type(arg) == types.ModuleType:
            transitive_reload(arg, visited)

if __name__ == '__main__':
    import reloadall                # test code: reload myself
    reload_all(reloadall)           # should reload this, types
