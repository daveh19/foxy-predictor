from tkinter import *

def doNothing(): 
    print('did nothing!')

root = Tk()




#------------------------------------------------------------------
# Menu bar
#------------------------------------------------------------------


myMenu = Menu(root)
root.config(menu = myMenu)

subMenu = Menu(myMenu)
myMenu.add_cascade(label = 'File', menu = subMenu)
subMenu.add_command(label = 'New Project ...', command = doNothing)
subMenu.add_command(label = 'New...', command = doNothing)
subMenu.add_separator()
subMenu.add_command(label = 'Exit', command = doNothing)

editMenu = Menu(myMenu)
myMenu.add_cascade(label = 'Edit', menu = editMenu)
editMenu.add_command(label = 'Redo', command = doNothing)

#------------------------------------------------------------------
# Tool bar
#------------------------------------------------------------------


toolBar = Frame(root, bg = 'blue')

insertButton = Button(toolBar, text = 'Insert Image', command = doNothing)
insertButton.pack(side = LEFT, padx = 2, pady = 2)

printButton = Button(toolBar, text = 'Print', command = doNothing) 
printButton.pack(side = LEFT, padx = 2, pady = 2)
toolBar.pack(side= TOP, fill = X)


#------------------------------------------------------------------
# Status bar
#------------------------------------------------------------------

statusBar = Label(root, text = 'Preparing to do noting...', bd = 1, relief = SUNKEN, anchor = W)

statusBar.pack(side = BOTTOM, fill = X)














root.mainloop()
