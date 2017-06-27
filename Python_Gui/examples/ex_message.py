from tkinter import *
import tkinter.messagebox


root = Tk()

tkinter.messagebox.showinfo('Window Title', 'text to fill the void')

answer = tkinter.messagebox.askquestion('Question 1', 'Would you say yes to this?')

if answer == 'yes':
    print('NO!')
 


root.mainloop()
