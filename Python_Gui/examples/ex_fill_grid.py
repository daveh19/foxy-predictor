from tkinter import *

root = Tk()


# ----------------------------------------------------------------
# examples with fill 
# ----------------------------------------------------------------


# bg = background color
# fg = foreground color

#one = Label(root, text = 'one', bg = 'red', fg = 'white')
#one.pack()  

#two = Label(root, text = 'two', bg = 'green', fg = 'black')
#two.pack(fill = X) #label x- size changes with parent size! 


#three = Label(root, text = 'three', bg = 'blue', fg = 'white')
#three.pack(side = LEFT, fill = Y)  


# ----------------------------------------------------------------
# examples with grid 
# ----------------------------------------------------------------

label1 = Label(root, text = 'Name')
label2 = Label(root, text = 'Password')

entry1 = Entry(root) # allows for user input
entry2 = Entry(root)

# grid layout insted of pack allows for finer place specification
# standard alignment  = center, other: use sticky
# grid does not take left/right but N, S, W, E!!

label1.grid(row = 0, sticky = E)
label2.grid(row = 1, sticky = E)

entry1.grid(row  = 0, column = 1)
entry2.grid(row = 1, column = 1)

#create checkbox!
c = Checkbutton(root, text = 'Keep me logged in')
c.grid(columnspan = 2)


root.mainloop()
