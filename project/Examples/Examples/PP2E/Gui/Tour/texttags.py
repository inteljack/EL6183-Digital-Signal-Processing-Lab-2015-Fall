# demo advanced tag and text interfaces

from Tkinter import *
root = Tk()
def hello(event): print 'Got tag event'

# make and config a Text
text = Text()
text.config(font=('courier', 15, 'normal'))                  # set font for all
text.config(width=20, height=12)
text.pack(expand=YES, fill=BOTH)
text.insert(END, 'This is\n\nthe meaning\n\nof life.\n\n')   # insert 6 lines

# embed windows and photos
btn = Button(text, text='Spam', command=lambda: hello(0))    # embed a button
btn.pack()
text.window_create(END, window=btn)                          # embed a photo
text.insert(END, '\n\n')
#img = PhotoImage(file='../gifs/spam.gif')                   # copyrighted :-(
img  = PhotoImage(file='../gifs/pythonPowered.gif')
text.image_create(END, image=img)

# apply tags to substrings
text.tag_add('demo', '1.5', '1.7')                       # tag 'is'
text.tag_add('demo', '3.0', '3.3')                       # tag 'the'
text.tag_add('demo', '5.3', '5.7')                       # tag 'life'
text.tag_config('demo', background='purple')             # change colors in tag
text.tag_config('demo', foreground='white')              # not called bg/fg here
text.tag_config('demo', font=('times', 16, 'underline')) # change font in tag
text.tag_bind('demo', '<Double-1>', hello)               # bind events in tag
root.mainloop()
