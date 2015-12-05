from Tkinter import * 

def onCanvasClick(event):                  
    print 'Got canvas click', event.x, event.y, event.widget
def onObjectClick(event):                  
    print 'Got object click', event.x, event.y, event.widget,
    print event.widget.find_closest(event.x, event.y)   # find text object's id

root = Tk()
canv = Canvas(root, width=100, height=100)
obj1 = canv.create_text(50, 30, text='Click me one')
obj2 = canv.create_text(50, 70, text='Click me two')

canv.bind('<Double-1>', onCanvasClick)                  # bind to whole canvas
canv.tag_bind(obj1, '<Double-1>', onObjectClick)        # bind to drawn item
canv.tag_bind(obj2, '<Double-1>', onObjectClick)        # a tag works here too
canv.pack()
root.mainloop()
