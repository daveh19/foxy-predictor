from tkinter import *


root = Tk()

def deleteRedLine(): 
    canvas.delete(redLine)
    
def deleteEverything(): 
    canvas.delete(ALL)

canvas = Canvas(root, width = 200, height = 100)
canvas.pack()

blackLine = canvas.create_line(0,0, 200, 50)
redLine = canvas.create_line(0, 100, 200, 50, fill = 'red')

# param is (x,y) of top left of rectangel, width and height
greenBox = canvas.create_rectangle(25, 25, 130, 60, fill = 'green')

deleteButton = Button(root, text = 'delete redLine', command = deleteRedLine)
deleteButton.pack(side = LEFT)

deleteAll = Button(root, text = 'delete all', command = deleteEverything)
deleteAll.pack(side = LEFT)


root.mainloop()
