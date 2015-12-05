AI (Artificial Intelligence) examples that are not covered 
very well in the text:


1) PyToe
========
A ticTacToe GUI program, described but not fully listed in the 
_Larger GUI Examples_ chapter.  This is a new program (developed
in the 1999-2000 timeframe) written for the 2nd edition of this book.
It demonstrates basic game search strategies (you play the program).


2) Holmes
=========
The holmes expert system is briefly mentioned to show its rule parser 
logic in the _Text and Language_ chapter.  I don't maintain holmes 
anymore, but it seems to still work as advertised under Python 1.5.2.
If memory serves, holmes dates back to 1993 and pre-1.0 Python releases,
so please note that it is very old code, and not necessarily a good 
coding style example (e.g., it does not use class constructor methods,
as they weren't available when holmes was written).

Below are example Holmes sessions to get you started (this was all
run under Python 1.5.2).  It uses the following holmes interactive
commands:

    += adds a rule
    @@ prints the rulebase
    ?- does backward chaining to prove a query
    +- does forward chaining with a set of facts
    @= loads a rulebase file
    stop exits holmes
    help prints all commands

==================================================================

C:\...\PP2E\Ai\ExpertSystem\holmes\holmes>python holmes.py
-Holmes inference engine-
holmes> += rule pylike if ?X likes coding, ?X likes spam then ?X likes Python
holmes> @@
rule pylike if ?X likes coding, ?X likes spam then ?X likes Python.
holmes>
holmes> ?- mel likes Python
is this true: "mel likes coding" ? y
is this true: "mel likes spam" ? y
yes: (no variables)

show proof ? yes
 "mel likes Python" by rule pylike
    "mel likes coding" by your answer
    "mel likes spam" by your answer
more solutions? n

holmes> +- linda likes spam, linda likes coding
I deduced these facts...
   linda likes Python
I started with these facts...
   linda likes spam
   linda likes coding
time:  0.0

holmes> ?- linda likes ?X
is this true: "linda likes coding" ? y
is this true: "linda likes spam" ? y
yes: linda likes Python

holmes> stop

==================================================================

holmes> += rule 1 if thinks ?x then human ?x
holmes> += rule 2 if human ?x then mortal ?x
holmes> ?- mortal bob
is this true: "thinks bob" ? y
yes: (no variables)

holmes> +- thinks bob
I deduced these facts...
   human bob
   mortal bob
I started with these facts...
   thinks bob
time:  0.0

===================================================================

holmes> @= ..\kbases\zoo.kb
holmes> ?- it is a penguin
is this true: "has feathers" ? y
is this true: "able to fly" ? n
is this true: "black color" ? y
yes: (no variables)

holmes> ?- it is a ?What
is this true: "lives in saltwater" ? n
is this true: "lives in freshwater" ? n
is this true: "has feathers" ? n
is this true: "live births" ? y
is this true: "is omnivorous" ? y
is this true: "is intelligent" ? y
is this true: "technologically advanced" ? n
yes: it is a monkey

show proof ? y
 "it is a monkey" by rule 20
    "subclass primate" by rule 19
       "class mammal" by rule d
          "live births" by your answer
       "is omnivorous" by your answer
       "is intelligent" by your answer
    "not technologically advanced" by failure to prove "technologically advanced"

======================================================================

C:\...\PP2E\Ai\ExpertSystem\holmes\holmes>python holmes.py
-Holmes inference engine-
holmes> @= ..\kbases\fixit.kb
holmes> ?- go toaster ?P ?S
is this true: "toaster works" ? no
is this true: "switch turned on" ? yes
is this true: "toaster runs on batteries" ? no
is this true: "toaster firmly plugged in" ? yes
is this true: "used toaster before" ? yes
is this true: "toaster makes sizzle sound" ? yes
yes: go toaster unit-is-wet dry-it-out

show proof ? yes
 "go toaster unit-is-wet dry-it-out" by rule 1
    "fixit toaster unit-is-wet dry-it-out" by rule t2
       "appliance abuse toaster unit-is-wet dry-it-out" by rule a1
          "toaster makes sizzle sound" by your answer
more solutions?
