from tkinter import *

root = Tk()

#------------------------------------------------------------------
# binding function via 'command': 
#------------------------------------------------------------------

#def printName():
#    print('hello world')

## 'command' binds a function to a widget
#button1 = Button(root, text= 'print',  command = printName)
#button1.pack()

#------------------------------------------------------------------
# binding function via 'bind': 
#------------------------------------------------------------------

#def printName(event):
#    print('hello world')

## 'command' binds a function to a widget
#button1 = Button(root, text= 'print')
#button1.bind('<Button-1>', printName) # left mouse 
#button1.pack()

#------------------------------------------------------------------
# binding different functions
#------------------------------------------------------------------

def leftClick(event): 
    print('left')
    
def middleClick(event): 
    print('middle')
        
def rightClick(event): 
    print('right')    

# one frame can help to adjust size of window
frame = Frame(root, width = 300, height =250)
frame.bind('<Button-1>', leftClick)
frame.bind('<Button-2>', middleClick)
frame.bind('<Button-3>', rightClick)
frame.pack()


root.mainloop()
