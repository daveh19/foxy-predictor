from tkinter import *

root = Tk()
#myLabel = Label(root, text = 'text and stuff')
#myLabel.pack()

#upper half of window
topFrame = Frame(root)
topFrame.pack()

#lower half of window
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

#create buttons in topFrame
button1 = Button(topFrame, text = 'Button1', fg = 'red', bg = 'blue')
button2 = Button(topFrame, text = 'Button2', fg = 'blue')
button3 = Button(topFrame, text = 'Button3', fg = 'green')

#create button in bottomFrame
button4 = Button(bottomFrame, text = 'Button4', fg = 'purple')

#by default pack() stacks stuff on top of each other!!
button1.pack(side = LEFT) # places the buttons on the leftmost position --> they will lie next to each other 
button2.pack(side = LEFT)
button3.pack(side = LEFT)

button4.pack(side = BOTTOM) #not really necessary

root.mainloop()
