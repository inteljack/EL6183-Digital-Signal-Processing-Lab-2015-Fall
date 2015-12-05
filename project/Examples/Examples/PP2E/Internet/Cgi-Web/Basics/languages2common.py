########################################################
# common objects shared by main and reply page scripts;
# need change only this file to add a new language;
########################################################

inputkey = 'language'                            # input parameter name 

hellos = {
    'Python':    r" print 'Hello World'               ",
    'Perl':      r' print "Hello World\n";            ',
    'Tcl':       r' puts "Hello World"                ',
    'Scheme':    r' (display "Hello World") (newline) ',
    'SmallTalk': r" 'Hello World' print.              ",
    'Java':      r' System.out.println("Hello World"); ',
    'C':         r' printf("Hello World\n");          ',
    'C++':       r' cout << "Hello World" << endl;    ',
    'Basic':     r' 10 PRINT "Hello World"            ',
    'Fortran':   r" print *, 'Hello World'             ",
    'Pascal':    r" WriteLn('Hello World');            "
}

