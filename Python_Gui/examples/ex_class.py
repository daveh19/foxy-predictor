from tkinter import *


class MyClass: 

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.printButton = Button(frame, text = 'print stuff', command = self.printMessage)
        self.printButton.pack(side = LEFT)
        
        self.quitButton = Button(frame, text = 'quit', command = frame.quit)
        self.quitButton.pack(side= LEFT)

    def printMessage(self): 
        print('heyyy') 
     


root = Tk()
# create an instance of the class, root window will be treated ad master
b = MyClass(root)

root.mainloop()
