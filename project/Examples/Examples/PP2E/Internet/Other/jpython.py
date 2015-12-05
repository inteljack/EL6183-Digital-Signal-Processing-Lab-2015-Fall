############################################
# implement a simple calculator in JPython;
# evaluation runs a full expression all at 
# once using the Python eval() built-in-- 
# JPython's compiler is present at run-time
############################################
 
from java import awt                   # get access to Java class libraries
from pawt import swing                 # they look like Python modules here 

labels = ['0', '1', '2', '+',          # labels for calculator buttons
          '3', '4', '5', '-',          # will be used for a 4x4 grid
          '6', '7', '8', '*',
          '9', '.', '=', '/' ]

keys = swing.JPanel(awt.GridLayout(4, 4))     # do Java class library magic
display = swing.JTextField()                  # Python data auto-mapped to Java

def push(event):                              # callback for regular keys
    display.replaceSelection(event.actionCommand)

def enter(event):                             # callback for the '=' key
    display.text = str(eval(display.text))    # use Python eval() to run expr
    display.selectAll()

for label in labels:                          # build up button widget grid
    key = swing.JButton(label)                # on press, invoke Python funcs
    if label == '=':
        key.actionPerformed = enter
    else:
        key.actionPerformed = push
    keys.add(key)

panel = swing.JPanel(awt.BorderLayout())      # make a swing panel
panel.add("North", display)                   # text plus key grid in middle
panel.add("Center", keys)
swing.test(panel)                             # start in a GUI viewer
