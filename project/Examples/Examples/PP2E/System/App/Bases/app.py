################################################################################
# an application class hierarchy, for handling top-level components;
# App is the root class of the App hierarchy, extended in other files;
################################################################################

import sys, os, traceback
AppError = 'App class error'                              # errors raised here

class App:                                                # the root class
    def __init__(self, name=None):
        self.name    = name or self.__class__.__name__    # the lowest class
        self.args    = sys.argv[1:] 
        self.env     = os.environ
        self.verbose = self.getopt('-v') or self.getenv('VERBOSE')   
        self.input   = sys.stdin
        self.output  = sys.stdout 
        self.error   = sys.stderr                     # stdout may be piped
    def closeApp(self):                               # not __del__: ref's?
        pass                                          # nothing at this level
    def help(self):
        print self.name, 'command-line arguments:'    # extend in subclass
        print '-v (verbose)'

    ##############################
    # script environment services
    ##############################

    def getopt(self, tag):
        try:                                    # test "-x" command arg
            self.args.remove(tag)               # not real argv: > 1 App?
            return 1                   
        except:
            return 0
    def getarg(self, tag, default=None):
        try:                                    # get "-x val" command arg
            pos = self.args.index(tag)
            val = self.args[pos+1]
            self.args[pos:pos+2] = []
            return val
        except:
            return default                      # None: missing, no default
    def getenv(self, name, default=''):
        try:                                    # get "$x" environment var
            return self.env[name]
        except KeyError:
            return default
    def endargs(self):
        if self.args:
            self.message('extra arguments ignored: ' + `self.args`)
            self.args = []
    def restargs(self):
        res, self.args = self.args, []          # no more args/options
        return res
    def message(self, text):
        self.error.write(text + '\n')           # stdout may be redirected
    def exception(self):
        return (sys.exc_type, sys.exc_value)    # the last exception
    def exit(self, message='', status=1):
        if message: 
            self.message(message)
        sys.exit(status)
    def shell(self, command, fork=0, inp=''):
        if self.verbose:
            self.message(command)                         # how about ipc?
        if not fork:
            os.system(command)                            # run a shell cmd
        elif fork == 1:
            return os.popen(command, 'r').read()          # get its output
        else:                                             # readlines too?
            pipe = os.popen(command, 'w')      
            pipe.write(inp)                               # send it input
            pipe.close()

    #################################################
    # input/output-stream methods for the app itself; 
    # redefine in subclasses if not using files, or 
    # set self.input/output to file-like objects;
    #################################################

    def read(self, *size):       
        return apply(self.input.read, size)
    def readline(self):          
        return self.input.readline()
    def readlines(self):         
        return self.input.readlines()
    def write(self, text):       
        self.output.write(text)
    def writelines(self, text):  
        self.output.writelines(text)

    ###################################################
    # to run the app
    # main() is the start/run/stop execution protocol;
    ###################################################

    def main(self):
        res = None
        try:
            self.start()
            self.run()
            res = self.stop()               # optional return val
        except SystemExit:                  # ignore if from exit()
            pass
        except:
            self.message('uncaught: ' + `self.exception()`)
            traceback.print_exc()
        self.closeApp()
        return res

    def start(self): 
        if self.verbose: self.message(self.name + ' start.')
    def stop(self): 
        if self.verbose: self.message(self.name + ' done.')
    def run(self):  
        raise AppError, 'run must be redefined!'
